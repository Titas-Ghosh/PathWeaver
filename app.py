"""Flask web application for the Word Ladder & DNA Mutation Pathway Solver."""

import os
import time

import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template, request, jsonify, send_from_directory

from solver.graph import WordGraph
from solver.astar import astar
from solver.bfs import bfs
from solver.dijkstra import dijkstra

app = Flask(__name__)

_word_graph = None
_dna_graphs: dict[int, WordGraph] = {}

ALGORITHMS = {
    "astar": ("A*", astar),
    "bfs": ("BFS", bfs),
    "dijkstra": ("Dijkstra", dijkstra),
}


def get_word_graph() -> WordGraph:
    global _word_graph
    if _word_graph is None:
        _word_graph = WordGraph("data/dictionary.txt")
    return _word_graph


def get_dna_graph(length: int) -> WordGraph:
    if length not in _dna_graphs:
        _dna_graphs[length] = WordGraph(mode="dna", seq_length=length)
    return _dna_graphs[length]


def _graph(mode, seq_length):
    return get_dna_graph(seq_length) if mode == "dna" else get_word_graph()


def _norm(text, mode):
    return text.strip().upper() if mode == "dna" else text.strip().lower()


@app.route("/")
def index():
    wg = get_word_graph()
    return render_template("index.html", word_count=len(wg.words))


@app.route("/api/solve", methods=["POST"])
def api_solve():
    data = request.json
    mode = data.get("mode", "word")
    start = _norm(data.get("start", ""), mode)
    goal = _norm(data.get("goal", ""), mode)
    algorithm = data.get("algorithm", "astar")
    seq_length = int(data.get("seq_length", 4))

    if mode == "dna":
        if not all(c in "ATGC" for c in start):
            return jsonify({"error": f"'{start}' contains invalid bases. Use A, T, G, C only."}), 400
        if not all(c in "ATGC" for c in goal):
            return jsonify({"error": f"'{goal}' contains invalid bases. Use A, T, G, C only."}), 400

    graph = _graph(mode, seq_length)

    if not start or not goal:
        return jsonify({"error": "Start and goal are required."}), 400
    if len(start) != len(goal):
        return jsonify({"error": f"Length mismatch: {len(start)} vs {len(goal)}"}), 400

    label = "sequence space" if mode == "dna" else "dictionary"
    if not graph.has_word(start):
        return jsonify({"error": f"'{start}' not found in {label}"}), 400
    if not graph.has_word(goal):
        return jsonify({"error": f"'{goal}' not found in {label}"}), 400

    results = []
    items = ALGORITHMS.items() if algorithm == "all" else [(algorithm, ALGORITHMS[algorithm])]
    for _, (name, fn) in items:
        r = fn(graph, start, goal)
        results.append({
            "algorithm": r.algorithm,
            "path": r.path,
            "path_length": r.path_length,
            "nodes_explored": r.nodes_explored,
            "execution_time": round(r.execution_time, 6),
        })

    return jsonify({"results": results, "mode": mode, "graph_size": len(graph.words)})


@app.route("/api/visualize", methods=["POST"])
def api_visualize():
    data = request.json
    mode = data.get("mode", "word")
    start = _norm(data.get("start", ""), mode)
    goal = _norm(data.get("goal", ""), mode)
    seq_length = int(data.get("seq_length", 4))
    graph = _graph(mode, seq_length)

    result = astar(graph, start, goal)
    if result.path is None:
        return jsonify({"error": "No path found - cannot generate visualizations."}), 400

    from visualizer.search_graph import plot_search_graph
    from visualizer.step_viewer import plot_step_viewer
    from visualizer.heuristic_plot import plot_heuristic_accuracy
    from visualizer.comparison import plot_comparison

    prefix = "dna_" if mode == "dna" else ""
    os.makedirs("output", exist_ok=True)

    plot_search_graph(result, graph, f"output/{prefix}search_graph.png", mode=mode)
    plot_step_viewer(result, graph, f"output/{prefix}astar_steps.png", mode=mode)
    plot_heuristic_accuracy(goal, graph, f"output/{prefix}heuristic_accuracy.png", mode=mode)
    plot_comparison(graph, output_path=f"output/{prefix}comparison_chart.png", mode=mode)

    t = int(time.time())
    return jsonify({"images": {
        "search_graph": f"/output/{prefix}search_graph.png?t={t}",
        "comparison_chart": f"/output/{prefix}comparison_chart.png?t={t}",
        "astar_steps": f"/output/{prefix}astar_steps.png?t={t}",
        "heuristic_accuracy": f"/output/{prefix}heuristic_accuracy.png?t={t}",
    }})


@app.route("/api/compare", methods=["POST"])
def api_compare():
    data = request.json
    mode = data.get("mode", "word")
    seq_length = int(data.get("seq_length", 4))
    graph = _graph(mode, seq_length)

    from visualizer.comparison import plot_comparison, DEFAULT_WORD_PAIRS, DNA_WORD_PAIRS

    prefix = "dna_" if mode == "dna" else ""
    pairs = DNA_WORD_PAIRS if mode == "dna" else DEFAULT_WORD_PAIRS
    os.makedirs("output", exist_ok=True)

    results = plot_comparison(
        graph, word_pairs=pairs,
        output_path=f"output/{prefix}comparison_chart.png", mode=mode,
    )

    t = int(time.time())
    return jsonify({
        "results": results,
        "image": f"/output/{prefix}comparison_chart.png?t={t}",
        "pairs": [list(p) for p in pairs],
    })


@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)


if __name__ == "__main__":
    print("Loading word dictionary...")
    get_word_graph()
    print(f"Loaded {len(get_word_graph().words)} words.")
    print("Starting server at http://localhost:5000")
    app.run(debug=True, port=5000, use_reloader=False)
