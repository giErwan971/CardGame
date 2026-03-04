# Rami – Jeu de Rami en Python

> Un jeu complet de Rami, en solo contre une IA, développé en Python avec interface graphique Pygame.

---

## 🎮 Présentation

Ce projet propose une implémentation numérique du célèbre jeu de cartes **Rami**. Jouez contre un bot et profitez d’une interface graphique dynamique, immersive et fidèle à l’esprit du jeu traditionnel !

---

## ✨ Fonctionnalités principales

- **Mode solo joueur contre IA** : profitez d'un adversaire virtuel disposant d'une stratégie avancée.
- **Interface graphique ergonomique et réactive** (Pygame) : manipulation intuitive des cartes à la souris, boutons animés, effets visuels et feedback immédiat.
- **Gestion complète du jeu** : pioche, défausse, constitution et validation de combinaisons (brelans, suites, groupes).
- **Système d'annulation/retour** : Un CTRL + Z pour annuler le dernier coup, la touche espace pour annuler le tour complet.
- **Affichage graphique du tapis, des cartes en main & des actions**.
- **Animations et illustrations enrichies** pour une expérience utilisateur optimale.
- **Deck de cartes double standard** géré en POO, classes bien structurées.

---

## 🧑‍💻 Structure du projet

Le code est organisé en plusieurs modules pour faciliter la maintenance et l'évolution :

    ├── Assets/ # Ressources graphiques (images, cartes, fonds...)
    ├── Script/ # Les différants programmes python qui gère le jeu.
        \── Main.py # Boucle principale & gestion générale
        ├── Rami.py # Mécanismes du jeu & règles de gestion
        ├── Bot.py # Intelligence artificielle de l'adversaire
        ├── Cards.py # Objets carte et deck, gestion des états
        ├── UI.py # Interface utilisateur (boutons, événements)
        ├── utils.py # Fonctions utilitaires diverses


### Rôles principaux :

- **Main.py** : Lance le jeu, initialise tous les éléments, gère l'écran & boucle des événements.
- **Rami.py** : Logique métiers, application des règles, manipulations de base (poser/prendre/valider des cartes, annulation...).
- **Bot.py** : Implémentation d'un bot jouant contre vous, basé sur des fonctions d’évaluation complexe.
- **Cards.py** : Gestion fine de la pioche, représentation orientée objet des cartes, méthodes de rendu graphique.
- **UI.py** : Gestion centralisée des boutons interactifs, effets de survol, clic, redimensionnement.
- **utils.py** : Outils annexes utiles au projet.

---

## 🤖 Intelligence Artificielle

L’adversaire IA repose sur une intelligence dynamique, prenant en compte :
- la polyvalence des cartes pour former des suites/brelans,
- la position optimale dans une séquence,
- la pénalité pour doublons,
- le calcul du nombre de poses optimales envisageables,
- une évaluation pondérée sur 100 pour chaque carte possible.

Le bot sélectionne ses actions (piocher, poser, défausser) en fonction d’une analyse combinatoire, testant l’impact de chaque mouvement sur ses opportunités de victoire. Vous pouvez donc vraiment progresser en l’affrontant !

---

## 🖥️ Prérequis & Installation

- **Python 3.8+** recommandé
- **pygame** (`pip install pygame`)
- Système Windows/Linux/Mac (prévu pour affichages Full HD et adaptation automatique)
- Tous les assets graphiques nécessaires doivent être présents dans le dossier `assets/` à la racine

### Lancement

- ouvrez visual studio code
- selectionner File/Open Folder ( Ctrl + k suivie de Ctrl + o)
- selectionner le dossier CardGame
- lancer le script Main.py dans le dossier script

*Le jeu se lance en plein écran pour une meilleure immersion.*

---

## 🚀 Utilisation

- **Souris** : navigation, drag & drop des cartes, clic sur les boutons (pioche, défausse, terminer, règles…)
- **Clavier** :
  - `Echap` = quitter la partie
  - `Espace` = reset du tour
  - `Ctrl + Z` = annuler l’action précédente

- **Déroulement** :
  1. Distribuez les cartes (13 en main, le reste forme la pioche/défausse).
  2. À votre tour : piochez ou prenez la carte de la défausse.
  3. Constituez des combinaisons valides sur le tapis.
  4. Défaussez une carte si vous n'avais rien posé pour finir votre tour.
  5. L’IA joue alors son propre tour.
  6. Continuez jusqu’à avoir jouer toutes vos cartes.

---

## 🧩 Stratégie & Algorithme du Bot

- **Polyvalence combinatoire** : analyse en profondeur de la capacité d’une carte à s’intégrer dans plusieurs groupes/suites.
- **Simulation d’actions** : le bot anticipe la réussite potentielle de chaque mouvement.
- **Pénalité-doublons** : le bot évite de conserver des cartes redondantes nuisibles à ses chances de victoires.
- **Positionnement** : il donne la priorité aux positions avantageuses dans les séquences.

*(Voir `Bot.py` pour plus de détails algorithmiques !)*

---

## 🎨 Interface graphique & Commandes

- Boutons interactifs : Jouer, Équipe, Règles, Pioche, Défausse.
- Illustration des cartes : images originales pour chaque carte, effets de surbrillance selon l’action possible.
- Animations : animations fluides dans le menu principale.
- Affichage de victoire/défaite à la fin de la partie.

---

## 🙋 Crédits

Développement & design : **SUPERS GEEKS**

Licence : Usage libre non-commercial

Technos : [Python](https://www.python.org/), [pygame](https://www.pygame.org/)

---

## 📄 Pour aller plus loin

- Améliorer l'IA avec apprentissage automatique ou simulations Monte-Carlo
- Ajout de plein de petites animation dans le menu de jeu pour le rendre plus vivant.

---

*Bon jeu, affrontez l’IA et devenez un Maître du Rami ! 🎲🃏*
