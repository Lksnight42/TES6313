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
                "base-time": fact["base-time"],
                "base-cost": fact["base-cost"],
                "distance": fact["distance"],
                "kind": fact["kind"] if "kind" in fact else "travel",
            }

    graph = Graph()

    edges_by_segment = {}

    for rid, r in routes.items():
        if rid not in route_scores:
            continue

        frm = r["from"]
        to = r["to"]
        service = r["service"]
        kind = r["kind"]

        score = route_scores[rid]
        decision_cost = score_to_cost(score)

        edge_data = {
            "from": frm,
            "to": to,
            "route_id": rid,

            "score": score,
            "decision_cost": decision_cost,

            "base_time": r["base-time"],
            "base_cost": r["base-cost"],
            "distance": r["distance"],

            "service": service,
            "kind": kind
        }

        if kind == "transfer":
            graph.add_edge(frm, edge_data)
            continue
        key = (frm, to)

        edges_by_segment.setdefault(key, []).append(edge_data)

    for (frm, to), edges in edges_by_segment.items():
        transfer_edges = [e for e in edges if e["kind"] == "transfer"]

        travel_edges = [e for e in edges if e["kind"] != "transfer"]

        concrete = [e for e in travel_edges if e["service"] != "none"]

        if concrete:
            final_edges = concrete
        else:
            final_edges = travel_edges

        for edge in transfer_edges + final_edges:
            graph.add_edge(frm, edge)

    return graph


