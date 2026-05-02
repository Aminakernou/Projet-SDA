import heapq
import math


class ContractionHierarchies:

    def __init__(self, graph):
        self.graph = graph
        self.rank = {}
        self.shortcuts = []

    # ordre de contraction : degré croissant
    def compute_order(self):
        nodes = list(range(self.graph.n))

        nodes.sort(
            key=lambda u: len(self.graph.neighbors(u))
        )

        for i, node in enumerate(nodes):
            self.rank[node] = i

        return nodes

    # trouver les prédécesseurs
    def predecessors(self, u):
        preds = []

        for x in range(self.graph.n):
            for v, w in self.graph.neighbors(x):
                if v == u:
                    preds.append((x, w))

        return preds

    # contracter un noeud
    def contract_node(self, u):
        preds = self.predecessors(u)
        succs = self.graph.neighbors(u)

        for p, wp in preds:
            for s, ws in succs:

                if p == s:
                    continue

                shortcut_weight = wp + ws

                best_existing = float("inf")

                for v, w in self.graph.neighbors(p):
                    if v == s:
                        best_existing = min(best_existing, w)

                if best_existing <= shortcut_weight:
                    continue

                # ajouter le shortcut
                self.graph.add_edge(
                    p,
                    s,
                    shortcut_weight
                )

                self.shortcuts.append(
                    (p, s, shortcut_weight)
                )

    # preprocessing
    def preprocess(self):
        order = self.compute_order()

        for u in order[: self.graph.n // 2]:
            self.contract_node(u)

        self.graph.build()

    # requête CH
    def query(self, src, dst):

        dist = [math.inf] * self.graph.n
        dist[src] = 0

        pq = [(0, src)]

        nb_extractions = 0
        nb_relaxations = 0

        while pq:
            d, u = heapq.heappop(pq)
            nb_extractions += 1

            if d > dist[u]:
                continue

            if u == dst:
                break

            for v, w in self.graph.neighbors(u):

                nd = d + w

                if nd < dist[v]:
                    dist[v] = nd
                    nb_relaxations += 1
                    heapq.heappush(
                        pq,
                        (nd, v)
                    )

        stats = {
            "extractions": nb_extractions,
            "relaxations": nb_relaxations
        }

        return dist, stats