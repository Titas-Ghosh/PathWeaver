"""Breadth-First Search implementation for the word ladder problem."""

import time
from collections import deque

from solver import SearchResult
from solver.graph import WordGraph


def bfs(graph: WordGraph, start: str, goal: str) -> SearchResult:
    """Find shortest word ladder path using BFS.

    BFS guarantees the shortest path in an unweighted graph since it
    explores nodes level by level.
    """
    start, goal = start.strip(), goal.strip()
    t0 = time.perf_counter()

    # Edge case: same word
    if start == goal:
        return SearchResult(
            path=[start], nodes_explored=0, path_length=0,
            algorithm="BFS", execution_time=time.perf_counter() - t0,
        )

    visited: set[str] = {start}
    parent: dict[str, str | None] = {start: None}
    queue: deque[str] = deque([start])
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        for neighbor in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            parent[neighbor] = current
            if neighbor == goal:
                # Reconstruct path
                path = []
                node: str | None = goal
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return SearchResult(
                    path=path, nodes_explored=nodes_explored,
                    path_length=len(path) - 1, algorithm="BFS",
                    execution_time=time.perf_counter() - t0,
                )
            visited.add(neighbor)
            queue.append(neighbor)

    return SearchResult(
        path=None, nodes_explored=nodes_explored, path_length=0,
        algorithm="BFS", execution_time=time.perf_counter() - t0,
    )
