
# Représentation du graphe en CSR 
# On stocke les arêtes dans 3 tableaux contigus 
# que les listes d'adjacence classiques
 
class Graph:
 
    def __init__(self, n):
        # n = nombre de noeuds
        self.n = n
        # liste temporaire des arêtes avant de construire le CSR
        self.aretes = []
        # coordonnées (x, y) de chaque noeud, utile pour A*
        self.coord = {}
 
    def add_edge(self, u, v, w):
        self.aretes.append((u, v, w))
 
    def set_coord(self, noeud, x, y):
        self.coord[noeud] = (x, y)
 
    def build(self):
        # étape 1 : compter combien de voisins a chaque noeud
        n = self.n
        nb_voisins = [0] * n
        for u, v, w in self.aretes:
            nb_voisins[u] += 1
 
        # étape 2 : calculer les debuts
        # debut[i] = index de début des voisins du noeud i dans self.voisins
        self.debut = [0] * (n + 1)
        for i in range(n):
            self.debut[i + 1] = self.debut[i] + nb_voisins[i]
 
        # étape 3 : remplir voisins et poids
        m = len(self.aretes)
        self.voisins = [0] * m
        self.poids = [0.0] * m
 
        # curseur = copie de debut pour savoir où écrire pour chaque noeud
        curseur = self.debut[:]
        for u, v, w in self.aretes:
            idx = curseur[u]
            self.voisins[idx] = v
            self.poids[idx] = w
            curseur[u] += 1
 
        # on vide aretes pour libérer la mémoire
        self.aretes = []
 
    def neighbors(self, u):
        # retourne la liste des (voisin, poids) du noeud u
        d = self.debut[u]
        f = self.debut[u + 1]
        res = []
        for i in range(d, f):
            res.append((self.voisins[i], self.poids[i]))
        return res
 
    def reverse(self):
        # construit le graphe inversé (toutes les arêtes retournées)
        # utilisé par la personne B pour le prétraitement ALT
        g_inv = Graph(self.n)
        g_inv.coord = self.coord
        for u in range(self.n):
            for v, w in self.neighbors(u):
                g_inv.add_edge(v, u, w)
        g_inv.build()
        return g_inv
if __name__ == "__main__":
    # petit graphe de test
    g = Graph(4)
    g.add_edge(0, 1, 5)
    g.add_edge(1, 2, 3)
    g.add_edge(1, 3, 7)
    g.build()

    print("nb noeuds :", g.n)
    print("voisins :", g.voisins)
    print("poids   :", g.poids)
    print("debut   :", g.debut)

    print("\nvoisins du noeud 1 :", g.neighbors(1))
    print("voisins du noeud 0 :", g.neighbors(0))
    print("voisins du noeud 2 :", g.neighbors(2))