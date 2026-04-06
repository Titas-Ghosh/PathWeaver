"""Visualization 3 — Step-by-step A* expansion panels."""

import math
import os

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

from solver import SearchResult
from solver.graph import WordGraph

# Nucleotide colors for DNA mode
_NUC_COLORS = {"A": "#00BCD4", "T": "#E91E63", "G": "#4CAF50", "C": "#FF9800"}


def plot_step_viewer(
    result: SearchResult,
    graph: WordGraph,
    output_path: str = "output/astar_steps.png",
    max_steps: int = 6,
    mode: str = "word",
) -> None:
    """Generate a multi-panel figure showing A* expanding step by step.

    Each panel shows: current node being expanded, open set, closed set,
    and the f/g/h values for the current node.
    """
    if not result.expansion_history:
        print("No expansion history available -- skipping step viewer.")
        return

    sns.set_theme(style="whitegrid")

    history = result.expansion_history
    num_steps = min(max_steps, len(history))

    # Select evenly spaced steps (always include first and last)
    if num_steps <= 1:
        indices = [0]
    elif num_steps >= len(history):
        indices = list(range(len(history)))
    else:
        indices = [round(i * (len(history) - 1) / (num_steps - 1))
                    for i in range(num_steps)]

    selected_steps = [history[i] for i in indices]
    num_steps = len(selected_steps)

    # Grid layout
    cols = min(3, num_steps)
    rows = math.ceil(num_steps / cols)

    # Build full subgraph from all nodes seen across all selected steps
    all_nodes: set[str] = set()
    for step in selected_steps:
        all_nodes.update(step["closed_set"])
        all_nodes.update(step["open_set"])
        all_nodes.add(step["current"])

    G_full = nx.Graph()
    G_full.add_nodes_from(all_nodes)
    for node in all_nodes:
        for neighbor in graph.get_neighbors(node):
            if neighbor in all_nodes:
                G_full.add_edge(node, neighbor)

    # Compute layout once for consistency across panels
    pos = nx.kamada_kawai_layout(G_full)

    path_set = set(result.path) if result.path else set()
    start = result.path[0] if result.path else None
    goal = result.path[-1] if result.path else None

    fig, axes = plt.subplots(rows, cols, figsize=(7 * cols, 6 * rows))
    if num_steps == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for idx, (step, ax) in enumerate(zip(selected_steps, axes)):
        closed = set(step["closed_set"])
        open_set = set(step["open_set"])
        current = step["current"]
        step_nodes = closed | open_set | {current}

        # Build subgraph for this step
        G_step = G_full.subgraph(step_nodes).copy()

        # Node colors
        node_colors = []
        node_sizes = []
        for node in G_step.nodes():
            if node == current:
                node_colors.append("#F44336")  # Red -- currently expanding
                node_sizes.append(650)
            elif node == start:
                node_colors.append("#2196F3")  # Blue
                node_sizes.append(550)
            elif node == goal and node in step_nodes:
                node_colors.append("#9C27B0")  # Purple
                node_sizes.append(550)
            elif node in open_set:
                if mode == "dna":
                    node_colors.append(_NUC_COLORS.get(node[0], "#FF9800"))
                else:
                    node_colors.append("#FF9800")  # Orange -- frontier
                node_sizes.append(400)
            elif node in closed:
                if mode == "dna":
                    node_colors.append(_NUC_COLORS.get(node[0], "#B0BEC5"))
                else:
                    node_colors.append("#B0BEC5")  # Gray -- explored
                node_sizes.append(400)
            else:
                node_colors.append("#ECEFF1")
                node_sizes.append(300)

        # Filter positions to nodes in this step
        step_pos = {n: pos[n] for n in G_step.nodes() if n in pos}

        nx.draw_networkx_edges(G_step, step_pos, alpha=0.2,
                               edge_color="#BDBDBD", ax=ax)
        nx.draw_networkx_nodes(G_step, step_pos, node_color=node_colors,
                               node_size=node_sizes, edgecolors="#424242",
                               linewidths=0.7, ax=ax)
        font_size = 5 if mode == "dna" else 6
        nx.draw_networkx_labels(G_step, step_pos, font_size=font_size,
                                font_weight="bold", ax=ax)

        ax.set_title(
            f"Step {step['step']}: expanding '{current}'\n"
            f"f={step['f']}  g={step['g']}  h={step['h']}  |  "
            f"open={len(open_set)}  closed={len(closed)}",
            fontsize=10, fontweight="bold", pad=8,
        )
        ax.axis("off")

    # Hide unused axes
    for idx in range(num_steps, len(axes)):
        axes[idx].axis("off")
        axes[idx].set_visible(False)

    title_prefix = "A* DNA Mutation \u2014 Step-by-Step" if mode == "dna" else "A* Step-by-Step Expansion"
    fig.suptitle(
        f"{title_prefix}:  {start} \u2192 {goal}",
        fontsize=16, fontweight="bold", y=1.02,
    )
    fig.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved step viewer -> {output_path}")
