from typing import List, Dict, Any
from data.map.index import ID_TO_NAME


class Path:
    def __init__(self, edges):
        self.edges = edges or []

    @property
    def nodes(self):
        if not self.edges:
            return []
        nodes = [self.edges[0]["route_id"]]
        for e in self.edges:
            nodes.append(e["to"])
        return nodes

    @property
    def total_base_time(self):
        return sum(e["base_time"] for e in self.edges)

    @property
    def total_base_cost(self):
        return sum(e["base_cost"] for e in self.edges)

    @property
    def total_distance(self):
        return sum(e["distance"] for e in self.edges)

    @property
    def total_score(self):
        return sum(e["score"] for e in self.edges)

    @property
    def total_cost(self):
        return sum(e["decision_cost"] for e in self.edges)

    def prompt(self):
        prompt = []
        for e in self.edges:
            prompt.append(
                f"{e['from']} -> {e['to']} | "
                f"{e['route_id']} ({e['service']}) "
                f"cost={fmt(e['decision_cost'])}  score={fmt(e['score'])}"
            )
        return prompt

    def __repr__(self):
        return (
            f"<Path steps={len(self.edges)}"
            f"score={self.total_score} "
            f"cost={self.total_cost}>"
        )


def fmt(x):
    return f"{float(x):.2f}"


def evaluate_path(edges):
    total_time = 0
    total_cost = 0
    transfer_count = 0
    score_sum = 0

    prev_service = None

    for e in edges:
        total_time += e.get("base_time", 0)
        total_cost += e.get("base_cost", 0)
        score_sum += e.get("score", 0)

        if prev_service is not None and e["service"] != prev_service:
            transfer_count += 1

        prev_service = e["service"]

    return {
        "total_time": total_time,
        "total_cost": total_cost,
        "transfers": transfer_count,
        "raw_score": score_sum,
    }


def final_score(path_metrics, preference="fastest"):
    if preference == "fastest":
        return (
            -path_metrics["total_time"]
            - path_metrics["transfers"] * 5
        )

    elif preference == "cheapest":
        return (
            -path_metrics["total_cost"]
            - path_metrics["transfers"] * 3
        )
    else:
        return path_metrics["raw_score"]


def edge_to_user_step(edge: Dict[str, Any], prev_service: str | None):
    service = edge.get("service", "unknown")
    kind = edge.get("kind", "travel")

    is_transfer = (
        prev_service is not None
        and service != prev_service
        and kind == "transfer"
    )

    if is_transfer:
        action = f"Transfer to {service}"
    else:
        action = f"Ride {service}"

    return {
        "from": edge["from"],
        "to": edge["to"],
        "service": service,
        "kind": kind,

        "time_min": round(edge.get("base_time", 0.0), 2),
        "cost_rm": round(edge.get("base_cost", 0.0), 2),

        "action": action,
    }


def build_user_route_result(
    path_edges: List[Dict[str, Any]],
    path_metrics: Dict[str, Any],
    start: str | int,
    end: str | int,
    preference: str,
):

    steps = []
    prev_service = None

    for edge in path_edges:
        step = edge_to_user_step(edge, prev_service)
        steps.append(step)
        prev_service = edge.get("service")


    return {
        "summary": {
            "start_name": ID_TO_NAME[int(start)],
            "end_name": ID_TO_NAME[int(end)],
            "start": start,
            "end": end,
            "total_time_min": round(path_metrics["total_time"], 2),
            "total_cost_rm": round(path_metrics["total_cost"], 2),
            "transfers": path_metrics["transfers"],
            "preference": preference,
        },
        "steps": steps,
    }


def print_user_route_result(result: Dict[str, Any]):

    s = result["summary"]
    steps = result["steps"]

    print("=" * 50)
    print("🚏 ROUTE RECOMMENDATION")
    print("=" * 50)

    print(f"From        : {s['start_name']}")
    print(f"To          : {s['end_name']}")
    print(f"Preference  : {s['preference']}")
    print()
    print(f"⏱  Total time   : {s['total_time_min']:.2f} min")
    print(f"💰 Total cost   : RM {s['total_cost_rm']:.2f}")
    print(f"🔁 Transfers    : {s['transfers']}")
    print()

    print("-" * 50)
    print("🧭 ROUTE STEPS")
    print("-" * 50)

    for i, step in enumerate(steps, 1):
        print(
            f"{i:>2}. {step['from']} → {step['to']} | "
            f"{step['action']:<15} | "
            f"{step['time_min']:>5.2f} min | "
            f"RM {step['cost_rm']:>4.2f}"
        )

    print("=" * 50)


def explain_route(result, all_paths_metrics=None):

    s = result["summary"]
    reasons = []

    if s["preference"] == "fastest":
        reasons.append(
            f"This route minimizes total travel time ({s['total_time_min']:.2f} minutes)."
        )

    if s["transfers"] == 0:
        reasons.append("No transfers are required, ensuring a smoother journey.")
    elif s["transfers"] == 1:
        reasons.append("Only one transfer is required, balancing speed and convenience.")
    else:
        reasons.append(f"Transfers are limited to {s['transfers']} times.")

    reasons.append(
        f"Estimated total cost is RM {s['total_cost_rm']:.2f}."
    )

    return {
        "title": "Why this route is recommended",
        "reasons": reasons
    }


def build_user_advise_result(path_rank, path, start, end, preference):

    edges = path["edges"]
    metrics = path["metrics"]

    return {
        "rank": path_rank,
        "summary": {
            "from": start,
            "to": end,
            "preference": preference,
            "total_time_min": round(metrics["total_time"], 2),
            "total_cost_rm": round(metrics["total_cost"], 2),
            "transfers": metrics["transfers"],
            "final_score": round(path["final_score"], 2)
        },
        "steps": [
            {
                "from": e["from"],
                "to": e["to"],
                "service": e["service"],
                "kind": e["kind"],
                "time": round(e.get("base_time", 0), 2),
                "cost": round(e.get("base_cost", 0), 2),
            }
            for e in edges
        ]
    }


def explain_top_k(results):
    if len(results) == 1:
        return[{
            "rank":1,
            "why": [
                "This is the only feasible route between the selected"
            ]
        }]
    explanations = []

    best = results[0]["summary"]

    for r in results:
        s = r["summary"]
        reasons = []

        if s["total_time_min"] == best["total_time_min"]:
            reasons.append("Fastest travel time among alternatives")
        elif s["total_time_min"] > best["total_time_min"]:
            reasons.append(
                f"{s['total_time_min'] - best['total_time_min']:.2f} minutes slower than fastest"
            )

        if s["transfers"] < best["transfers"]:
            reasons.append("Fewer transfers than other options")
        elif s["transfers"] > best["transfers"]:
            reasons.append(f"Requires {s['transfers']} transfers")

        reasons.append(
            f"Estimated cost RM {s['total_cost_rm']:.2f}"
        )

        explanations.append({
            "rank": r["rank"],
            "why": reasons
        })

    return explanations


def print_top_k_explanations(explanations):
    print("\n🏆 TOP RECOMMENDATIONS")
    print("=" * 50)

    for e in explanations:
        print(f"#{e['rank']}")
        for reason in e["why"]:
            print(f"  • {reason}")
        print("-" * 30)


