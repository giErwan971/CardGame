# 🎴 Rami - Jeu de Cartes en Python

## 📋 Résumé Exécutif

**CardGame** est une implémentation numérique complète du jeu de Rami, développée en Python avec une interface graphique avancée utilisant Pygame. Ce projet offre un système de jeu complet jouable en solo contre une Intelligence Artificielle sophistiquée, intégrant des mécaniques complexes de gameplay, une IA stratégique et une interface utilisateur intuitive.

---

## 🎯 Objectifs et Context Pédagogique

Ce projet a été développé pour démontrer :
- **L'architecture logicielle** : Organisation modulaire en objets (POO) et séparation des responsabilités
- **L'algorithme et la stratégie** : Implémentation d'une IA capable d'évaluer les coups optimaux
- **L'interface graphique** : Création d'une UI réactive avec Pygame et gestion des événements
- **La gestion d'état complexe** : Système de sauvegarde/annulation de coups pour rejeu
- **La gestion de projets** : Structuration professionnelle du code pour la maintenance

---

## 📊 Architecture du Projet

### Structure des fichiers

```
CardGame/
├── Assets/                 # Ressources graphiques
│   ├── Cards/             # Jeux de cartes graphiques (5 thèmes)
│   │   ├── Cute Cards/
│   │   ├── Darck Theme Cards/
│   │   ├── Default Cards/
│   │   ├── Golden Cards/
│   │   └── King's Cards/
│   └── MainMenu/          # Interface menu
├── Scripts/               # Code Python
│   ├── Main.py           # Boucle principale
│   ├── Rami.py           # Logique du jeu
│   ├── Bot.py            # Intelligence Artificielle
│   ├── Cards.py          # Gestion des cartes
│   ├── UI.py             # Interface utilisateur
│   ├── utils.py          # Fonctions utilitaires
│   └── TempEval.py       # Algorithmes d'évaluation avancés
├── README.md
├── LICENSE
└── presentation.md
```

---

## 🔧 Modules Principaux et Fonctionnalités

### 1. **Main.py** - Orchestrateur Principal
- **Initialisation Pygame** : Gestion de la résolution d'écran fullscreen avec adaptation dynamique
- **Gestion des ressources graphiques** : Chargement des images, tilemap des animations
- **Boucle principale** : Gestion des événements et mise à jour de l'écran
- **Animations** : Effets de survol sur les boutons (Play, Team, Rules)

**Points techniques clés** :
- Adaptation de la résolution pour tous les écrans
- Système de couches (UIScreen, CardsScreen, RuleScreen)
- Tilemap pour économiser la mémoire (sprites animés)

### 2. **Cards.py** - Gestion des Cartes
Implémentation orientée objet complète :

**Classe Card**
```python
- value: int (1-13, valet, dame, roi)
- color: str (Spades, Hearts, Diamonds, Clubs)
- etat: int (0=pioche, 1=main, 2=main adversaire, 3=table)
- Méthodes: getAll(), show()
```

**Classe Deck**
- Gestion d'un deck complet (2 jeux standard = 104 cartes)
- Méthodes : `pickCard()`, `playCard()`, `shuffleDeck()`, `saveDeck()`
- Suivi des différents emplacements des cartes

**Classe cardSelected**
- Gestion de la sélection actuelle
- Suivi de l'origine et position de la carte sélectionnée

### 3. **Rami.py** - Logique Métier du Jeu
Implémentation des mécaniques fondamentales :

**Fonctions principales** :
- `resetTurn()` : Réinitialisation du tour
- `undo()` : Système d'annulation multi-niveaux avec historique
- `bloomCombination()` : Affichage visuel avec détection des collisions souris
- `showCardOnTable()` : Rendu des cartes sur la table de jeu

**Points innovants** :
- Système de sauvegarde d'état pour permettre l'annulation
- Gestion des phases du tour (draw phase, delete phase)
- Détection avancée des zones interactives avec `pygame.Rect`

### 4. **Bot.py** - Intelligence Artificielle Avancée
Implémentation d'une IA stratégique multi-critères :

