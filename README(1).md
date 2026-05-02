# Projet-SDA

# Partie C : Benchmarks & Contraction Hierarchies (CH)

## Objectif

Cette partie du projet couvre :

* la mise en place d’un framework de benchmark,
* l’implémentation de **Contraction Hierarchies (CH)**,
* la validation des résultats par comparaison avec Dijkstra.

---

## Fichiers

```text
src/
├── benchmark.py
├── metrics.py
├── ch.py
├── run_benchmarks.py
```

---

## Benchmark

Le framework benchmark permet de mesurer :

* temps moyen par requête
* p50 / p95
* débit (requêtes/s)
* nombre moyen d’extractions
* nombre moyen de relaxations

Les résultats sont exportés en CSV :

* `dijkstra_results.csv`
* `ch_results.csv`

---

## Contraction Hierarchies (CH)

L’implémentation suit 3 étapes :

### 1. Ordre de contraction

Les nœuds sont triés par degré croissant.

### 2. Contraction

Lorsqu’un nœud est contracté, des **shortcuts** sont ajoutés pour préserver les plus courts chemins.

### 3. Requête

Les requêtes utilisent le graphe augmenté (graphe original + shortcuts).

---

## Validation

Chaque résultat CH est comparé à Dijkstra :

```text
distance_CH == distance_Dijkstra
```

Validation correcte sur toutes les requêtes testées.

---

## Résultats

### Dijkstra

* Temps moyen : `0.00235 s`
* Débit : `425 req/s`

### CH

* Temps moyen : `0.00129 s`
* Débit : `775 req/s`

### Gain

* Accélération : **~1.8x**
* Réduction des nœuds explorés : **~44%**

---

## Difficultés rencontrées

* perte de certains chemins avec les arêtes montantes,
* ajout excessif de shortcuts,
* erreurs d’implémentation (boucles et relaxations).

Solutions :

* simplification de la requête CH,
* contrôle des shortcuts,
* correction de la logique du parcours.

---

## Exécution

Depuis le dossier `src` :

```bash
python3 run_benchmarks.py
```

Cela génère :

```text
dijkstra_results.csv
ch_results.csv
```

---

## Conclusion

L’implémentation CH permet de réduire le temps de réponse et le nombre de nœuds explorés, au prix d’un prétraitement supplémentaire.
