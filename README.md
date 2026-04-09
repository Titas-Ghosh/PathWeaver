# PathWeaver - Sequence Pathfinding Engine

A Python-based pathfinding engine that finds the shortest transformation chain between two sequences — English words or DNA — changing exactly one character at each step. Features three search algorithms implemented from scratch, interactive web visualization, and a full CLI.

**Word Ladder:** `cold -> cord -> word -> worm -> warm`
**DNA Mutation:** `ATCG -> ATCA -> ATGA -> GCGA -> GCTA`

---

## Features

- **A\* Search** with Hamming distance heuristic — optimal pathfinding with minimal exploration
- **BFS & Dijkstra** implementations for algorithm comparison
- **Live A\* Visualization** — interactive step-by-step animation showing the algorithm at work
- **DNA Mutation Analysis** — single-nucleotide mutation pathway discovery
- **Material 3 Expressive Web UI** — dark-themed interface with pill-shaped controls
- **4 Static Visualizations** — search graph, comparison chart, A\* steps, heuristic accuracy
- **CLI Interface** — full-featured command line with multiple flags

---

## How It Works

The solver models the problem as a graph where each sequence (word or DNA) is a node and edges connect sequences that differ by exactly one character. Graph construction uses **pattern-based bucketing** for O(N\*L) efficiency — each word generates wildcard patterns (e.g., `cold` produces `_old`, `c_ld`, `co_d`, `col_`) and words sharing a pattern are neighbors.

### Algorithms

| Algorithm | Strategy | Guarantee | Exploration |
|-----------|----------|-----------|-------------|
| **A\*** | `f(n) = g(n) + h(n)` with Hamming distance | Optimal shortest path | Minimal — guided by heuristic |
| **BFS** | Level-by-level expansion | Optimal shortest path | Moderate — explores all directions equally |
| **Dijkstra** | Priority queue, uniform cost | Optimal shortest path | High — no heuristic guidance |

A\* consistently explores **10-100x fewer nodes** than BFS/Dijkstra by using the Hamming distance heuristic to focus the search toward the goal.

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/Titas-Ghosh/AI-Poster.git
cd AI-Poster

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web application server |
| `matplotlib` | Static chart generation |
| `networkx` | Graph layout computation |
| `seaborn` | Enhanced plot styling |

---

## Web Application

### Start the Server

```bash
python app.py
```

Open http://localhost:5000 in your browser.

### Web Interface Overview

The web UI is built with a **Material 3 Expressive** design language featuring a dark purple theme, pill-shaped controls, and rounded card layouts.

**Dashboard** — Overview of loaded dictionary (3,196 words) and DNA sequence space (256 sequences for 4-base)

**Solver** — Enter start/goal words or DNA sequences, select algorithm(s), and solve. Results show the path, steps, nodes explored, and execution time.

**Live A\* Visualization** — After solving, click **"Watch Live A\*"** to see the algorithm work step-by-step:
  - SVG-based graph with nodes colored by state (start, goal, current, open set, closed set, path)
  - Play/Pause/Step/Back/Reset controls with adjustable speed
  - Real-time info panel showing f(n), g(n), h(n), open set size, and closed set size
  - Node positions computed server-side using Kamada-Kawai layout

**Compare** — Run all three algorithms on preset word pairs or DNA sequences side-by-side

**Static Charts** — Generate matplotlib visualizations (search graph, comparison bar chart, A\* expansion steps, heuristic accuracy scatter)

---

## CLI Usage

### Word Ladder Mode (default)

```bash
# Solve with A* (default algorithm)
python main.py --start cold --goal warm

# Compare all three algorithms
python main.py --start cold --goal warm --algorithm all

# Generate all 4 visualizations
python main.py --start cold --goal warm --visualize

# Run preset comparison across 5 word pairs
python main.py --compare
```

**Sample output:**
```
-------------------------------------------------------
  Mode:           Word Ladder
  Algorithm:      A*
  Path:           cold -> cord -> word -> worm -> warm
  Path length:    4 steps
  Nodes explored: 7
  Time:           0.0001s
-------------------------------------------------------
```

### DNA Mutation Mode

```bash
# Solve a DNA mutation pathway
python main.py --mode dna --start ATCG --goal GCTA

# All algorithms on DNA
python main.py --mode dna --start ATCG --goal GCTA --algorithm all

# Generate DNA visualizations (saved with dna_ prefix)
python main.py --mode dna --start ATCG --goal GCTA --visualize

# Preset DNA comparison
python main.py --mode dna --compare

# Longer sequences (5-base)
python main.py --mode dna --seq-length 5 --start ATCGA --goal GCTAT
```

### CLI Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--start` | `-s` | Start word or DNA sequence |
| `--goal` | `-g` | Goal word or DNA sequence |
| `--algorithm` | `-a` | `astar`, `bfs`, `dijkstra`, or `all` (default: `astar`) |
| `--visualize` | `-v` | Generate all 4 static visualizations |
| `--compare` | `-c` | Run preset comparison across multiple pairs |
| `--mode` | `-m` | `word` or `dna` (default: `word`) |
| `--seq-length` | | DNA sequence length (default: 4) |
| `--dictionary` | `-d` | Path to custom dictionary file |

---

## DNA Mutation Pathway Analysis

DNA sequences are composed of four nucleotide bases: **A** (Adenine), **T** (Thymine), **G** (Guanine), **C** (Cytosine). A single-nucleotide mutation changes exactly one base — structurally identical to the word ladder problem.

The solver generates the full search space of all possible DNA sequences:

| Length | Sequences | Method |
|--------|-----------|--------|
| 4 bases | 256 (4^4) | Exhaustive |
| 5 bases | 1,024 (4^5) | Exhaustive |
| 6 bases | 4,096 (4^6) | Exhaustive |
| 7+ bases | ~5,000 | Random sample |

In DNA mode, visualizations color nodes by their first nucleotide: A=cyan, T=pink, G=green, C=orange.

---

## API Endpoints

The Flask backend exposes a JSON API:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface |
| `POST` | `/api/solve` | Solve a pathway (`start`, `goal`, `algorithm`, `mode`) |
| `POST` | `/api/graph-data` | Get A\* expansion graph data for live visualization |
| `POST` | `/api/visualize` | Generate static matplotlib charts |
| `POST` | `/api/compare` | Run multi-pair algorithm comparison |

---

## Project Structure

```
pathweaver/
├── app.py                  # Flask web application
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── solver/
│   ├── __init__.py         # SearchResult dataclass
│   ├── graph.py            # Word/DNA graph with pattern-based bucketing
│   ├── astar.py            # A* search with expansion history
│   ├── bfs.py              # Breadth-first search
│   ├── dijkstra.py         # Dijkstra's algorithm
│   ├── dna.py              # DNA sequence generator
│   └── heuristics.py       # Hamming distance heuristic
├── visualizer/
│   ├── __init__.py
│   ├── search_graph.py     # Explored subgraph with optimal path
│   ├── comparison.py       # Algorithm comparison bar chart
│   ├── step_viewer.py      # A* step-by-step expansion panels
│   └── heuristic_plot.py   # Heuristic accuracy scatter plot
├── templates/
│   └── index.html          # Web UI (M3 Expressive design)
├── data/
│   └── dictionary.txt      # Curated word list (~3,196 words, 3-5 letters)
└── output/                 # Generated visualization PNGs
```

---

## Tech Stack

**Backend:** Python, Flask, networkx, matplotlib, seaborn

**Frontend:** Vanilla JS, SVG, CSS3 (Material 3 Expressive design)

**Algorithms:** A\* Search, BFS, Dijkstra — all implemented from scratch
