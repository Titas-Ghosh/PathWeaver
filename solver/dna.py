"""DNA sequence generator for mutation pathway analysis."""

import itertools
import random

BASES = "ATGC"


def generate_dna_sequences(length: int) -> set[str]:
    """Generate valid DNA sequences of the given length.

    For length <= 6: returns ALL possible sequences (4^length).
    For length >= 7: randomly samples 5000 sequences to keep it manageable.
    """
    if length < 1:
        raise ValueError("Sequence length must be at least 1")

    total = 4 ** length

    if length <= 6:
        # Generate all possible sequences
        return {"".join(combo) for combo in itertools.product(BASES, repeat=length)}
    else:
        # Random sample for large search spaces
        sequences: set[str] = set()
        while len(sequences) < min(5000, total):
            seq = "".join(random.choice(BASES) for _ in range(length))
            sequences.add(seq)
        return sequences
