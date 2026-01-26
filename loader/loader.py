import clips
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def load_location(env):
    with open(BASE / "data" / "map" / "nodes.json") as f:
        locations = json.load(f)["locations"]
    for loc in locations:
        fact = f'''
        (location
            (id {loc["id"]})
            (name "{loc["name"]}")
            (level {loc["level"]})
            (parent "{loc["parent"]}")
        )
        '''
        env.assert_string(fact)


def load_edge(env):
    with open(BASE / "data" / "map" / "edges_test.json") as f:
        edges = json.load(f)["edges"]
    for edg in edges:
        transports = " ".join(edg["allowed_transport"])
        fact = f'''
        (edge
            (from {edg["from"]})
            (to {edg["to"]})
            (allowed-transport {transports})
            (distance {edg["distance"]})
        )
        '''
        env.assert_string(fact)


def load_line(env):
    with open(BASE / "data" / "map" / "mrt" / "lines.json") as f:
        lines = json.load(f)["lines"]
    for line in lines:
        mode = line["mode"]
        service = line["service"]
        stations = line["stations"]

        for i in range(len(stations) - 1):
            a = stations[i]
            b = stations[i + 1]

            fact = f'''
            (line-segment
              (mode {mode})
              (service {service})
              (from {a})
              (to {b}))
            '''
            env.assert_string(fact)

            fact_rev = f'''
            (line-segment
              (mode {mode})
              (service {service})
              (from {b})
              (to {a}))
            '''
            env.assert_string(fact_rev)


def load_transfer(env):
    with open(BASE / "data" / "map" / "mrt" / "transfer.json") as f:
        transfers = json.load(f)["transfers"]
    for tfr in transfers:
        fact = f'''
        (transfer
            (location {tfr["location"]})
            (from-mode {tfr["from-mode"]})
            (from-service {tfr["from-service"]})
            (to-mode {tfr["to-mode"]})
            (to-service {tfr["to-service"]})
            (time {tfr["time"]})
        )
        '''
        env.assert_string(fact)


def load_env():
    env = clips.Environment()

    env.load(str(BASE / "core" / "expert" / "templates.clp"))
    env.load(str(BASE / "core" / "expert" / "facts.clp"))
    env.load(str(BASE / "core" / "expert" / "log.clp"))
    env.load(str(BASE / "core" / "expert" / "rules.clp"))
    env.load(str(BASE / "core" / "expert" / "test-scenarios.clp"))

    return env
