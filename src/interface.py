import tkinter as tk
from tkinter import ttk, messagebox, font #messagebox  : pour afficher les alertes
from bibliotheque import Bibliotheque
from livre import Livre
from membre import Membre
from PIL import Image, ImageTk #pour gerer les images
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from visualisation import pie_genre, top_auteurs

class InterfaceBibliotheque(tk.Tk):
    def __init__(self): #constructeur de la classe parente tk.Tk
        super().__init__()
        self.title("MyLib")
        self.geometry("800x500")

        # Configuration du style global
        self.style = ttk.Style() #Ceer un objet style pour personnaliser l'apparence des widgets ttk
        self.style.theme_use('clam')
        
        # Définition des styles personnalisés
        self.style.configure('.', background='#34495E')
        self.style.configure('TFrame', background='#34495E')
        self.style.configure('TLabel', background='#34495E', foreground='white', font=('Helvetica', 10))
        self.style.configure('TButton', background='#1ABC9C', foreground='white', 
                          font=('Helvetica', 10, 'bold'), borderwidth=0)
        self.style.map('TButton', # map(): changer dynamiquement l'apparence selon l'état (bouton actif, désactivé)
                      background=[('active', '#16A085'), ('disabled', '#7F8C8D')])
        self.style.configure('Treeview', background='#2C3E50', foreground='white',
                          fieldbackground='#2C3E50', font=('Helvetica', 10))
        self.style.map('Treeview', background=[('selected', '#1ABC9C')])
        self.style.configure('Treeview.Heading', background='#1ABC9C', 
                          foreground='white', font=('Helvetica', 10, 'bold'))
        self.style.configure('TEntry', fieldbackground='white')
        self.style.configure('TNotebook', background='#34495E')
        self.style.configure('TNotebook.Tab', background='#34495E', foreground='white',
                           padding=[10, 5], font=('Helvetica', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#1ABC9C')])

        # creation des frames pricipales (frame=page)
        self.frame_accueil = tk.Frame(self, bg="#34495E")
        self.frame_principal = tk.Frame(self, bg="#34495E")

        self.frame_accueil.pack(fill='both', expand=True) # affiche acceuil au debut 
      
         #initialisation et charger les data
        self.biblio = Bibliotheque()
        self.biblio.charger_donnees()
        
        #Appelle des méthodes qui vont créer l'interface dans chaque partie
        self.accueil()
        self.init_tabs()
        self.init_livres_tab()
        self.init_membres_tab()
        self.init_emprunts_tab()
        self.init_stats_tab()

    def accueil(self):
      self.frame_accueil.configure(bg="#34495E")
      #creer une label au centre
      title_font = font.Font(family="Helvetica", size=36, weight="bold") # creer un police personalisée
      title_label = tk.Label(self.frame_accueil, text="Bienvenue sur MyLib", 
                       font=title_font, fg="white", bg="#34495E")
      title_label.place(relx=0.5, rely=0.3, anchor='center') #positionnement de labl
      # meme chose pour le slogan
      slogan_font = font.Font(family="Helvetica", size=16, slant="italic")
      slogan_label = tk.Label(self.frame_accueil, text="Gérez votre savoir, facilement et efficacement...", 
                        font=slogan_font, fg="white", bg="#34495E")
      slogan_label.place(relx=0.5, rely=0.4, anchor='center')

      btn_style = {
          "font": ("Helvetica", 14, "bold"),
          "bg": "#1ABC9C",
          "fg": "white",
          "activebackground": "#16A085",
          "activeforeground": "white",
          "bd": 0,
         "relief": "flat",
         "cursor": "hand2",
         "padx": 25,
         "pady": 10,
    }

      btn_entrer = tk.Button(self.frame_accueil, text="Entrer", 
                       command=self.show_principal, **btn_style)
      btn_entrer.place(relx=0.5, rely=0.7, anchor='center')


    def show_principal(self):
        self.frame_accueil.pack_forget() #Cache le frame d'accueil (pack_forget)
        self.frame_principal.pack(fill='both', expand=True) #Affiche le frame principal 

    def init_tabs(self):
    # Configuration du style pour l'onglet Statistiques
     self.style.configure('Stats.TFrame', background='#34495E')

    # Crée un cadre qui contiendra les onglets
     contenu_frame = ttk.Frame(self.frame_principal)
     contenu_frame.pack(fill='both', expand=True)

     tab_principal = ttk.Notebook(contenu_frame)

    # Crée 4 onglets avec style personnalisé pour l'onglet stats
     self.tab_livres = ttk.Frame(tab_principal)
     self.tab_membres = ttk.Frame(tab_principal)
     self.tab_emprunts = ttk.Frame(tab_principal)
     self.tab_stats = ttk.Frame(tab_principal, style='Stats.TFrame')  # style avec fond sombre

    # Ajoute chaque onglet au notebook
     tab_principal.add(self.tab_livres, text='Livres')
     tab_principal.add(self.tab_membres, text='Membres')
     tab_principal.add(self.tab_emprunts, text='Emprunts')
     tab_principal.add(self.tab_stats, text='Statistiques')

    # Affiche le notebook
     tab_principal.pack(expand=1, fill='both')
############################################ interface livre ###########################################
    def init_livres_tab(self):
        # Titre
        ttk.Label(self.tab_livres, text="Gestion des Livres", 
                font=('Helvetica', 14, 'bold')).pack(pady=10)

        # Barre de recherche et buttons
        frame_recherche = ttk.Frame(self.tab_livres)
        frame_recherche.pack(pady=5)
        
        ttk.Label(frame_recherche, text="Recherche (ISBN ou Titre) :").pack(side="left")
        
        self.entry_recherche = ttk.Entry(frame_recherche) # creer un champs de saisir
        self.entry_recherche.pack(side="left", padx=5)
        
        ttk.Button(frame_recherche, text="Rechercher", 
              command=self.rechercher_livre).pack(side="left")
        
        ttk.Button(frame_recherche, text="Afficher tout", 
                  command=self.charger_livres_table).pack(side="left", padx=5)

        # Tableau des livres
        columns = ("isbn", "titre", "auteur", "annee", "genre", "statut")
        self.table_livres = ttk.Treeview(self.tab_livres, columns=columns, show='headings')
        
        for col in columns:
            self.table_livres.heading(col, text=col.capitalize())
            self.table_livres.column(col, anchor='center')

        # Configuration des colonnes
        self.table_livres.column("isbn", width=80)
        self.table_livres.column("titre", width=150)
        self.table_livres.column("auteur", width=120)
        self.table_livres.column("annee", width=60)
        self.table_livres.column("genre", width=100)
        self.table_livres.column("statut", width=80)

    
        self.table_livres.pack(fill='both', expand=True, padx=10, pady=5)
      
        #self.charger_livres_table()

        # Boutons d 'ajouter et supprimer 
        frame_boutons = ttk.Frame(self.tab_livres)
        frame_boutons.pack(pady=10)
        
        ttk.Button(frame_boutons, text="Ajouter Livre", 
                  command=self.ajouter_livre).pack(side="left", padx=10)
        
        ttk.Button(frame_boutons, text="Supprimer Livre", 
                  command=self.supprimer_livre).pack(side="left", padx=10)
        
        self.charger_livres_table() #Remplit le tableau avec les données des livres

    def charger_livres_table(self):
        #Vider le tableau puis insère toutes les données des livres stockés dans self.biblio.livres
        self.table_livres.delete(*self.table_livres.get_children())
        for livre in self.biblio.livres:
            self.table_livres.insert('', 'end', values=(
                livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut
            ))

    def ajouter_livre(self):
        def valider():
            try:
                isbn = entry_isbn.get().strip()
                titre = entry_titre.get().strip()
                auteur = entry_auteur.get().strip()
                annee = entry_annee.get().strip()
                genre = entry_genre.get().strip()

                if not all([isbn, titre, auteur, annee, genre]):
                    raise ValueError("Tous les champs sont requis.")

                livre = Livre(isbn, titre, auteur, annee, genre)
                self.biblio.ajouter_livre(livre)
                self.biblio.sauvegarder_donnees()
                self.charger_livres_table()

                top.destroy()
                messagebox.showinfo("Succès", "Livre ajouté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        # fenetre de saisie
        top = tk.Toplevel(self)
        top.title("Ajouter un Livre")
        top.geometry("400x250")
        top.configure(bg="#34495E")
        
        main_frame = ttk.Frame(top)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        champs = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
        entries = []

        for i, champ in enumerate(champs):
            ttk.Label(main_frame, text=champ + " :").grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(main_frame)
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)
            entries.append(entry)

        entry_isbn, entry_titre, entry_auteur, entry_annee, entry_genre = entries
        ttk.Button(main_frame, text="Valider", command=valider).grid(row=len(champs), column=0, columnspan=2, pady=10)


    def supprimer_livre(self):
        selection = self.table_livres.selection() #selection() renvoie une list des identifiants d'elts sélectionnés dans la tab
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à supprimer.")
            return

        reponse = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce livre ?")
        if reponse: # si l user confirme la suppression
            #Récupérer  des données du livre selectionner
            item = selection[0]
            valeurs = self.table_livres.item(item, "values")
            isbn = valeurs[0]
            try:
                self.biblio.supprimer_livre(isbn)
                self.biblio.sauvegarder_donnees()
                self.charger_livres_table()
                messagebox.showinfo("Succès", "Livre supprimé.")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def rechercher_livre(self):
        recherche = self.entry_recherche.get().strip().lower() #recuperer le champs entry, supprimer les espaces , tous en min
        #Vérification du champ vide
        if not recherche:
            messagebox.showwarning("Champ vide", "Entrez un ISBN ou un titre.")
            return

        livres_trouves = []
        for livre in self.biblio.livres:
            if recherche in livre.isbn.lower() or recherche in livre.titre.lower():
                livres_trouves.append(livre)
        #supprime toutes les lignes affichées dans la Treeview (self.table_livres) pour préparer l'affichage des résultats
        self.table_livres.delete(*self.table_livres.get_children())

        if not livres_trouves:
            messagebox.showinfo("Aucun résultat", "Aucun livre trouvé.")
        else:
            for livre in livres_trouves:
                self.table_livres.insert('', 'end', values=(
                    livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut
                ))


######################################################## interface membre ##################################################################
    
    
    def init_membres_tab(self):
     ttk.Label(self.tab_membres, text="Gestion des Membres", 
              font=('Helvetica', 14, 'bold')).pack(pady=10)

    # Formulaire d'ajout de membre
     frame_form = ttk.Frame(self.tab_membres)
     frame_form.pack(pady=10)

     ttk.Label(frame_form, text="ID Membre :").grid(row=0, column=0, padx=5, pady=5)
     self.entry_id_membre = ttk.Entry(frame_form)
     self.entry_id_membre.grid(row=0, column=1, padx=5, pady=5)

     ttk.Label(frame_form, text="Nom :").grid(row=1, column=0, padx=5, pady=5)
     self.entry_nom_membre = ttk.Entry(frame_form)
     self.entry_nom_membre.grid(row=1, column=1, padx=5, pady=5)

     ttk.Button(frame_form, text="Enregistrer Membre",  
           command=self.ajouter_membre).grid(row=2, column=0, pady=10, padx=(0, 5))

     ttk.Button(frame_form, text="Rechercher",
           command=self.rechercher_membre).grid(row=2, column=1, pady=10)
    
     ttk.Button(frame_form, text="Afficher tout",
           command=self.charger_membre).grid(row=2, column=2, pady=10, padx=(5, 0))


    # Conteneur vertical pour table + boutons
     frame_table_boutons = ttk.Frame(self.tab_membres)
     frame_table_boutons.pack(fill='both', expand=True, padx=10, pady=5)

    # Colonnes du tableau
     columns = ("id", "nom", "livres_empruntes")
     self.table_membres = ttk.Treeview(frame_table_boutons, columns=columns, show='headings')

     for col in columns:
        self.table_membres.heading(col, text=col.capitalize())
        self.table_membres.column(col, width=150, anchor="center")

     self.table_membres.grid(row=0, column=0, sticky='nsew')
    

    # Ajustement automatique de la taille
     frame_table_boutons.rowconfigure(0, weight=1)
     frame_table_boutons.columnconfigure(0, weight=1)

    # Bouton Supprimer
     frame_boutons_membres = ttk.Frame(frame_table_boutons)
     frame_boutons_membres.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
    
     ttk.Button(frame_boutons_membres, text="Supprimer Membre", 
               command=self.supprimer_membre).pack(side="right", padx=10)
     
     # Chargement initial
     self.charger_membre()

    def rechercher_membre(self):
     recherche = self.entry_id_membre.get().strip().lower()
     if not recherche:
        messagebox.showwarning("Champ vide", "Entrez un ID de membre ou un nom.")
        return

     membres_trouves = []
     for m in self.biblio.membres:
        if recherche in m.id_membre.lower() or recherche in m.nom.lower():
            membres_trouves.append(m)

     self.table_membres.delete(*self.table_membres.get_children())

     if not membres_trouves:
        messagebox.showinfo("Aucun résultat", "Aucun membre trouvé.")
     else:
        for m in membres_trouves:
            self.table_membres.insert('', 'end', values=(
                m.id_membre, m.nom, ", ".join(m.livres_empruntes)
            ))

    def ajouter_membre(self):
        id_membre = self.entry_id_membre.get().strip()
        nom = self.entry_nom_membre.get().strip()

        if not id_membre or not nom:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        try:
            membre = Membre(id_membre, nom)
            self.biblio.enregistrer_membre(membre)
            self.biblio.sauvegarder_donnees()
            self.charger_membre()
            self.entry_id_membre.delete(0, tk.END)
            self.entry_nom_membre.delete(0, tk.END)
            messagebox.showinfo("Succès", "Membre enregistré.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_membre(self):
        selection = self.table_membres.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un membre à supprimer.")
            return

        reponse = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce membre ?")
        if reponse:
            item = selection[0]
            valeurs = self.table_membres.item(item, "values")
            id_membre = valeurs[0]
            try:
                self.biblio.supprimer_membre(id_membre)
                self.biblio.sauvegarder_donnees()
                self.charger_membre()
                messagebox.showinfo("Succès", "Membre supprimé.")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def charger_membre(self):
        self.table_membres.delete(*self.table_membres.get_children())
        for m in self.biblio.membres:
            self.table_membres.insert('', 'end', values=(
                m.id_membre, m.nom, ", ".join(m.livres_empruntes)
            ))

################################################### interface emprunts #################################################
    def init_emprunts_tab(self):
        ttk.Label(self.tab_emprunts, text="Gestion des Emprunts", 
                 font=('Helvetica', 14, 'bold')).pack(pady=10)

        frame = ttk.Frame(self.tab_emprunts)
        frame.pack(pady=10)

        ttk.Label(frame, text="ID Membre :").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_emprunt = ttk.Entry(frame)
        self.entry_id_emprunt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="ISBN Livre :").grid(row=1, column=0, padx=5, pady=5)
        self.entry_isbn_emprunt = ttk.Entry(frame)
        self.entry_isbn_emprunt.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self.tab_emprunts)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text=" Emprunter", 
                  command=self.emprunter_livre).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=" Retourner", 
                  command=self.retourner_livre).pack(side="left", padx=10)


    def emprunter_livre(self):
        #Récupérer des champs de saisie
        id_membre = self.entry_id_emprunt.get().strip()
        isbn = self.entry_isbn_emprunt.get().strip()
        #Vérifier que les deux champs sont remplis
        if not id_membre or not isbn:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID du membre et l'ISBN du livre.")
            return

        try:
            self.biblio.emprunter_livre(id_membre, isbn)
            self.biblio.enregistrer_historique(isbn, id_membre, "emprunté")
            self.biblio.sauvegarder_donnees()
            self.charger_livres_table()
            self.charger_membre()
            messagebox.showinfo("Succès", "Livre emprunté.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


    def retourner_livre(self):
        id_membre = self.entry_id_emprunt.get().strip()
        isbn = self.entry_isbn_emprunt.get().strip()

        if not id_membre or not isbn:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID du membre et l'ISBN du livre.")
            return

        try:
            self.biblio.retourner_livre(id_membre, isbn)
            self.biblio.enregistrer_historique(isbn, id_membre, "retourné")
            self.biblio.sauvegarder_donnees()
            self.charger_livres_table()
            self.charger_membre()
            messagebox.showinfo("Succès", "Livre retourné.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

############################################### interface statistique ############################################

    def init_stats_tab(self):
    # Le fond sombre est géré via le style 'Stats.TFrame' sur self.tab_stats

    # Titre avec fond et texte bien visibles
     label_stats = tk.Label(self.tab_stats, text="Statistiques de la Bibliothèque",
                           font=('Helvetica', 14, 'bold'), fg='white', bg='#34495E')
     label_stats.pack(pady=10)
 
    # Conteneur pour les graphiques
     frame_graph = ttk.Frame(self.tab_stats)
     frame_graph.pack(fill='both', expand=True)

    # Config grille pour que les graphiques occupent bien l'espace
     frame_graph.columnconfigure(0, weight=1)
     frame_graph.columnconfigure(1, weight=1)
     frame_graph.rowconfigure(0, weight=1)

    # Graphique 1 : Répartition des genres
     fig1 = pie_genre(self.biblio)
     canvas1 = FigureCanvasTkAgg(fig1, master=frame_graph)
     canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew")
     canvas1.draw()

    # Graphique 2 : Top 10 auteurs
     fig2 = top_auteurs(self.biblio)
     canvas2 = FigureCanvasTkAgg(fig2, master=frame_graph)
     canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew")
     canvas2.draw()


        
 

if __name__ == "__main__":
    app = InterfaceBibliotheque()
    app.mainloop()


