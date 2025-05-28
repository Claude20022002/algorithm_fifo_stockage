# Algorithm FIFO - Gestion de la Mémoire

Ce projet est une simulation interactive de l'algorithme FIFO (First In, First Out) pour la gestion de la mémoire virtuelle. Il permet de visualiser le comportement de l'algorithme FIFO lors de la gestion des pages en mémoire.

## Fonctionnalités

-   Interface graphique interactive avec CustomTkinter
-   Visualisation en temps réel de la gestion des pages
-   Mode étape par étape pour suivre l'évolution de la mémoire
-   Graphique d'évolution des défauts de page
-   Simulation personnalisable avec séquence de pages et nombre de cadres

## Prérequis

```bash
pip install customtkinter matplotlib
```

## Utilisation

1. Lancez l'application :

```bash
python script.py
```

2. Dans l'interface :

    - Entrez une séquence de pages (ex: 7,0,1,2,0,3,0,4)
    - Spécifiez le nombre de cadres mémoire
    - Cliquez sur "Démarrer la simulation"

3. Contrôles disponibles :
    - "Étape suivante" : Visualisez la simulation pas à pas
    - "Afficher graphique" : Consultez l'évolution des défauts de page

## Explication du Code

### Structure Principale

-   `fifo_simulation(pages, nb_frames)` : Fonction principale qui implémente l'algorithme FIFO

    -   Gère la mémoire et la file d'attente
    -   Retourne les étapes de simulation et le nombre de défauts

-   `FifoApp` : Classe principale de l'interface graphique
    -   Gère l'interface utilisateur
    -   Contrôle la simulation et l'affichage

### Composants Clés

1. **Simulation FIFO**

    - Utilise une liste pour la mémoire
    - Maintient une file d'attente pour l'ordre d'arrivée
    - Détecte les défauts de page

2. **Interface Graphique**

    - Visualisation des cadres mémoire
    - Indication des défauts de page (rouge)
    - Affichage des pages en mémoire (vert)

3. **Visualisation**
    - Mode étape par étape
    - Graphique d'évolution des défauts
    - Statut en temps réel

## Exemple de Séquence

Pour tester l'algorithme, utilisez des séquences comme :

-   7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1
-   1,2,3,4,1,2,5,1,2,3,4,5

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

-   Signaler des bugs
-   Proposer des améliorations
-   Ajouter de nouvelles fonctionnalités

## Licence

Ce projet est sous licence MIT.
