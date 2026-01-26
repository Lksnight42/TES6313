from collections import defaultdict
from .graph import Graph


MAX_SCORE = 100


def score_to_cost(score: float) -> float:

    return max(0, MAX_SCORE - score)


def build_graph(env) -> Graph:

    route_scores = {}
    routes = {}

    # collect route evaluation
    for fact in env.facts():
        if fact.template.name == "route-evaluation":
            route_scores[fact["route-id"]] = fact["score"]

    # collect route
    for fact in env.facts():
        if fact.template.name == "route":
            routes[fact["id"]] = {
                "from": fact["start-location"],
                "to": fact["end-location"],
                "service": fact["service"],
            }

    graph = Graph()

    best_edges = {}

    for rid, r in routes.items():
        if rid not in route_scores:
            continue

        frm = r["from"]
        to = r["to"]
        service = r["service"]

        score = route_scores[rid]
        cost = score_to_cost(score)

        key = (frm, to)

        edge_data = {
            "from": frm,
            "to": to,
            "route_id": rid,
            "score": score,
            "cost": cost,
            "service": service,
        }

        if key not in best_edges:
            best_edges[key] = edge_data
            continue

        prev = best_edges[key]

        if score > prev["score"]:
            best_edges[key] = edge_data
        elif (
            score == prev["score"]
            and prev["service"] == "none"
            and service != "none"
        ):
            best_edges[key] = edge_data

    for edge in best_edges.values():
        graph.add_edge(
            edge["from"],
            {
                "from": edge["from"],
                "to": edge["to"],
                "route_id": edge["route_id"],
                "score": edge["score"],
                "cost": edge["cost"],
                "service": edge["service"],
            },
        )

    return graph


