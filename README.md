# Word Ladder & DNA Mutation Pathway Solver — A* Search Algorithm

A Python tool that finds the shortest transformation chain between two sequences — English words or DNA — changing exactly one character at each step so every intermediate sequence is valid.

**Word Ladder:** `cold -> cord -> card -> ward -> warm`
**DNA Mutation:** `ATCG -> ATCA -> ATGA -> GCGA -> GCTA`

## How It Works

The solver models the problem as a graph where each sequence is a node and edges connect sequences that differ by exactly one character. It then searches for the shortest path using:

- **A\* Search** — Uses `f(n) = g(n) + h(n)` where `g(n)` is the number of steps taken and `h(n)` is the Hamming distance (number of differing characters) to the goal. This heuristic is admissible, guaranteeing an optimal solution while exploring fewer nodes than uninformed search.
- **BFS** — Breadth-first search explores all nodes at the current depth before moving deeper. Guarantees the shortest path but explores more nodes than A*.
- **Dijkstra's Algorithm** — Uses a priority queue with uniform edge cost. Equivalent to BFS for unweighted graphs, included for comparison.

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:** matplotlib, networkx, seaborn (Python 3.10+)

## Usage

### Word Ladder Mode (default)

```bash
python main.py --start cold --goal warm
```

Output:
```
  Mode:           Word Ladder
  Algorithm:      A*
  Path:           cold -> cord -> word -> worm -> warm
  Path length:    4 steps
  Nodes explored: 7
  Time:           0.0001s
```

### Compare all three algorithms

```bash
python main.py --start cold --goal warm --algorithm all
```

### Generate visualizations

```bash
python main.py --start cold --goal warm --visualize
```

Generates four high-resolution PNG images in `output/`:

| File | Description |
|------|-------------|
| `search_graph.png` | Explored subgraph with optimal path highlighted |
| `comparison_chart.png` | Bar chart comparing nodes explored across algorithms |
| `astar_steps.png` | Step-by-step A* expansion panels |
| `heuristic_accuracy.png` | Scatter plot of heuristic estimate vs actual cost |

### Run preset comparison

```bash
python main.py --compare
```

Runs all three algorithms on five word pairs and generates the comparison bar chart.

## DNA Mutation Pathway Analysis

DNA sequences are composed of four nucleotide bases: **A** (Adenine), **T** (Thymine), **G** (Guanine), and **C** (Cytosine). A single-nucleotide mutation changes exactly one base — structurally identical to the word ladder problem. The Hamming distance heuristic is the standard metric used in genetics for comparing sequences.

The solver generates the full search space of all possible DNA sequences for a given length:
- Length 4: 256 sequences (4^4)
- Length 5: 1,024 sequences (4^5)
- Length 6: 4,096 sequences (4^6)
- Length 7+: randomly sampled 5,000 sequences

### DNA mode usage

```bash
# Solve a DNA mutation pathway
python main.py --mode dna --start ATCG --goal GCTA

# Use all three algorithms
python main.py --mode dna --start ATCG --goal GCTA --algorithm all

# Generate all visualizations (saved with dna_ prefix)
python main.py --mode dna --start ATCG --goal GCTA --visualize

# Run preset DNA comparison
python main.py --mode dna --compare

# Use longer sequences (length 5)
python main.py --mode dna --seq-length 5 --start ATCGA --goal GCTAT
```

DNA visualizations are saved with a `dna_` prefix (e.g., `output/dna_search_graph.png`) to avoid overwriting word mode outputs. In DNA mode, explored nodes are colored by their first nucleotide base: A=cyan, T=pink, G=green, C=orange.

## Algorithm Comparison

A* consistently explores fewer nodes than BFS and Dijkstra by using the Hamming distance heuristic to guide the search toward the goal. BFS and Dijkstra explore roughly the same number of nodes (as expected for unweighted graphs), expanding outward uniformly in all directions.

## Project Structure

```
├── main.py              # CLI entry point
├── solver/
│   ├── graph.py         # Dictionary/DNA loading & adjacency graph
│   ├── astar.py         # A* search implementation
│   ├── bfs.py           # BFS implementation
│   ├── dijkstra.py      # Dijkstra implementation
│   ├── dna.py           # DNA sequence generator
│   └── heuristics.py    # Hamming distance heuristic
├── visualizer/
│   ├── search_graph.py  # Search graph visualization
│   ├── comparison.py    # Algorithm comparison bar chart
│   ├── step_viewer.py   # Step-by-step A* expansion
│   └── heuristic_plot.py# Heuristic accuracy scatter plot
├── data/
│   └── dictionary.txt   # Word list (~3,200 words, 3-5 letters)
└── output/              # Generated images
```

## Tech Stack

Python | networkx | matplotlib | seaborn
