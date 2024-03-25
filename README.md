# Automate
Ce projet est une implémentation en Python d'un automate. Il permet de créer et de manipuler des automates de différents types, tels que les automates finis déterministes (AFD), les automates finis non déterministes (AFN), les automates à pile, etc. La classe Automate fournit des méthodes pour ajouter et supprimer des états et des transitions, définir l'alphabet, les états initiaux et finaux, et effectuer diverses opérations telles que déterminer si l'automate est déterministe, minimiser le nombre d'états, et convertir l'automate en une représentation graphique à l'aide de la bibliothèque graphviz.

Installation
Pour utiliser le code, vous devez avoir graphviz installé sur votre ordinateur. Vous pouvez télécharger graphviz depuis le site officiel : https://graphviz.org/download/

Une fois graphviz installé, vous pouvez télécharger le code depuis ce dépôt GitHub et l'exécuter en utilisant un éditeur de code Python tel que PyCharm ou Visual Studio Code. Assurez-vous que votre environnement Python a accès à la bibliothèque graphviz.

Si vous utilisez Anaconda, vous pouvez installer graphviz en utilisant la commande suivante dans votre terminal :

```
conda install python-graphviz
```

Si vous utilisez pip, vous pouvez installer graphviz en utilisant la commande suivante dans votre terminal :

```
pip install graphviz
```

# Utilisation
Le code définit une classe Automate qui représente un AFD. La classe contient plusieurs méthodes pour ajouter et supprimer des états et des transitions, définir l'alphabet, les états initiaux et finaux, et effectuer diverses opérations telles que déterminer si l'AFD est déterministe, minimiser le nombre d'états, et convertir l'AFD en une représentation graphique à l'aide de la bibliothèque graphviz.

La classe Automate a les méthodes suivantes :

`__init__` : Initialise un automate vide.  
`Automate` : Définit l'alphabet de l'automate.  
`ajouter_etat` : Ajoute un état à l'automate.  
`ajouter_initial` : Ajoute un état initial à l'automate.  
`ajouter_final` : Ajoute un état final à l'automate.  
`supprimer_etat` : Supprime un état de l'automate.  
`ajouter_transition` : Ajoute une transition à l'automate.  
`supprimer_transition` : Supprime une transition de l'automate.  
`copie` : Retourne une copie de l'automate.  
`__str__` : Retourne une représentation sous forme de chaîne de caractères de l'automate.  
`demonte` : Retourne une liste de transitions où chaque transition est décomposée en une transition par symbole de l'alphabet.  
`concatenation_transitions` : Retourne une liste de transitions où chaque transition est concaténée en une transition par état de l'automate.  
`to_dot` : Retourne une représentation graphique de l'automate sous forme de graphe avec la bibliothèque graphviz.  
`to_png` : Retourne une représentation graphique de l'automate sous forme d'image au format png.  
`sauvegarder` : Sauvegarde l'automate dans un fichier texte avec une structure prédéfinie.  
`reconstruire` : Permet de construire une liste d'états à partir d'une chaîne de caractères.  
`charger` : Charge un automate depuis un fichier texte avec une structure prédéfinie.  
`reset` : Réinitialise l'automate.  
`epsilon_cloture` : Retourne la clôture transitive de l'automate.  
`epsilon_initial` : Ajoute les états accessibles par epsilon aux états initiaux de l'automate.  
`etats_accessibles` : Retourne la liste des états accessibles depuis l'état initial.  
`existe_chemin_vers_etat_final` : Retourne vrai s'il existe un chemin depuis l'état donné vers un état final, faux sinon.  
`epsilon_supprimer` : Supprime les transitions epsilon de l'automate en appliquant la règle.  
`synchroniser` : Réalise la suppression des transitions epsilon de l'automate.  
`completer` : Complète l'automate pour qu'il soit complet.  
`supprimer_puit` : Supprime l'état puit de l'automate.  
`table_transition` : Retourne la table de transition de l'automate.  
`afficher_table_transition` : Affiche la table de transition de l'automate.  
`est_deterministe` : Retourne vrai si l'automate est déterministe, faux sinon.  
`concatener` : Retourne une chaîne de caractères concaténée à partir d'une liste de caractères.  
`determiniser` : Retourne un automate déterministe équivalent à l'automate.  
`find_index` : Retourne une liste des indexes où la valeur est présente dans la liste.  
`moore` : Réalise l'algorithme de Moore pour minimiser l'automate.  
`minimiser` : Retourne un automate minimal équivalent à l'automate.  
`accepte_mot` : Retourne vrai si le mot est accepté par l'automate, faux sinon.  
<br>
De plus, il existe trois fonctions `union_automate`, `concatenation_automate`, et `duplication_automate` qui effectuent des opérations d'union, de concaténation et de duplication sur deux ou plusieurs automates.

# Exemple
Voici un exemple d'utilisation de la classe Automate :

```
from automate import Automate

# Créer un automate
aut = Automate()

# Définir l'alphabet
aut.Automate(alphabet="ab")

# Ajouter des états
aut.ajouter_etat("A", est_initial=True)
aut.ajouter_etat("B")
aut.ajouter_etat("C", est_terminal=True)

# Ajouter des transitions
aut.ajouter_transition("A", "a", "B")
aut.ajouter_transition("B", "b", "C")

# Afficher l'automate
print(aut)

# Sauvegarder l'automate dans un fichier texte
aut.sauvegarder("automate.txt")

# Charger un automate depuis un fichier texte
aut2 = Automate()
aut2.charger("automate.txt")

# Afficher l'automate chargé
print(aut2)

# Convertir l'automate en une représentation graphique
dot = aut.to_dot()

# Afficher la représentation graphique
print(dot)

# Convertir l'automate en une image png
aut.to_png("automate.png")

# Déterminer si l'automate est déterministe
print(aut.est_deterministe())

# Minimiser l'automate
aut.minimiser()

# Afficher l'automate minimisé
print(aut)

# Vérifier si un mot est accepté par l'automate
print(aut.accepte_mot("aba"))
```
