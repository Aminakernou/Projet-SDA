import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.dijkstra import dijkstra
from src.generator import generate_grid, generate_queries


# test 1 : graphe simple dont on connait la reponse a la main
def test_simple():
    # graphe :  0 --1--> 1 --2--> 2
    #                    |
    #                    3
    #                    v
    #                    3
    g = Graph(4)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 2)
    g.add_edge(1, 3, 3)
    g.build()

    dist, stats = dijkstra(g, src=0)

    assert dist[0] == 0,   "dist[0] doit etre 0"
    assert dist[1] == 1,   "dist[1] doit etre 1"
    assert dist[2] == 3,   "dist[2] doit etre 3"
    assert dist[3] == 4,   "dist[3] doit etre 4"
    print("test_simple OK  stats =", stats)


# test 2 : un noeud isolé doit avoir une distance infinie
def test_noeud_isole():
    g = Graph(4)
    g.add_edge(0, 1, 5)
    g.add_edge(1, 2, 3)
    # noeud 3 est isolé, personne ne pointe vers lui
    g.build()

    dist, _ = dijkstra(g, src=0)
    assert dist[3] == math.inf, "dist[3] doit etre inf"
    print("test_noeud_isole OK")


# test 3 : le graphe inversé doit retourner toutes les aretes
def test_reverse():
    # graphe original : 0 -> 1 (poids 2), 1 -> 2 (poids 3)
    # graphe inversé  : 2 -> 1 (poids 3), 1 -> 0 (poids 2)
    g = Graph(3)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, 3)
    g.build()

    g_inv = g.reverse()
    dist, _ = dijkstra(g_inv, src=2)

    assert dist[2] == 0, "dist[2] doit etre 0"
    assert dist[1] == 3, "dist[1] doit etre 3"
    assert dist[0] == 5, "dist[0] doit etre 5"
    print("test_reverse OK")


# test 4 : dijkstra avec dst doit donner la meme distance que sans dst
def test_arret_anticipe():
    g = generate_grid(20, 20, seed=0)
    src = 0
    dst = 399

    dist_complet, _ = dijkstra(g, src)
    dist_anticipe, _ = dijkstra(g, src, dst)

    assert math.isclose(dist_complet[dst], dist_anticipe[dst]), \
        "les deux versions doivent donner la meme distance"
    print("test_arret_anticipe OK  distance =", round(dist_complet[dst], 2))


# test 5 : les requetes generees doivent etre valides
def test_requetes():
    g = generate_grid(50, 50)
    qs = generate_queries(g, nb=30)

    assert len(qs) == 30, "on doit avoir 30 requetes"
    for s, t in qs:
        assert 0 <= s < g.n, "src invalide"
        assert 0 <= t < g.n, "dst invalide"
    print("test_requetes OK  nb =", len(qs))


if __name__ == "__main__":
    print("=" * 40)
    print("   Tests partie A")
    print("=" * 40)
    test_simple()
    test_noeud_isole()
    test_reverse()
    test_arret_anticipe()
    test_requetes()
    print("=" * 40)
    print("   Tous les tests passent !")
    print("=" * 40)



def test_inaccessible():
    g = Graph(4)
    g.add_edge(0, 1, 5)
    g.add_edge(1, 2, 3)
    g.build()
    dist, _ = dijkstra(g, 0)
    assert dist[3] == math.inf
    print("test_inaccessible OK")


def test_reverse():
    g = Graph(3)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, 3)
    g.build()
    gr = g.reverse()
    dist, _ = dijkstra(gr, 2)
    assert dist[1] == 3
    assert dist[0] == 5
    print("test_reverse OK")


def test_dst():
    g = generate_grid(20, 20, seed=0)
    d1, _ = dijkstra(g, 0)
    d2, _ = dijkstra(g, 0, dst=399)
    assert math.isclose(d1[399], d2[399])
    print("test_dst OK  distance=", round(d1[399], 2))


def test_queries():
    g = generate_grid(50, 50)
    qs = generate_queries(g, nb=30)
    assert len(qs) == 30
    for s, t in qs:
        assert 0 <= s < g.n and 0 <= t < g.n
    print("test_queries OK  nb=", len(qs))


if __name__ == "__main__":
    test_simple()
    test_inaccessible()
    test_reverse()
    test_dst()
    test_queries()
    print("\nTous les tests passent !")