"""Dijkstra's algorithm implementation for the word ladder problem."""

import heapq
import time

from solver import SearchResult
from solver.graph import WordGraph


def dijkstra(graph: WordGraph, start: str, goal: str) -> SearchResult:
    """Find shortest word ladder path using Dijkstra's algorithm.

    All edges have uniform cost of 1, so this behaves similarly to BFS
    but uses a priority queue. Included for algorithm comparison.
    """
    start, goal = start.strip(), goal.strip()
    t0 = time.perf_counter()

    if start == goal:
        return SearchResult(
            path=[start], nodes_explored=0, path_length=0,
            algorithm="Dijkstra", execution_time=time.perf_counter() - t0,
        )

    dist: dict[str, int] = {start: 0}
    parent: dict[str, str | None] = {start: None}
    visited: set[str] = set()
    counter = 0  # Tiebreaker for heap stability
    heap: list[tuple[int, int, str]] = [(0, counter, start)]
    nodes_explored = 0

    while heap:
        cost, _, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if current == goal:
            path = []
            node: str | None = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return SearchResult(
                path=path, nodes_explored=nodes_explored,
                path_length=len(path) - 1, algorithm="Dijkstra",
                execution_time=time.perf_counter() - t0,
            )

        for neighbor in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            new_cost = cost + 1
            if new_cost < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_cost
                parent[neighbor] = current
                counter += 1
                heapq.heappush(heap, (new_cost, counter, neighbor))

    return SearchResult(
        path=None, nodes_explored=nodes_explored, path_length=0,
        algorithm="Dijkstra", execution_time=time.perf_counter() - t0,
    )
