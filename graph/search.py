import heapq
import math
import itertools
import copy
from graph.path import evaluate_path, final_score


def dijkstra(graph, start, end):
    TRANSFER_PENALTY = 5

    counter = itertools.count()
    start_state = (start, None)
    #
    dist = {start_state: 0}
    prev = {}   # node -> (prev_node, edge)

    pq = [(0, next(counter), start_state)]

    while pq:
        cost, _, (node, cur_service) = heapq.heappop(pq)

        if node == end:
            break

        if cost > dist.get((node, cur_service), math.inf):
            continue

        for edge in graph.neighbors(node):
            nxt = edge["to"]
            next_service = edge["service"]

            transfer_cost = 0
            if cur_service is not None and next_service != cur_service and cur_service != "none":
                transfer_cost = TRANSFER_PENALTY

            new_cost = (
                cost
                + edge["decision_cost"]
                + transfer_cost
            )

            next_state = (nxt, next_service)

            if new_cost < dist.get(next_state, math.inf):
                dist[next_state] = new_cost
                prev[next_state] = ((node, cur_service), edge)
                heapq.heappush(pq, (new_cost, next(counter), next_state))

    end_states = [
        s for s in dist
        if s[0] == end
    ]

    if not end_states:
        return None, math.inf

    best_end_state = min(end_states, key=lambda s: dist[s])

    path_edges = []
    cur_state = best_end_state
    while cur_state in prev:
        cur_state, edge = prev[cur_state]
        path_edges.append(edge)

    path_edges.reverse()
    return path_edges, dist[best_end_state]


def path_signature(edges):
    return tuple(
        (e["from"], e["to"], e["service"])
        for e in edges
    )

def find_top_k_path(graph, start, end, k, preference):
    paths = []
    penalties = {}
    seen_signatures = set()

    for i in range(k):
        g = graph.clone()

        for (frm, to, service), p in penalties.items():
            g.penalize_edge(frm, to, service, p)

        edges, _ = dijkstra(g, start, end)
        if not edges:
            break

        sig = path_signature(edges)
        if sig in seen_signatures:
            break

        seen_signatures.add(sig)

        metrics = evaluate_path(edges)
        score = final_score(metrics, preference)

        paths.append({
            "edges": edges,
            "metrics": metrics,
            "final_score": score
        })

        for e in edges:
            key = (e["from"], e["to"], e["service"])
            penalties[key] = penalties.get(key, 0) + 100

    return paths


