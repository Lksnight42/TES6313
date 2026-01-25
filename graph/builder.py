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

    for rid, r in routes.items():
        if rid not in route_scores:
            continue

        score = route_scores[rid]
        cost = score_to_cost(score)

        graph.add_edge(
            r["from"],
            {
                "to": r["to"],
                "route_id": rid,
                "score": score,
                "cost": cost,
                "service": r["service"],
            },
        )

    return graph



