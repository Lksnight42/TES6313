import loader.loader as loader
from log.logger import setup_logging
from log.logger import dump_logs

from graph.builder import build_graph
from graph.search import dijkstra, find_top_k_path
from graph.path import evaluate_path, final_score
from data.map.index import load_locations


from graph.path import (
    build_user_route_result,
    print_user_route_result,
    print_top_k_explanations,
    explain_top_k,
    build_user_advise_result,
)
logger = setup_logging()
load_locations()


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
# print("=== RUN CLIPS ===")
# for fact in env.facts():
#     if fact.template.name == "route-metric":
#         print("metric exists")
#         print(fact)
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

# graph.print_graph()


path_edges, cost = dijkstra(
    graph,
    start=79, #ctx.start_location
    end=9, #ctx.end_location
)

# if path_edges:
#     path = Path(path_edges)
#     print(path)
#     print("Path Result:")
#     for line in path.prompt():
#         print(line)
# else:
#     print("No path found")

# if not path_edges:
#     print("No path found")

metrics = evaluate_path(path_edges)
score = final_score(metrics, "cheapest")

result = build_user_route_result(
    path_edges=path_edges,
    path_metrics=metrics,
    start="79",
    end="9",
    preference="cheapest"
)
# print("=== PATH METRICS ===")
# print(metrics)
# print("Final score:", score)

print_user_route_result(result)

paths = find_top_k_path(
    graph,
    79,
    9,
    3,
    "cheapest"
)

results = [
    build_user_advise_result(
        i + 1,
        p,
        79,
        9,
        "cheapest"
    )
    for i, p in enumerate(paths)

]

explainations = explain_top_k(results)
print_top_k_explanations(explainations)




del env


# for r in env.rules():
#     print(r.name)
