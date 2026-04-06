#!/usr/bin/env python3
"""Word Ladder & DNA Mutation Pathway Solver — CLI entry point.

Usage:
    python main.py --start cold --goal warm
    python main.py --start cold --goal warm --visualize
    python main.py --compare
    python main.py --mode dna --start ATCG --goal GCTA
    python main.py --mode dna --start ATCG --goal GCTA --visualize
    python main.py --mode dna --compare
"""

import argparse
import sys

from solver.astar import astar
from solver.bfs import bfs
from solver.dijkstra import dijkstra
from solver.graph import WordGraph


def print_result(result, mode="word"):
    """Pretty-print a search result to the console."""
    label = "DNA Mutation Pathway" if mode == "dna" else "Word Ladder"
    print(f"\n{'-' * 55}")
    print(f"  Mode:           {label}")
    print(f"  Algorithm:      {result.algorithm}")
    if result.path:
        print(f"  Path:           {' -> '.join(result.path)}")
        print(f"  Path length:    {result.path_length} steps")
    else:
        print("  Path:           No path found!")
    print(f"  Nodes explored: {result.nodes_explored}")
    print(f"  Time:           {result.execution_time:.4f}s")
    print(f"{'-' * 55}")


def cmd_solve(args, graph):
    """Solve a single word ladder / DNA mutation and optionally generate visualizations."""
    mode = args.mode

    if mode == "dna":
        start, goal = args.start.upper(), args.goal.upper()
        valid_bases = set("ATGC")
        if not all(c in valid_bases for c in start):
            print(f"Error: '{start}' contains invalid DNA bases. Use only A, T, G, C.")
            sys.exit(1)
        if not all(c in valid_bases for c in goal):
            print(f"Error: '{goal}' contains invalid DNA bases. Use only A, T, G, C.")
            sys.exit(1)
    else:
        start, goal = args.start.lower(), args.goal.lower()

    # Validation
    if len(start) != len(goal):
        print(f"Error: Sequences must be the same length. "
              f"'{start}' has {len(start)} characters, '{goal}' has {len(goal)}.")
        sys.exit(1)
    if not graph.has_word(start):
        print(f"Error: '{start}' is not in the {'sequence space' if mode == 'dna' else 'dictionary'}.")
        sys.exit(1)
    if not graph.has_word(goal):
        print(f"Error: '{goal}' is not in the {'sequence space' if mode == 'dna' else 'dictionary'}.")
        sys.exit(1)

    # Run selected algorithm(s)
    algorithms = {"astar": ("A*", astar), "bfs": ("BFS", bfs), "dijkstra": ("Dijkstra", dijkstra)}

    if args.algorithm == "all":
        for name, fn in algorithms.values():
            result = fn(graph, start, goal)
            print_result(result, mode)
    else:
        name, fn = algorithms[args.algorithm]
        result = fn(graph, start, goal)
        print_result(result, mode)

    # Visualizations (always run A* for these, since they need expansion history)
    if args.visualize:
        astar_result = astar(graph, start, goal) if args.algorithm != "astar" else result

        from visualizer.search_graph import plot_search_graph
        from visualizer.step_viewer import plot_step_viewer
        from visualizer.heuristic_plot import plot_heuristic_accuracy
        from visualizer.comparison import plot_comparison

        prefix = "dna_" if mode == "dna" else ""

        print("\nGenerating visualizations...")
        plot_search_graph(astar_result, graph,
                          output_path=f"output/{prefix}search_graph.png", mode=mode)
        plot_step_viewer(astar_result, graph,
                         output_path=f"output/{prefix}astar_steps.png", mode=mode)
        plot_heuristic_accuracy(goal, graph,
                                output_path=f"output/{prefix}heuristic_accuracy.png", mode=mode)
        plot_comparison(graph,
                        output_path=f"output/{prefix}comparison_chart.png", mode=mode)
        print(f"\nAll visualizations saved to output/ (prefix: '{prefix}')")