**Stratégies**
1. **DropTripleCard()** : Détecte et joue les brelans (3 cartes même valeur, couleurs différentes)
2. **Suites consécutives** : Identifie les séquences valides (3+ cartes consécutives même couleur)
3. **Scoring d'évaluation** : Évalue chaque coup selon des critères de risque/bénéfice

**Algorithme de décision** :
```
1. Score le dernier carte de défausse
2. Score les cartes du deck et de la main
3. Calcule la moyenne
4. Si score(défausse) > moyenne → pioche de la défausse
5. Sinon → pioche du deck
6. Applique les stratégies de jeu
```

### 5. **TempEval.py** - Évaluation Avancée
Système de scoring sophistiqué intégrant :

**Polyvalence Combinatoire** :
- Analyse de proximité des cartes complémentaires
- Score basé sur la distance (±1 à ±2 = 18pts, ±3 à ±5 = 8pts, etc.)
- Évaluation de la complétude des groupes

**Position dans Séquence** :
- Calcul de l'importance stratégique d'une carte
- Bonus pour groupes complets (3 cartes même valeur)

### 6. **UI.py** - Gestion de l'Interface
Classe Button centralisée :
- Gestion des clics avec détection de collision
- Effets de survol (mouseIn/mouseExit)
- Chargement dynamique d'images animées
- Redimensionnement adaptatif

### 7. **utils.py** - Utilitaires
Gestion centralisée des paramètres globaux et calculs :
- `getScaledMousePosUI()` : Adaptation coordonnées souris
- `getScaledMousePosCards()` : Scaling pour la table de jeu

---

## 🎮 Mécaniques de Jeu

### Règles Implémentées
- **Meldage** : Constitution de groupes (3+ cartes même valeur) et suites (3+ cartes consécutives même couleur)
- **Pioche/Défausse** : Interaction complète avec le deck
- **Undo multi-niveaux** : CTRL+Z pour annuler le dernier coup, SPACE pour réinitialiser le tour
- **Validation des coups** : Vérification des combinaisons valides selon les règles du Rami

---

## 💡 Concepts Informatiques Utilisés

| Concept | Implémentation |
|---------|-----------------|
| **Programmation Orientée Objet** | Classes Card, Deck, Button, cardSelected |
| **Algorithmes de Graphiques** | Tilemap, rendering optimisé, adaptation écran |
| **IA/Recherche Heuristique** | Scoring multi-critères, évaluation de position |
| **Gestion d'État** | Sauvegarde/restauration complète du deck |
| **Événementiel** | Pygame event loop, clics boutons, drag-and-drop |
| **Structuration Modulaire** | Séparation concerns (logique, UI, data) |
| **Optimisation Mémoire** | Utilisation de tilemap pour les animations |

---

## 🚀 Améliorations Futures Possibles

- [ ] Mode multijoueur (réseau)
- [ ] Classement ELO persistant
- [ ] Tutoriel interactif des règles
- [ ] Statistiques détaillées de jeu
- [ ] Sauvegarde/reprise de parties
- [ ] Animations de transition entre les phases

---

## 🛠️ Technologies Utilisées

- **Python 3.x** : Langage principal
- **Pygame** : Moteur graphique 2D
- **POO** : Architecture orientée objet
- **Algorithmes** : Scoring heuristique, recherche exhaustive

---

## 📈 Taille et Complexité

- **Lignes de code** : ~1000+ lignes
- **Nombre de classes** : 5+ classes principales
- **Algorithmes supplémentaires** : 10+ fonctions d'évaluation

---

## 🎓 Compétences Démontrées

✅ Développement Python avancé\
✅ Architecture logicielle et design patterns\
✅ Programmation graphique avec Pygame\
✅ Algorithmes et intelligence artificielle\
✅ Gestion d'événements et interaction utilisateur\
✅ Optimisation de performance (tilemap, rendering)\
✅ Organisation et documentation du code

---

## 📝 Licence

Ce projet est sous licence MIT.

---

**Projet réalisé pour le trophée NSI - Démonstration de compétences en ingénierie logicielle** 🏆
