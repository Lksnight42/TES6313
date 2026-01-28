import json
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

MIN_DISTANCE = 0.2
MAX_DISTANCE = 5.0

MAX_TIME = 10.0
MAX_COST = 1.0

INPUT_FILE = str(BASE / "data" / "map" / "edges.json")
OUTPUT_FILE = str(BASE / "data" / "map" / "edges_updated.json")


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

edge_list = data["edges"]

for edge in edge_list:
    old_distance = edge.get("distance")

    edge["distance"] = round(
        random.uniform(MIN_DISTANCE, MAX_DISTANCE), 2
    )

    edge["base_time"] = round(
        random.uniform(1.0, MAX_TIME), 2
    )

    edge["base_cost"] = round(
        random.uniform(0.1, MAX_COST), 2
    )

    print(
        f"edge {edge['from']}→{edge['to']} | "
        f"distance: {old_distance}→{edge['distance']}, "
        f"time: {edge['base_time']}min, "
        f"cost: {edge['base_cost']}"
    )


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✔ Updated {len(edge_list)} edges with base_time and base_cost")

