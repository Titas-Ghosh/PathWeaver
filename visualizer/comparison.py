"""Visualization 2 — Algorithm comparison bar chart."""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from solver import SearchResult
from solver.astar import astar
from solver.bfs import bfs
from solver.dijkstra import dijkstra
from solver.graph import WordGraph


DEFAULT_WORD_PAIRS = [
    ("cold", "warm"),
    ("head", "tail"),
    ("hide", "seek"),
    ("lead", "gold"),
    ("work", "play"),
]

DNA_WORD_PAIRS = [
    ("ATCG", "GCTA"),
    ("AAAA", "TTTT"),
    ("ATCG", "TAGC"),
    ("AATT", "GGCC"),
    ("ACGT", "TGCA"),
]


def plot_comparison(
    graph: WordGraph,
    word_pairs: list[tuple[str, str]] | None = None,
    output_path: str = "output/comparison_chart.png",
    mode: str = "word",
) -> list[dict]:
    """Run A*, BFS, and Dijkstra on multiple pairs and generate a grouped bar chart.

    Returns a list of result dicts for printing.
    """
    if word_pairs is None:
        word_pairs = DNA_WORD_PAIRS if mode == "dna" else DEFAULT_WORD_PAIRS

    sns.set_theme(style="whitegrid")

    algorithms = [
        ("A*", astar),
        ("BFS", bfs),
        ("Dijkstra", dijkstra),
    ]
    colors = ["#4CAF50", "#2196F3", "#FF9800"]

    labels = [f"{s}\u2192{g}" for s, g in word_pairs]
    results_table: list[dict] = []
    data: dict[str, list[int]] = {name: [] for name, _ in algorithms}

    for start, goal in word_pairs:
        for algo_name, algo_fn in algorithms:
            result = algo_fn(graph, start, goal)
            data[algo_name].append(result.nodes_explored)
            results_table.append({
                "pair": f"{start}->{goal}",
                "algorithm": algo_name,
                "nodes_explored": result.nodes_explored,
                "path_length": result.path_length,
                "path": " -> ".join(result.path) if result.path else "No path",
            })

    # Plot grouped bar chart
    x = np.arange(len(labels))
    width = 0.25
    fig, ax = plt.subplots(figsize=(14 if mode == "dna" else 12, 6))

    for i, (algo_name, _) in enumerate(algorithms):
        bars = ax.bar(
            x + i * width, data[algo_name], width,
            label=algo_name, color=colors[i], edgecolor="white", linewidth=0.8,
        )
        # Value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{int(height)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", fontsize=8, fontweight="bold",
            )

    x_label = "DNA Sequence Pair" if mode == "dna" else "Word Pair"
    title = ("DNA Mutation Pathway \u2014 Algorithm Comparison"
             if mode == "dna"
             else "Algorithm Comparison \u2014 Nodes Explored per Word Pair")

    ax.set_xlabel(x_label, fontsize=12, fontweight="bold")
    ax.set_ylabel("Nodes Explored", fontsize=12, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x + width)
    ax.set_xticklabels(labels, fontsize=9 if mode == "dna" else 10)
    ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
    ax.set_ylim(bottom=0)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved comparison chart -> {output_path}")

    return results_table
