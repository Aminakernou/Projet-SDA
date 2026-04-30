import random
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.graph import Graph

# on génère un faux réseau routier en grille
# rows x cols noeuds, poids aléatoires entre 1 et 10

def generate_grid(rows, cols, seed=42):
    rng = random.Random(seed)
    n = rows * cols
    g = Graph(n)

    for i in range(rows):
        for j in range(cols):
            # id du noeud courant
            noeud = i * cols + j

            # on stocke les coordonnées pour A* plus tard
            g.set_coord(noeud, x=j, y=i)

            # arête vers le noeud à droite
            if j + 1 < cols:
                w = rng.uniform(1, 10)
                g.add_edge(noeud, noeud + 1, w)
                g.add_edge(noeud + 1, noeud, w)

            # arête vers le noeud en bas
            if i + 1 < rows:
                w = rng.uniform(1, 10)
                g.add_edge(noeud, noeud + cols, w)
                g.add_edge(noeud + cols, noeud, w)

    g.build()
    return g


# on génère un lot de requêtes (src, dst) reproductible
# mélange de requêtes courtes, moyennes et longues

def generate_queries(g, nb=100, seed=42):
    rng = random.Random(seed)
    n = g.n
    requetes = []

    # requêtes courtes : src et dst dans le premier quart
    for _ in range(nb // 3):
        s = rng.randint(0, n // 4)
        t = rng.randint(0, n // 4)
        requetes.append((s, t))

    # requêtes moyennes : src et dst dans la première moitié
    for _ in range(nb // 3):
        s = rng.randint(0, n // 2)
        t = rng.randint(0, n // 2)
        requetes.append((s, t))

    # requêtes longues : src dans le premier quart, dst dans le dernier quart
    for _ in range(nb - 2 * (nb // 3)):
        s = rng.randint(0, n // 4)
        t = rng.randint(3 * n // 4, n - 1)
        requetes.append((s, t))

    return requetes


if __name__ == "__main__":
    # test rapide
    g = generate_grid(5, 5)
    print("nb noeuds :", g.n)
    print("nb aretes :", len(g.voisins))
    print("coord noeud 0 :", g.coord[0])
    print("coord noeud 24 :", g.coord[24])

    qs = generate_queries(g, nb=9)
    print("\nrequetes generees :", qs)