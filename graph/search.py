import heapq
import itertools


def dijkstra(graph, start, end):

    counter = itertools.count()
    pq = [(0, start, [])]  # cost, node, path
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node == end:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for edge in graph.neighbors(node):
            heapq.heappush(
                pq,
                (
                    cost + edge["cost"],
                    next(counter),
                    edge["to"],
                    path + [edge],
                )
            )
        return None, float("inf")




