import heapq
import math


def dijkstra(graph, start, end):
    #
    dist = {start: 0}
    prev = {}   # node -> (prev_node, edge)

    pq = [(0, start)]

    while pq:
        cost, node = heapq.heappop(pq)

        if node == end:
            break

        if cost > dist.get(node, math.inf):
            continue

        for edge in graph.neighbors(node):
            nxt = edge["to"]
            new_cost = cost + edge["cost"]

            if new_cost < dist.get(nxt, math.inf):
                dist[nxt] = new_cost
                prev[nxt] = (node, edge)
                heapq.heappush(pq, (new_cost, nxt))

    if end not in prev and start != end:
        return None, math.inf

    path_edges = []
    cur = end
    while cur != start:
        pnode, edge = prev[cur]
        path_edges.append(edge)
        cur = pnode

    path_edges.reverse()
    return path_edges, dist[end]


