import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

LOCATION_FILE = BASE / "map" / "nodes.json"

NAME_TO_ID = {}
ID_TO_NAME = {}
VALID_LOCATION_IDS = set()


def load_locations():
    global NAME_TO_ID, ID_TO_NAME, VALID_LOCATION_IDS

    with open(LOCATION_FILE, "r", encoding="utf-8") as f:
        locations = json.load(f)["locations"]

    for loc in locations:
        loc_id = int(loc["id"])
        name = loc["name"]

        NAME_TO_ID[name] = loc_id
        ID_TO_NAME[loc_id] = name
        VALID_LOCATION_IDS.add(loc_id)
