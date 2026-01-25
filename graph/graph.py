
from collections import defaultdict


class Graph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_edge(self, from_node, edge):
        self.adj[from_node].append(edge)

    def neighbors(self, node):
        return self.adj.get(node, [])

    def __repr(self):
        return f"<Graph nodes={len(self.adj)}"

    def print_graph(self):

        print("=== GRAPH DUMP ===")
        for from_node, edges in self.adj.items():
            print(f"{from_node}:")
            for e in edges:
                print(
                    f"  -> {e['to']} "
                    f"(route={e['route_id']}, "
                    f"service={e['service']}, "
                    f"score={e['score']}, "
                    f"cost={e['cost']})"
                )


def reachable(graph, start):
    from collections import deque
    seen = set([start])
    q = deque([start])

    while q:
        u = q.popleft()
        for e in graph.neighbors(u):
            v = e["to"]
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen



