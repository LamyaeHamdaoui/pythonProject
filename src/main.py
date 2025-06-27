from livre import Livre
from membre import Membre
from bibliotheque import Bibliotheque
from exception import *
from collections import Counter
import matplotlib.pyplot as plt
from visualisation import pie_genre, top_auteurs

biblio = Bibliotheque()
biblio.charger_donnees()

while True:
    print("\n==== GESTION BIBLIOTHEQUE ====")
    print("1. Ajouter un livre")
    print("2. Supprimer un livre")
    print("3. Enregistrer un membre")
    print("4. Emprunter un livre")
    print("5. Retourner un livre")
    print("6. Sauvegarder")
    print("7. Statistiques")
    print("8. Afficher l’historique")
    print("9. Quitter")
   

    choix = input("Choix : ")

    try:
        if choix == "1":
            isbn = input("ISBN: ")
            titre = input("Titre: ")
            auteur = input("Auteur: ")
            annee = input("Année: ")
            genre = input("Genre: ")
            biblio.ajouter_livre(Livre(isbn, titre, auteur, annee, genre))
            print("Livre ajouté.")

        elif choix == "2":
            isbn = input("ISBN du livre à supprimer: ")
            biblio.supprimer_livre(isbn)
            print("Livre supprimé.")

        elif choix == "3":
            id = input("ID membre: ")
            nom = input("Nom membre: ")
            biblio.enregistrer_membre(Membre(id, nom))
            print("Membre enregistré.")

        elif choix == "4":
            id = input("ID membre: ")
            isbn = input("ISBN livre: ")
            biblio.emprunter_livre(id, isbn)
            print("Livre emprunté.")
            biblio.enregistrer_historique(isbn, id, "emprunt")

        elif choix == "5":
            id = input("ID membre: ")
            isbn = input("ISBN livre: ")
            biblio.retourner_livre(id, isbn)
            print("Livre retourné.")
            biblio.enregistrer_historique(isbn, id, "retour")

        elif choix == "6":
           biblio.sauvegarder_donnees()
           print("Données sauvegardées.")

        elif choix == "7":
            if biblio.livres:
                fig1 = pie_genre(biblio)
                fig1.show()
                fig2 = top_auteurs(biblio)
                fig2.show()
            else:
                print("Aucun livre disponible pour générer les statistiques.")


        elif choix == "8":
          biblio.afficher_historique() 

        elif choix == "9":
           biblio.sauvegarder_donnees()
           print("On a quitté.")
           break

        else:
            print("Choix invalide.")

    except Exception as e:
        print("Erreur:", e)
