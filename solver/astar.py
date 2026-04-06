"""A* search algorithm implementation for the word ladder problem."""

import heapq
import time

from solver import SearchResult
from solver.graph import WordGraph
from solver.heuristics import hamming_distance


def astar(graph: WordGraph, start: str, goal: str) -> SearchResult:
    """Find shortest word ladder path using A* search with Hamming distance heuristic.

    A* combines the actual cost g(n) with a heuristic estimate h(n) to
    prioritize nodes most likely on the shortest path: f(n) = g(n) + h(n).

    The Hamming distance heuristic is admissible (never overestimates) because
    each differing character requires at least one transformation step.

    This implementation captures a full expansion history for step-by-step
    visualization of the algorithm's progress.
    """
    start, goal = start.strip(), goal.strip()
    t0 = time.perf_counter()

    if start == goal:
        return SearchResult(
            path=[start], nodes_explored=0, path_length=0,
            algorithm="A*", execution_time=time.perf_counter() - t0,
        )

    h_start = hamming_distance(start, goal)
    g_score: dict[str, int] = {start: 0}
    f_score: dict[str, int] = {start: h_start}
    parent: dict[str, str | None] = {start: None}

    open_set_hash: set[str] = {start}
    closed_set: set[str] = set()

    counter = 0  # Tiebreaker for heap stability
    heap: list[tuple[int, int, str]] = [(h_start, counter, start)]

    nodes_explored = 0
    expansion_history: list[dict] = []

    while heap:
        _, _, current = heapq.heappop(heap)

        # Skip if already processed (stale entry in heap)
        if current in closed_set:
            continue
        if current not in open_set_hash:
            continue

        open_set_hash.discard(current)
        closed_set.add(current)
        nodes_explored += 1

        current_g = g_score[current]
        current_h = hamming_distance(current, goal)
        current_f = current_g + current_h

        # Record expansion step for visualization
        neighbors_added: list[str] = []

        for neighbor in graph.get_neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_g = current_g + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                h = hamming_distance(neighbor, goal)
                f = tentative_g + h
                f_score[neighbor] = f
                parent[neighbor] = current
                if neighbor not in open_set_hash:
                    open_set_hash.add(neighbor)
                counter += 1
                heapq.heappush(heap, (f, counter, neighbor))
                neighbors_added.append(neighbor)

        expansion_history.append({
            "step": nodes_explored,
            "current": current,
            "g": current_g,
            "h": current_h,
            "f": current_f,
            "open_set": list(open_set_hash),
            "closed_set": list(closed_set),
            "neighbors_added": neighbors_added,
        })

        if current == goal:
            path = []
            node: str | None = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return SearchResult(
                path=path, nodes_explored=nodes_explored,
                path_length=len(path) - 1, algorithm="A*",
                execution_time=time.perf_counter() - t0,
                expansion_history=expansion_history,
            )

    return SearchResult(
        path=None, nodes_explored=nodes_explored, path_length=0,
        algorithm="A*", execution_time=time.perf_counter() - t0,
        expansion_history=expansion_history,
    )
