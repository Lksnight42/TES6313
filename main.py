import loader.loader as loader
from graph.builder import build_graph
from graph.search import dijkstra
from graph.path import evaluate_path, final_score
from graph.path import build_user_route_result, print_user_route_result, explain_route


def inject_user_context(env):
    env.assert_string("""
    (user-context
      (user-id u1)
      (start-location 1)
      (start-location 10)
      (preference fastest)
      (avoid transfer)
      (flexibility medium))
    """)


def path_algorithm(env):
    """
    For future algorithm
    """

    return None


def get_user_input():

    return None


def main():
    print("=== SYSTEM START ")

    while True:
        ctx = get_user_input()

        if ctx is None:
            break

        env = loader.load_env()
        env.reset()

        print("=== Loading static knowledge ===")

        loader.load_location(env)
        loader.load_edge(env)
        loader.load_line(env)
        loader.load_transfer(env)

        print("Running initial inference...")
        env.run()

        graph = build_graph(env)

        path_edges, cost = dijkstra(
            graph,
            start=ctx.start_location,
            end=ctx.end_location
        )

        if not path_edges:
            print("No route found.")
            continue

        metrics = evaluate_path(path_edges)
        score = final_score(metrics, "cheapest")

        result = build_user_route_result(
            path_edges=path_edges,
            path_metrics=metrics,
            start=ctx.start_location,
            end=ctx.end_location,
            preference="cheapest"
        )

        print_user_route_result(result)


if __name__ == "__main__":
    main()

