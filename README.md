<div align="center">

# <img src="https://img.icons8.com/fluency/48/route.png" width="32" height="32" alt="icon"/> PathWeaver

### Sequence Pathfinding Engine

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://pathweaver-rho.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A pathfinding engine that finds the shortest transformation chain between sequences — English words or DNA — changing one character at each step. Three search algorithms, interactive visualization, and a full CLI.

[**Live Demo**](https://pathweaver-rho.vercel.app) &nbsp;&middot;&nbsp; [**Report Bug**](https://github.com/Titas-Ghosh/AI-Poster/issues) &nbsp;&middot;&nbsp; [**Request Feature**](https://github.com/Titas-Ghosh/AI-Poster/issues)

</div>

---

```
  Word Ladder:     cold  ->  cord  ->  word  ->  worm  ->  warm
  DNA Mutation:    ATCG  ->  ATCA  ->  ATGA  ->  GCGA  ->  GCTA
```

---

## &#x2728; Features

| | Feature | Description |
|:-:|---------|-------------|
| &#x1F9E0; | **A\* Search** | Optimal pathfinding with Hamming distance heuristic |
| &#x1F50D; | **BFS & Dijkstra** | Side-by-side algorithm comparison |
| &#x1F3AC; | **Live Visualization** | Interactive step-by-step A\* animation with SVG graph |
| &#x1F9EC; | **DNA Mutation Analysis** | Single-nucleotide mutation pathway discovery |
| &#x1F3A8; | **Material 3 UI** | Dark-themed web interface with pill-shaped controls |
| &#x1F4CA; | **Static Charts** | Search graph, comparison bar chart, A\* steps, heuristic accuracy |
| &#x1F4BB; | **CLI Interface** | Full-featured command line with multiple flags |

---

## &#x2699; How It Works

The solver models the problem as a **graph** where each sequence is a node and edges connect sequences differing by one character. Graph construction uses **pattern-based bucketing** for O(N*L) efficiency:

```
cold  ->  _old  c_ld  co_d  col_    (wildcard patterns)
                  |
cord  ->  _ord  c_rd  co_d  cor_    (share "co_d" -> neighbors!)
```

### Algorithm Comparison

```
                    Nodes Explored (cold -> warm)
  A*        ██ 7
  BFS       ████████████████████████████ 162
  Dijkstra  ██████████████████████████████████████████████████████████████████ 462
```

| Algorithm | Strategy | Explored | Speedup |
|:---------:|----------|:--------:|:-------:|
| **A\*** | `f(n) = g(n) + h(n)` | **7** | **baseline** |
| **BFS** | Level-by-level | 162 | 23x more |
| **Dijkstra** | Priority queue | 462 | 66x more |

> A\* explores **10-100x fewer nodes** by using Hamming distance to guide search toward the goal.

---

## &#x1F680; Quick Start

### Prerequisites

> **Python 3.10+** and **pip** required

### Installation

```bash
# Clone the repository
git clone https://github.com/Titas-Ghosh/AI-Poster.git
cd AI-Poster

# Install dependencies
pip install -r requirements.txt
```

### Launch Web App

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Or use the CLI

```bash
python main.py --start cold --goal warm
```

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

---

## &#x1F310; Web Application

The web UI uses a **Material 3 Expressive** design with a dark purple theme, pill-shaped controls, and rounded cards.

### Views

<table>
<tr>
<td width="50%" valign="top">

**&#x1F4CB; Dashboard**
Overview of loaded dictionary (3,196 words) and DNA sequence space (256 sequences for 4-base)

**&#x1F9EA; Solver**
Enter start/goal words or DNA sequences, pick algorithm(s), and solve. See the path, steps, nodes explored, and execution time.

</td>
<td width="50%" valign="top">

**&#x1F3AC; Live A\* Visualization**
- SVG graph with nodes colored by state
- Play / Pause / Step / Back / Reset controls
- Real-time f(n), g(n), h(n) info panel
- Kamada-Kawai node layout

**&#x1F4CA; Compare**
Run all three algorithms on preset word pairs or DNA sequences side-by-side

</td>
</tr>
</table>

---

## &#x1F4BB; CLI Reference

### Word Ladder Mode

```bash
python main.py --start cold --goal warm                    # A* (default)
python main.py --start cold --goal warm --algorithm all    # All 3 algorithms
python main.py --start cold --goal warm --visualize        # Generate charts
python main.py --compare                                   # Preset comparison
```

### DNA Mutation Mode

```bash
python main.py --mode dna --start ATCG --goal GCTA                     # Solve
python main.py --mode dna --start ATCG --goal GCTA --algorithm all     # All algorithms
python main.py --mode dna --start ATCG --goal GCTA --visualize         # Charts
python main.py --mode dna --compare                                    # Preset pairs
python main.py --mode dna --seq-length 5 --start ATCGA --goal GCTAT   # 5-base
```

### Flags

| Flag | Short | Default | Description |
|:-----|:-----:|:-------:|:------------|
| `--start` | `-s` | | Start word or DNA sequence |
| `--goal` | `-g` | | Goal word or DNA sequence |
| `--algorithm` | `-a` | `astar` | `astar` \| `bfs` \| `dijkstra` \| `all` |
| `--visualize` | `-v` | `false` | Generate all 4 static visualizations |
| `--compare` | `-c` | `false` | Run preset multi-pair comparison |
| `--mode` | `-m` | `word` | `word` \| `dna` |
| `--seq-length` | | `4` | DNA sequence length |
| `--dictionary` | `-d` | `data/dictionary.txt` | Custom dictionary file |

---

## &#x1F9EC; DNA Mutation Pathway Analysis

DNA sequences use four nucleotide bases — structurally identical to the word ladder problem:

```
  A (Adenine)   T (Thymine)   G (Guanine)   C (Cytosine)
```

| Length | Sequences | Method |
|:------:|:---------:|:------:|
| 4 bases | **256** (4^4) | Exhaustive |
| 5 bases | **1,024** (4^5) | Exhaustive |
| 6 bases | **4,096** (4^6) | Exhaustive |
| 7+ bases | **~5,000** | Random sample |

In DNA mode, visualization nodes are colored by first nucleotide: **A**=cyan, **T**=pink, **G**=green, **C**=orange.

---

## &#x1F504; API Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/` | Web interface |
| `POST` | `/api/solve` | Solve a pathway |
| `POST` | `/api/graph-data` | A\* expansion graph for live visualization |
| `POST` | `/api/visualize` | Generate static matplotlib charts |
| `POST` | `/api/compare` | Multi-pair algorithm comparison |

<details>
<summary><b>Example Request</b></summary>

```bash
curl -X POST https://pathweaver-rho.vercel.app/api/solve \
  -H "Content-Type: application/json" \
  -d '{"start":"cold","goal":"warm","algorithm":"all"}'
```

```json
{
  "results": [
    {"algorithm": "A*",       "path_length": 4, "nodes_explored": 7},
    {"algorithm": "BFS",      "path_length": 4, "nodes_explored": 162},
    {"algorithm": "Dijkstra", "path_length": 4, "nodes_explored": 462}
  ]
}
```

</details>

---

## &#x1F4C1; Project Structure

```
pathweaver/
├── app.py                  # Flask web application + API
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment config
│
├── solver/
│   ├── __init__.py         # SearchResult dataclass
│   ├── graph.py            # Word/DNA graph (pattern-based bucketing)
│   ├── astar.py            # A* search with expansion history
│   ├── bfs.py              # Breadth-first search
│   ├── dijkstra.py         # Dijkstra's algorithm
│   ├── dna.py              # DNA sequence generator
│   └── heuristics.py       # Hamming distance heuristic
│
├── visualizer/
│   ├── search_graph.py     # Explored subgraph with optimal path
│   ├── comparison.py       # Algorithm comparison bar chart
│   ├── step_viewer.py      # A* step-by-step expansion panels
│   └── heuristic_plot.py   # Heuristic accuracy scatter plot
│
├── templates/
│   └── index.html          # Web UI (M3 Expressive design)
│
├── data/
│   └── dictionary.txt      # Curated word list (~3,196 words)
└── output/                 # Generated visualization PNGs
```

---

## &#x1F6E0; Tech Stack

<div align="center">

| Layer | Technologies |
|:-----:|:------------|
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) |
| **Algorithms** | ![A*](https://img.shields.io/badge/A*_Search-FF6B6B?style=flat-square) ![BFS](https://img.shields.io/badge/BFS-4ECDC4?style=flat-square) ![Dijkstra](https://img.shields.io/badge/Dijkstra-45B7D1?style=flat-square) |
| **Visualization** | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=plotly&logoColor=white) ![NetworkX](https://img.shields.io/badge/NetworkX-4C8CBF?style=flat-square) ![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat-square) |
| **Frontend** | ![JavaScript](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black) ![SVG](https://img.shields.io/badge/SVG-FFB13B?style=flat-square&logo=svg&logoColor=black) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) |
| **Deployment** | ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white) |

</div>

---

<div align="center">

**[&#x2B06; Back to Top](#-pathweaver)**

</div>
