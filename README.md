# Partie B — A* et ALT

## Fichier principal

`src/astar_alt.py`

---

## Ce que contient ce fichier

### 1. A* (A-star)

A* est une amélioration de Dijkstra qui utilise une **heuristique** pour guider la recherche vers la destination. On explore moins de nœuds, donc les requêtes sont plus rapides.

L'heuristique utilisée est la **distance euclidienne** entre le nœud courant et la destination, divisée par une vitesse max. Elle est admissible : elle ne surestime jamais le vrai coût.

### 2. ALT (A* + Landmarks)

ALT améliore encore A* en utilisant des **landmarks** (points repères). Après un prétraitement, on obtient une heuristique plus informative :

```
h(v, t) = max sur l : max(d(l,t) - d(l,v), d(v,l) - d(t,l))
```

Le prétraitement lance des Dijkstra complets depuis chaque landmark sur le graphe normal et le graphe inversé.

---

## Utilisation

### A*

```python
from src.graph import Graph
from src.astar_alt import astar

g = Graph(4)
g.add_edge(0, 1, 1)
g.add_edge(1, 3, 3)
g.build()
g.coord = {0: (0,0), 1: (1,0), 3: (1,1)}

dist, stats = astar(g, src=0, dst=3)
print(dist)   # distance du plus court chemin
print(stats)  # {'extractions': ..., 'relaxations': ...}
```

### ALT

```python
from src.astar_alt import pretraitement_alt, alt

# prétraitement (à faire une seule fois)
landmarks = [0, 3]
dist_depuis, dist_vers = pretraitement_alt(g, landmarks)

# requête
dist, stats = alt(g, src=0, dst=3,
                  landmarks=landmarks,
                  dist_depuis=dist_depuis,
                  dist_vers=dist_vers)
```

---

## Paramètres

| Paramètre | Description |
|-----------|-------------|
| `g` | Graphe CSR (classe Graph de `graph.py`) |
| `src` | Nœud source |
| `dst` | Nœud destination |
| `landmarks` | Liste d'indices de nœuds repères |
| `dist_depuis` | Table de distances depuis les landmarks |
| `dist_vers` | Table de distances vers les landmarks |

---

## Ce que retournent les fonctions

- `dist` : float — distance du plus court chemin (`math.inf` si pas de chemin)
- `stats` : dict — `{'extractions': int, 'relaxations': int}`

---

## Résultats observés (petit graphe test, 4 nœuds)

| Algo | Distance | Extractions | Relaxations |
|------|----------|-------------|-------------|
| Dijkstra | 4.0 | 4 | 4 |
| A* | 4.0 | 3 | 4 |
| ALT (k=2) | 4.0 | 3 | 4 |

A* et ALT donnent la **même distance** que Dijkstra ✅  
A* et ALT explorent **moins de nœuds** que Dijkstra ✅

---

## Validation

Tous les algos retournent la même distance que Dijkstra sur l'ensemble des requêtes de test.

```bash
python3 -c "
from src.graph import Graph
from src.dijkstra import dijkstra
from src.astar_alt import astar, pretraitement_alt, alt

g = Graph(4)
g.add_edge(0, 1, 1)
g.add_edge(1, 2, 2)
g.add_edge(1, 3, 3)
g.add_edge(0, 3, 10)
g.build()
g.coord = {0: (0,0), 1: (1,0), 2: (2,0), 3: (1,1)}

landmarks = [0, 3]
dist_depuis, dist_vers = pretraitement_alt(g, landmarks)

dist_dijk, _ = dijkstra(g, src=0, dst=3)
dist_astar, _ = astar(g, src=0, dst=3)
dist_alt, _   = alt(g, 0, 3, landmarks, dist_depuis, dist_vers)

print('Correct :', dist_dijk[3] == dist_astar == dist_alt)
"
```# Projet-SDA