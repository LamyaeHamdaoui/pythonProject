import exception as exc
from membre import Membre
from livre import Livre
import json 
import csv
import datetime

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.membres = []
    
    def ajouter_livre(self, livre):
        self.livres.append(livre)

    def supprimer_livre(self, isbn):
     for livre in self.livres:
        if livre.isbn == isbn:
            self.livres.remove(livre)
            return  
     raise exc.LivreInexistantError()

    def enregistrer_membre(self, membre):
        self.membres.append(membre)
    
    def supprimer_membre(self, id_membre):
    # Trouver le membre par son ID puis le retirer de la liste
     self.membres = [m for m in self.membres if m.id_membre != id_membre]


    def emprunter_livre(self, id_membre, isbn):
        membre = self.trouver_membre(id_membre)
        livre = self.trouver_livre(isbn)
        if livre.statut != "disponible":
            raise exc.LivreIndisponibleError()
        if len(membre.livres_empruntes) >= 3:
            raise exc.QuotaEmpruntDepasseError()
        membre.livres_empruntes.append(livre.isbn)
        livre.statut = "emprunté"


    def retourner_livre(self, id_membre, isbn):
     membre = self.trouver_membre(id_membre)
     livre = self.trouver_livre(isbn)

     if membre is None or livre is None:
        raise ValueError("Membre ou livre introuvable.")

     if livre.statut == "disponible":
        raise ValueError("Ce livre est déjà disponible.")

     if isbn not in membre.livres_empruntes:
        raise ValueError("Ce membre n’a pas emprunté ce livre.")

     membre.livres_empruntes.remove(isbn)
     livre.statut = "disponible"



    def trouver_membre(self, id_membre):
        for m in self.membres:
            if m.id_membre == id_membre:
                return m
        raise exc.MembreInexistantError()

    def trouver_livre(self, isbn):
        for l in self.livres:
            if l.isbn == isbn:
                return l
        raise exc.LivreInexistantError()
    

    
    def sauvegarder_donnees(self):
        with open("data/livres.txt", "w") as f:#Ouvre (ou crée si non existant) le fich  en mode écriture 
            for l in self.livres:
                f.write(f"{l.isbn};{l.titre};{l.auteur};{l.annee};{l.genre};{l.statut}\n") #Écrit chaque livre sur une ligne du fichier, avec les champs séparés par  ;

        with open("data/membres.txt", "w") as f:
            for m in self.membres:
                livres_str = ",".join(m.livres_empruntes) #convertir la list des livres en chaines de caracteres 
                f.write(f"{m.id_membre};{m.nom};{livres_str}\n")

    def charger_donnees(self):
        try:
            with open("data/livres.txt") as f:
                self.livres = []
                for l in f:
                    isbn, titre, auteur, annee, genre, statut = l.strip().split(";") #Supprime les espaces et le saut de ligne à la fin (strip()) #Sépare la ligne en morceaux avec split(";"), selon l’ordre des champs
                    self.livres.append(Livre(isbn, titre, auteur, annee, genre, statut))

            with open("data/membres.txt") as f:
                self.membres = []
                for l in f:
                    parts = l.strip().split(";")  #Nettoie la ligne et la découpe avec split(";")
                    id_membre, nom = parts[0], parts[1] #Récupère l’ID et le nom du membre
                    empruntes = parts[2].split(",") if len(parts) > 2 and parts[2] else [] #verifier qu il y a 3 champs dans la ligne et verifier que 3eme champs n est pas vide et on met dans empruntes
                    membre = Membre(id_membre, nom)
                    membre.livres_empruntes = empruntes #Assigne à l’objet membre la liste des livres empruntés
                    self.membres.append(membre)
        except FileNotFoundError:
            self.livres = []
            self.membres = []
# cette methode sert à  enregistrer une ligne d’historique dans un fichier CSV chaque fois qu’un livre est emprunté ou retourné
    def enregistrer_historique(self, isbn, id_membre, action):  # action : emprunté / retourné
     with open("data/historique.csv", "a", newline="") as f:
        fich = csv.writer(f)
        date_du_jour = datetime.datetime.now().strftime("%Y-%m-%d")
        fich.writerow([date_du_jour, isbn, id_membre, action])

    def afficher_historique(self):
     try:
        with open("data/historique.csv", "r") as f:
            for l in f:
                print(l.strip()) #l.strip() supprime les caractères invisibles \n
     except FileNotFoundError:
        print("Aucun historique disponible.")

