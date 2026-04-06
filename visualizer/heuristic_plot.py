"""Visualization 4 — Heuristic accuracy scatter plot."""

import os
from collections import deque

import matplotlib.pyplot as plt
import seaborn as sns

from solver.graph import WordGraph
from solver.heuristics import hamming_distance


def _bfs_all_distances(graph: WordGraph, source: str) -> dict[str, int]:
    """Compute shortest-path distance from source to all reachable sequences."""
    dist: dict[str, int] = {source: 0}
    queue: deque[str] = deque([source])
    while queue:
        current = queue.popleft()
        for neighbor in graph.get_neighbors(current):
            if neighbor not in dist:
                dist[neighbor] = dist[current] + 1
                queue.append(neighbor)
    return dist


def plot_heuristic_accuracy(
    goal: str,
    graph: WordGraph,
    output_path: str = "output/heuristic_accuracy.png",
    mode: str = "word",
) -> None:
    """Scatter plot of Hamming distance h(n) vs actual shortest-path cost to goal.

    A perfect heuristic would have all points on the y=x line. An admissible
    heuristic has all points on or below the line (never overestimates).
    """
    if mode != "dna":
        goal = goal.lower()

    sns.set_theme(style="whitegrid")

    # Compute actual distances from goal to all same-length sequences via BFS
    actual_distances = _bfs_all_distances(graph, goal)
    seq_length = len(goal)

    h_values: list[int] = []
    actual_values: list[int] = []

    for word in graph.words_by_length.get(seq_length, set()):
        if word in actual_distances:
            h = hamming_distance(word, goal)
            h_values.append(h)
            actual_values.append(actual_distances[word])

    if not h_values:
        print("No reachable sequences found -- skipping heuristic accuracy plot.")
        return

    fig, ax = plt.subplots(figsize=(8, 8))

    # Scatter with transparency for overlapping points
    ax.scatter(
        actual_values, h_values, alpha=0.4, s=30, c="#2196F3",
        edgecolors="white", linewidth=0.3, zorder=2,
    )

    # Perfect heuristic reference line (y = x)
    max_val = max(max(h_values), max(actual_values)) + 1
    ax.plot(
        [0, max_val], [0, max_val], "--", color="#F44336", linewidth=2,
        label="Perfect heuristic (h = actual)", zorder=3,
    )

    ax.set_xlabel("Actual Shortest Path Distance", fontsize=12, fontweight="bold")
    ax.set_ylabel("Hamming Distance Heuristic h(n)", fontsize=12, fontweight="bold")

    if mode == "dna":
        title = f"Heuristic Accuracy \u2014 Hamming Distance for DNA Sequences to '{goal}'"
    else:
        title = f"Heuristic Accuracy \u2014 Hamming Distance vs Actual Cost to '{goal}'"

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
    ax.set_xlim(left=-0.5)
    ax.set_ylim(bottom=-0.5)
    ax.set_aspect("equal", adjustable="box")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved heuristic accuracy plot -> {output_path}")
