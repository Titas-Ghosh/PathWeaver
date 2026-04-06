"""Dictionary loading and adjacency graph construction for word ladders and DNA sequences."""

from collections import defaultdict
from pathlib import Path


class WordGraph:
    """Graph where sequences are nodes and edges connect sequences differing by one character.

    Supports two modes:
        - "word": loads English words from a dictionary file (default)
        - "dna": generates DNA sequences of a given length using bases A, T, G, C
    """

    def __init__(
        self,
        dictionary_path: str = "data/dictionary.txt",
        mode: str = "word",
        seq_length: int = 4,
    ):
        self.words: set[str] = set()
        self.graph: dict[str, list[str]] = defaultdict(list)
        self.words_by_length: dict[int, set[str]] = defaultdict(set)
        self.mode = mode

        if mode == "dna":
            self._load_dna(seq_length)
        else:
            self._load_words(dictionary_path)

        self._build_graph()

    def _load_words(self, path: str) -> None:
        """Read words from file, keep only lowercase alphabetic 3-5 letter words."""
        filepath = Path(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Dictionary file not found: {path}")

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if 3 <= len(word) <= 5 and word.isalpha():
                    self.words.add(word)
                    self.words_by_length[len(word)].add(word)

    def _load_dna(self, seq_length: int) -> None:
        """Generate DNA sequences of the specified length."""
        from solver.dna import generate_dna_sequences

        sequences = generate_dna_sequences(seq_length)
        self.words = sequences
        for seq in sequences:
            self.words_by_length[len(seq)].add(seq)

    def _build_graph(self) -> None:
        """Build adjacency list using pattern-based bucketing.

        For each sequence, generate wildcard patterns by replacing each character
        with '_'. Sequences sharing a pattern are neighbors (differ by one character).
        """
        buckets: dict[str, list[str]] = defaultdict(list)

        for word in self.words:
            for i in range(len(word)):
                pattern = word[:i] + "_" + word[i + 1:]
                buckets[pattern].append(word)

        # Sequences in the same bucket are mutual neighbors
        for bucket_words in buckets.values():
            for i, w1 in enumerate(bucket_words):
                for w2 in bucket_words[i + 1:]:
                    self.graph[w1].append(w2)
                    self.graph[w2].append(w1)

    def get_neighbors(self, word: str) -> list[str]:
        """Return all sequences that differ from the given one by exactly one character."""
        return self.graph.get(word, [])

    def has_word(self, word: str) -> bool:
        """Check if a sequence exists in the graph."""
        return word in self.words
