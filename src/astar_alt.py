import heapq
import math


def heuristique(g, v, t):
    """
    Distance euclidienne entre v et t.
    Admissible car elle ne surestime jamais le vrai coût.
    """
    x1, y1 = g.coord[v]
    x2, y2 = g.coord[t]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def astar(g, src, dst):
    """
    A* de src vers dst sur le graphe g.
    Retourne (distance, stats) comme dijkstra.
    """
    dist = [math.inf] * g.n
    dist[src] = 0.0

    nb_extractions = 0
    nb_relaxations = 0

    # tas : (f = dist_reelle + heuristique, dist_reelle, noeud)
    h_src = heuristique(g, src, dst)
    tas = [(h_src, 0.0, src)]

    while tas:
        f, d, u = heapq.heappop(tas)
        nb_extractions += 1

        # entrée périmée
        if d > dist[u]:
            continue

        # destination atteinte
        if u == dst:
            break

        for v, w in g.neighbors(u):
            nouvelle_dist = dist[u] + w
            if nouvelle_dist < dist[v]:
                dist[v] = nouvelle_dist
                nb_relaxations += 1
                h_v = heuristique(g, v, dst)
                heapq.heappush(tas, (nouvelle_dist + h_v, nouvelle_dist, v))

    stats = {"extractions": nb_extractions, "relaxations": nb_relaxations}
    return dist[dst], stats
def pretraitement_alt(g, landmarks):
    """
    Pour chaque landmark, calcule les distances depuis et vers lui.
    Retourne deux dicts : dist_depuis et dist_vers.
    """
    g_inv = g.reverse()
    dist_depuis = {}
    dist_vers = {}

    for l in landmarks:
        # distances depuis le landmark (graphe normal)
        dist_depuis[l] = _dijkstra_complet(g, l)
        # distances vers le landmark (= depuis l sur graphe inversé)
        dist_vers[l] = _dijkstra_complet(g_inv, l)

    return dist_depuis, dist_vers


def _dijkstra_complet(g, src):
    """Dijkstra depuis src, retourne toutes les distances."""
    dist = [math.inf] * g.n
    dist[src] = 0.0
    tas = [(0.0, src)]
    while tas:
        d, u = heapq.heappop(tas)
        if d > dist[u]:
            continue
        for v, w in g.neighbors(u):
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(tas, (nd, v))
    return dist


def _heuristique_alt(v, t, landmarks, dist_depuis, dist_vers):
    """h(v,t) = max sur les landmarks de |d(l,t) - d(l,v)|"""
    h = 0.0
    for l in landmarks:
        val1 = dist_depuis[l][t] - dist_depuis[l][v]
        val2 = dist_vers[l][v] - dist_vers[l][t]
        h = max(h, val1, val2)
    return h


def alt(g, src, dst, landmarks, dist_depuis, dist_vers):
    """
    Requête ALT de src vers dst.
    Retourne (distance, stats) comme dijkstra.
    """
    dist = [math.inf] * g.n
    dist[src] = 0.0

    nb_extractions = 0
    nb_relaxations = 0

    h_src = _heuristique_alt(src, dst, landmarks, dist_depuis, dist_vers)
    tas = [(h_src, 0.0, src)]

    while tas:
        f, d, u = heapq.heappop(tas)
        nb_extractions += 1

        if d > dist[u]:
            continue

        if u == dst:
            break

        for v, w in g.neighbors(u):
            nouvelle_dist = dist[u] + w
            if nouvelle_dist < dist[v]:
                dist[v] = nouvelle_dist
                nb_relaxations += 1
                h_v = _heuristique_alt(v, dst, landmarks, dist_depuis, dist_vers)
                heapq.heappush(tas, (nouvelle_dist + h_v, nouvelle_dist, v))

    stats = {"extractions": nb_extractions, "relaxations": nb_relaxations}
    return dist[dst], stats