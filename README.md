# Mini Project - Scénario 1 

Ce projet est un solveur de labyrinthe qui utilise différents algorithmes pour trouver le chemin le plus court dans un labyrinthe. Les labyrinthes sont lus à partir d'un fichier et affichés à l'aide d'une interface graphique. Inspiré par les découvertes de Márcio Himura sur les punitions sous le règne de Ramathibodi Ier, ce projet simule un scénario où un prisonnier doit trouver la sortie d'une pièce enflammée pour survivre.

## Structure du Projet

- `Graph.py`: Contient la classe `Graph` qui représente le labyrinthe sous forme de graphe et implémente divers algorithmes de recherche de chemin.
- `Labyrinth.py`: Contient la classe `Labyrinth` qui lit les labyrinthes à partir d'un fichier, les affiche et trouve le chemin le plus court en utilisant l'algorithme spécifié.
- `labyrinth.txt`: Contient les labyrinthes à résoudre.

## Utilisation

1. Exécutez le script `Labyrinth.py` pour démarrer l'interface graphique.
2. Sélectionnez un labyrinthe et un algorithme pour trouver et afficher le chemin le plus court.

## Algorithmes

Les algorithmes suivants sont implémentés :

- Algorithme de Dijkstra
- Algorithme A* avec heuristique de distance euclidienne
- Algorithme A* avec heuristique de détection de feu

## Exemple

Pour exécuter le projet, utilisez la commande suivante :

```sh
python Labyrinth.py
