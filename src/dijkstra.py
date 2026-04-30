
import heapq
import math
 
# algorithme de Dijkstra avec un tas binaire (heapq)
# on cherche les plus courts chemins depuis un noeud source
 
def dijkstra(g, src, dst=None):
    # au départ toutes les distances sont infinies
    dist = [math.inf] * g.n
    dist[src] = 0.0
 
    # pour compter les operations 
    nb_extractions = 0
    nb_relaxations = 0
 
    # le tas contient des tuples (distance, noeud)
    # on commence avec juste le noeud source à distance 0
    tas = [(0.0, src)]
 
    while tas:
        # on extrait le noeud avec la plus petite distance
        d, u = heapq.heappop(tas)
        nb_extractions += 1
 
        # si on a déjà trouvé mieux pour ce noeud on skip
        if d > dist[u]:
            continue
 
        # si on a atteint la destination on arrête
        if dst is not None and u == dst:
            break
 
        # on regarde tous les voisins de u
        for v, w in g.neighbors(u):
            nouvelle_dist = dist[u] + w
            # si on trouve un chemin plus court on met à jour
            if nouvelle_dist < dist[v]:
                dist[v] = nouvelle_dist
                nb_relaxations += 1
                heapq.heappush(tas, (nouvelle_dist, v))
 
    stats = {"extractions": nb_extractions, "relaxations": nb_relaxations}
    return dist, stats
 
 
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from src.graph import Graph
 
    # petit test rapide
    g = Graph(4)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 2)
    g.add_edge(1, 3, 3)
    g.build()
 
    dist, stats = dijkstra(g, src=0)
    print("distances depuis 0 :", dist)
    print("stats :", stats)
