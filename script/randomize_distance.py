import json
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

MIN_DISTANCE = 0.2
MAX_DISTANCE = 5.0

INPUT_FILE = str(BASE / "data" / "map" / "edges.json")
OUTPUT_FILE = str(BASE / "data" / "map" / "edges_updated.json")


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

edge_list = data["edges"]

for edge in edge_list:
    old = edge["distance"]
    edge["distance"] = round(
        random.uniform(MIN_DISTANCE, MAX_DISTANCE), 2
    )
    print(f"distance: {old} → {edge['distance']}")


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✔ Updated distance for {len(data)} edges")

