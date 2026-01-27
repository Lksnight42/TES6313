import loader.loader as loader
from log.logger import setup_logging
from log.logger import dump_logs

from graph.builder import build_graph
from graph.search import dijkstra
from graph.path import Path
from graph.graph import reachable


logger = setup_logging()


env = loader.load_env()

print("=== RUN CLIPS ===")
env.reset()

loader.load_location(env)
loader.load_edge(env)
loader.load_line(env)
loader.load_transfer(env)


env.run()

print("=== RUN CLIPS ===")
dump_logs(env, min_level="DEBUG")

loader.load_edge
print("=== RUN CLIPS ===")
for fact in env.facts():
    if fact.template.name == "route-metric":
        print("metric exists")
        print(fact)
# print(fact)


# routes = [
#     r for r in env.facts()
#     if r.template.name == "route" and r["mode"] == "mrt"
# ]
#
# for r in routes:
#     print(r)

graph = build_graph(env)

# reach = reachable(graph, 80)
# print("Reachable from start:", reach)
# print("End in reachable?", 80 in reach)

graph.print_graph()


path_edges, cost = dijkstra(
    graph,
    start=1,
    end=90,
)

if path_edges:
    path = Path(path_edges)
    print(path)
    print("Path Result:")
    for line in path.prompt():
        print(line)
else:
    print("No path found")


del env


# for r in env.rules():
#     print(r.name)
