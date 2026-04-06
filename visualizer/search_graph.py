"""Visualization 1 — Search graph showing explored nodes and optimal path."""

import os

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

from solver import SearchResult
from solver.graph import WordGraph

# Nucleotide colors for DNA mode (based on first base)
_NUC_COLORS = {"A": "#00BCD4", "T": "#E91E63", "G": "#4CAF50", "C": "#FF9800"}


def _dna_node_color(seq: str) -> str:
    """Return a color based on the first nucleotide of a DNA sequence."""
    return _NUC_COLORS.get(seq[0], "#E0E0E0")


def plot_search_graph(
    result: SearchResult,
    graph: WordGraph,
    output_path: str = "output/search_graph.png",
    mode: str = "word",
) -> None:
    """Render the subgraph of all explored nodes, highlighting the optimal path.

    Color coding:
        - Blue: start node
        - Red: goal node
        - Green: optimal path nodes (excluding start/goal)
        - Orange: frontier / open set nodes (A* only)
        - Light gray (word) or nucleotide-colored (DNA): other explored nodes
    """
    if result.path is None:
        print("No path found -- skipping search graph visualization.")
        return

    sns.set_theme(style="whitegrid")

    # Collect all nodes to display: explored (closed set) + frontier (open set)
    if result.expansion_history:
        last_step = result.expansion_history[-1]
        explored_nodes = set(last_step["closed_set"])
        frontier_nodes = set(last_step["open_set"])
    else:
        explored_nodes = set()
        for word in result.path:
            explored_nodes.add(word)
            for neighbor in graph.get_neighbors(word):
                explored_nodes.add(neighbor)
        frontier_nodes = set()

    all_nodes = explored_nodes | frontier_nodes
    path_set = set(result.path)
    start, goal = result.path[0], result.path[-1]

    # Build networkx subgraph
    G = nx.Graph()
    G.add_nodes_from(all_nodes)
    for node in all_nodes:
        for neighbor in graph.get_neighbors(node):
            if neighbor in all_nodes:
                G.add_edge(node, neighbor)

    # Layout
    pos = nx.kamada_kawai_layout(G)

    fig, ax = plt.subplots(1, 1, figsize=(14, 10))

    # Categorize nodes for coloring
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == start:
            node_colors.append("#2196F3")  # Blue
            node_sizes.append(700)
        elif node == goal:
            node_colors.append("#F44336")  # Red
            node_sizes.append(700)
        elif node in path_set:
            node_colors.append("#4CAF50")  # Green
            node_sizes.append(600)
        elif node in frontier_nodes and node not in explored_nodes:
            node_colors.append("#FF9800")  # Orange
            node_sizes.append(350)
        else:
            # DNA mode: color by first nucleotide; word mode: light gray
            if mode == "dna":
                node_colors.append(_dna_node_color(node))
            else:
                node_colors.append("#E0E0E0")
            node_sizes.append(350)

    # Draw regular edges (light)
    nx.draw_networkx_edges(G, pos, alpha=0.15, edge_color="#BDBDBD", ax=ax)

    # Draw path edges (thick green)
    path_edges = list(zip(result.path[:-1], result.path[1:]))
    nx.draw_networkx_edges(
        G, pos, edgelist=path_edges, width=3.5, edge_color="#4CAF50",
        alpha=0.9, ax=ax,
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, node_color=node_colors, node_size=node_sizes,
        edgecolors="#424242", linewidths=0.8, ax=ax,
    )

    # Labels
    font_size = 6 if mode == "dna" else 7
    nx.draw_networkx_labels(
        G, pos, font_size=font_size, font_weight="bold", font_color="#212121", ax=ax,
    )

    title_prefix = "A* DNA Mutation Search" if mode == "dna" else "A* Search Graph"
    ax.set_title(
        f"{title_prefix}:  {start} \u2192 {goal}   |   "
        f"Path length: {result.path_length}   |   "
        f"Nodes explored: {result.nodes_explored}",
        fontsize=14, fontweight="bold", pad=20,
    )
    ax.axis("off")

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#2196F3",
               markersize=12, label="Start"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#F44336",
               markersize=12, label="Goal"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#4CAF50",
               markersize=12, label="Optimal path"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#FF9800",
               markersize=12, label="Frontier (open set)"),
    ]
    if mode == "dna":
        for base, color in _NUC_COLORS.items():
            legend_elements.append(
                Line2D([0], [0], marker="o", color="w", markerfacecolor=color,
                       markersize=10, label=f"Base {base}"),
            )
    else:
        legend_elements.append(
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#E0E0E0",
                   markersize=12, label="Explored"),
        )
    ax.legend(handles=legend_elements, loc="lower left", fontsize=10,
              frameon=True, fancybox=True, shadow=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved search graph -> {output_path}")
