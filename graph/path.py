class Path:
    def __init__(self, edges):
        self.edges = edges or []

    @property
    def nodes(self):
        if not self.edges:
            return []
        nodes = [self.edges[0]["route_id"]]
        for e in self.edges:
            nodes.append(e["to"])
        return nodes

    @property
    def total_score(self):
        return sum(e["score"] for e in self.edges)

    @property
    def total_cost(self):
        return sum(e["cost"] for e in self.edges)

    def prompt(self):
        prompt = []
        for e in self.edges:
            prompt.append(
                f"{e['route_id']} ({e['service']}) score={e['score']}"
            )
        return prompt

    def __repr__(self):
        return (
            f"<Path steps={len(self.edges)}"
            f"score={self.total_score} "
            f"cost={self.total_cost}>"
        )




