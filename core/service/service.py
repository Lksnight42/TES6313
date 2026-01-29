import loader.loader as loader
from core.context.adapter import assert_user_context
from core.context.model import UserContext
from graph.builder import build_graph
from graph.search import dijkstra
from graph.path import evaluate_path
from graph.path import build_user_route_result
def find_route(ctx: UserContext):

    env = loader.load_env()
    env.reset()

    loader.load_location(env)
    loader.load_edge(env)
    loader.load_line(env)
    loader.load_transfer(env)

    assert_user_context(env, ctx)

    env.run()

    graph = build_graph(env)
    edges, _ = dijkstra(
        graph,
        ctx.start_location,
        ctx.end_location
    )

    if not edges:
        raise RuntimeError("No route found")

    metrics = evaluate_path(edges)

    return build_user_route_result(
        edges,
        metrics,
        ctx.start_location,
        ctx.end_location,
        ctx.preference
    )