def cmd_compare(args, graph):
    """Run algorithm comparison across preset pairs."""
    from visualizer.comparison import plot_comparison, DEFAULT_WORD_PAIRS, DNA_WORD_PAIRS

    mode = args.mode
    prefix = "dna_" if mode == "dna" else ""
    pairs = DNA_WORD_PAIRS if mode == "dna" else DEFAULT_WORD_PAIRS
    label = "DNA mutation" if mode == "dna" else "algorithm"

    print(f"Running {label} comparison...")
    print(f"Pairs: {', '.join(f'{s}->{g}' for s, g in pairs)}\n")

    results = plot_comparison(
        graph, word_pairs=pairs,
        output_path=f"output/{prefix}comparison_chart.png", mode=mode,
    )

    # Print table
    current_pair = None
    for r in results:
        if r["pair"] != current_pair:
            current_pair = r["pair"]
            print(f"\n  {current_pair}:")
        print(f"    {r['algorithm']:>8s}  |  explored: {r['nodes_explored']:>4d}  |  "
              f"path length: {r['path_length']}  |  {r['path']}")


def main():
    parser = argparse.ArgumentParser(
        description="Word Ladder & DNA Mutation Pathway Solver using A*, BFS, and Dijkstra",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py --start cold --goal warm\n"
               "  python main.py --start cold --goal warm --visualize\n"
               "  python main.py --start cold --goal warm --algorithm all\n"
               "  python main.py --compare\n"
               "\n"
               "DNA mode:\n"
               "  python main.py --mode dna --start ATCG --goal GCTA\n"
               "  python main.py --mode dna --start ATCG --goal GCTA --visualize\n"
               "  python main.py --mode dna --start ATCG --goal GCTA --algorithm all\n"
               "  python main.py --mode dna --compare\n",
    )
    parser.add_argument("-s", "--start", type=str, help="Start word/sequence")
    parser.add_argument("-g", "--goal", type=str, help="Goal word/sequence")
    parser.add_argument("-a", "--algorithm", type=str, default="astar",
                        choices=["astar", "bfs", "dijkstra", "all"],
                        help="Algorithm to use (default: astar)")
    parser.add_argument("-v", "--visualize", action="store_true",
                        help="Generate all visualizations")
    parser.add_argument("-c", "--compare", action="store_true",
                        help="Run algorithm comparison on preset pairs")
    parser.add_argument("-d", "--dictionary", type=str,
                        default="data/dictionary.txt",
                        help="Path to dictionary file (word mode only)")
    parser.add_argument("-m", "--mode", type=str, default="word",
                        choices=["word", "dna"],
                        help="Mode: 'word' for word ladders, 'dna' for DNA mutations (default: word)")
    parser.add_argument("--seq-length", type=int, default=4,
                        help="DNA sequence length (default: 4, DNA mode only)")

    args = parser.parse_args()

    # Build graph based on mode
    if args.mode == "dna":
        seq_len = args.seq_length
        print(f"Generating DNA sequence space (length={seq_len})...")
        graph = WordGraph(mode="dna", seq_length=seq_len)
        print(f"Generated {len(graph.words)} sequences "
              f"({seq_len}-base: {len(graph.words_by_length.get(seq_len, set()))})")
    else:
        print(f"Loading dictionary from {args.dictionary}...")
        graph = WordGraph(args.dictionary)
        print(f"Loaded {len(graph.words)} words "
              f"({', '.join(f'{k}-letter: {len(v)}' for k, v in sorted(graph.words_by_length.items()))})")

    if args.compare:
        cmd_compare(args, graph)
    elif args.start and args.goal:
        cmd_solve(args, graph)
    else:
        parser.print_help()
        print("\nError: Provide --start and --goal, or use --compare.")
        sys.exit(1)


if __name__ == "__main__":
    main()
