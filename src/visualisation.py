import matplotlib.pyplot as plt
from collections import Counter # pour compter les occurrences
import matplotlib.pyplot as plt
from collections import Counter


def pie_genre(biblio):
    genres = [livre.genre for livre in biblio.livres] #list contient le genre de chaque livre 
    c = Counter(genres) # ompte combien de fois chaque genre apparaît 

    # Remplacer les espaces par des sauts de ligne pour les labels ( "Roman Policier" → "Roman\nPolicier") pour la lisibilité 
    labels_multiligne = [g.replace(' ', '\n') for g in c.keys()]
    # creer le figure 
    fig, ax = plt.subplots(figsize=(6,6))  # Taille carrée
    fig.patch.set_facecolor('#34495E') #color de fond
    

    wedges, texts, autotexts = ax.pie(
        c.values(),# les valeurs des parts (nbr de livres par genre)
        labels=labels_multiligne,#les noms des genres avec saut de ligne
        autopct='%1.1f%%',#affiche le pourcentage avec une décimale.
        startangle=90,# commence la première part à 90° (en haut).
        textprops={'color':'white', 'fontsize':10, 'weight':'bold'}
    )

    ax.set_title("Répartition des genres", color='white', fontsize=14, fontweight='bold')
    ax.axis('equal')  # Cercle parfait pas ovale
    return fig



def top_auteurs(biblio):
    auteurs = [livre.auteur for livre in biblio.livres] #List des auteurs de tous les livres
    c = Counter(auteurs).most_common(10) #Compte les occurrences d'auteurs et garde les 10 plus fréquents sous forme de liste de tuples (auteur, nombre)

    noms, valeurs = zip(*c) if c else ([], []) #Dézippe les auteurs et leurs comptes en deux listes séparées noms et valeurs sinon des list vides

    fig, ax = plt.subplots(figsize=(6,4))  # taille normale
    fig.patch.set_facecolor('#34495E')
    ax.set_facecolor('#34495E')

    bars = ax.bar(noms, valeurs, color='#1ABC9C')

    ax.set_title("Top 10 auteurs", color='white', fontsize=14, fontweight='bold')

    # Tronquer les noms longs
    noms_courts = [nom if len(nom) <= 15 else nom[:12] + '...' for nom in noms] #pour les noms langues
    ax.set_xticklabels(noms_courts, rotation=45, ha='right', fontsize=10, color='white') #appliquer ces noms sur l exe x avec 45°

    ax.tick_params(axis='y', colors='white')
    # Augmente la marge basse pour les labels inclinés
    fig.subplots_adjust(bottom=0.25)

    return fig


