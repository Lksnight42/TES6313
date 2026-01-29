import loader.loader as loader
from core.context.adapter import assert_user_context
from core.context.model import UserContext
from graph.builder import build_graph
from graph.search import dijkstra, find_top_k_path, path_signature
from graph.path import (
    evaluate_path, 
    build_user_route_result,
    explain_top_k,
    build_user_advise_result,
)

from dataclasses import replace

def find_route(ctx: UserContext, k: int = 3):

    env = loader.load_env()
    env.reset()

    loader.load_location(env)
    loader.load_edge(env)
    loader.load_line(env)
    loader.load_transfer(env)

    assert_user_context(env, ctx)

    env.run()

    graph = build_graph(env)
    best_edges, _ = dijkstra(
        graph,
        ctx.start_location,
        ctx.end_location
    )

    if not best_edges:
        raise RuntimeError("No route found")

    metrics = evaluate_path(best_edges)

    best_result = build_user_route_result(
        best_edges,
        metrics,
        ctx.start_location,
        ctx.end_location,
        ctx.preference
    )

    topk_paths = find_top_k_path(
        graph, 
        ctx.start_location,
        ctx.end_location,
        k,
        ctx.preference
    )

    topk_results = [
        build_user_advise_result(
            i + 1,
            p,
            ctx.start_location,
            ctx.end_location,
            ctx.preference
        )
        for i, p in enumerate(topk_paths)
    ]

    explanations = explain_top_k(topk_results)

    return {
        "best": best_result,
        "alternatives": explanations
    }
