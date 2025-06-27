
#  Projet : Système de Gestion de Bibliothèque  
**Module : Programmation Avancée en Python – ENSAO GI3**
Réalisé par :
   Nom & Prénom : HAMDAOUI Lamyae
   Filière : GI3

##  Fonctionnalités principales de l'application
L’application nous permet : 
-  Ajouter / supprimer un livre  
-  Enregistrer / supprimer un membre  
-  Emprunter et retourner un livre  
- Sauvegarde / chargement des données dans des fichiers texte (`.txt`) ou CSV (`.csv`)  
-  Statistiques avec graphiques (camembert, histogramme) via `matplotlib`  
-  Gestion des erreurs via des **exceptions personnalisées**

##  Guide d'installation

### 1. Prérequis
- Python 3.13.5 

### 2. Installation des bibliothèques
 pip install matplotlib
 Tkinter est souvent préinstallé

### 3. Lancer le programme
 ***Interface en ligne de commande :
 Python src/main.py
 ***Interface graphique (Tkinter) :
 python src/interface.py
### 4.Organisation des fichiers
projet/
│
├── data/                     
│   ├── historique.csv         
│   ├── livres.txt             
│   └── membres.txt           
│
├── doc/                     
│    ├── rapport.pdf 

├── src/                   
│   ├── bibliotheque.py        # Classe principale 
│   ├── exception.py           # Exceptions personnalisées
│   ├── interface.py           # Interface graphique (Tkinter)
│   ├── livre.py               # Classe Livre
│   ├── membre.py              # Classe Membre
│   ├── main.py                # Menu ligne de commande
│   ├── visualisation.py       # Statistiques avec matplotlib
├── README.md                  





