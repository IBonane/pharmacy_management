import sys
import tkinter as tk
from tkinter import messagebox
import hashlib
import mysql.connector as mc

sys.path.append("/home/djimba/python_projects/pharmacie")

from config import dbinfo
from services.dbConnection import dbconnection


class User:
    def __init__(self, root):
        self.root = root
        self.root.title("User Register")

        # Connexion à la base de données
        self.conn = dbconnection(mc, dbinfo)

        # Variable pour suivre l'état de connexion
        self.is_logged_in = False

    def show_registration_page(self):
        # Oublie la page précédente
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Crée et affiche la page d'inscription
        self.register_page()

        # Ajouter un bouton de retour à la page d'accueil
        self.btn_back_home = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_home.pack(pady=10)

        # Ajouter un bouton pour accéder à la page de connexion
        self.btn_goto_login = tk.Button(self.root, text="Aller à la connexion", command=self.show_login_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_goto_login.pack(pady=10)

    def register_page(self):
        # Interface pour l'inscription
        self.label_firstname = tk.Label(self.root, text="Nom:", font=("Helvetica", 12))
        self.entry_firstname = tk.Entry(self.root, font=("Helvetica", 12))
        self.label_lastname = tk.Label(self.root, text="Prénom:", font=("Helvetica", 12))
        self.entry_lastname = tk.Entry(self.root, font=("Helvetica", 12))
        self.label_username = tk.Label(self.root, text="Email:", font=("Helvetica", 12))
        self.entry_username = tk.Entry(self.root, font=("Helvetica", 12))
        self.label_password = tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 12))
        self.entry_password = tk.Entry(self.root, show="*", font=("Helvetica", 12))
        self.btn_register = tk.Button(self.root, text="S'inscrire", command=self.register_user, font=("Helvetica", 12), padx=10, pady=5)

        # Placement des widgets
        self.label_firstname.pack(padx=10, pady=10)
        self.entry_firstname.pack(padx=10, pady=10)
        self.label_lastname.pack(padx=10, pady=10)
        self.entry_lastname.pack(padx=10, pady=10)
        self.label_username.pack(padx=10, pady=10)
        self.entry_username.pack(padx=10, pady=10)
        self.label_password.pack(padx=10, pady=10)
        self.entry_password.pack(padx=10, pady=10)
        self.btn_register.pack(pady=10)

    def register_user(self):
        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Hacher le mot de passe avant de l'insérer dans la base de données
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = (firstname, lastname, username, hashed_password)

        # Vérifier si le nom d'utilisateur existe déjà
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_name=%s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
        else:
            # Insérer le pharmacien dans la base de données
            cursor.execute("INSERT INTO user (first_name, last_name, user_name, password) VALUES (%s, %s, %s, %s)", user)
            self.conn.commit()
            messagebox.showinfo("Succès", "Inscription réussie.")

            # Rediriger vers la page de connexion après l'inscription réussie
            self.show_login_page()

    def show_login_page(self):
        # Efface la page précédente
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Crée et affiche la page de connexion
        self.login_page()

        # Ajouter un bouton de retour à la page d'accueil
        self.btn_back_home = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_home.pack(pady=10)

        # Ajouter un bouton pour accéder à la page d'inscription
        self.btn_goto_register = tk.Button(self.root, text="Aller à l'inscription", command=self.show_registration_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_goto_register.pack(pady=10)

    def login_page(self):
        # Interface pour la connexion
        self.label_username = tk.Label(self.root, text="Email:", font=("Helvetica", 12))
        self.entry_username = tk.Entry(self.root, font=("Helvetica", 12))
        self.label_password = tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 12))
        self.entry_password = tk.Entry(self.root, show="*", font=("Helvetica", 12))
        self.btn_login = tk.Button(self.root, text="Se connecter", command=self.login_user, font=("Helvetica", 12))

        # Placement des widgets
        self.label_username.pack(padx=10, pady=10)
        self.entry_username.pack(padx=10, pady=10)
        self.label_password.pack(padx=10, pady=10)
        self.entry_password.pack(padx=10, pady=10)
        self.btn_login.pack(pady=10)

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Hacher le mot de passe avant de l'insérer dans la base de données
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Vérifier les informations d'identification
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_name=%s AND password=%s", (username, hashed_password))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Succès", "Connexion réussie.")
            self.is_logged_in = True
            self.current_user = {'firstname':result[1], 'lastname':result[2], 'email':username}
            self.home_page()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def logout(self):
        self.is_logged_in = False
        self.home_page()
        
    def show_profile(self):
        # Oublie la page précédente
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Afficher les informations de l'utilisateur
        self.label_firstname = tk.Label(self.root, text=f"Nom : {self.current_user['firstname']}", font=("Helvetica", 14))
        self.label_lastname = tk.Label(self.root, text=f"Prénom : {self.current_user['lastname']}", font=("Helvetica", 14))
        self.label_username = tk.Label(self.root, text=f"Nom d'utilisateur : {self.current_user['email']}", font=("Helvetica", 14))

        self.label_firstname.pack(pady=10)
        self.label_lastname.pack(pady=10)
        self.label_username.pack(pady=10)

        # Ajouter un bouton pour accéder à la page d'édition du profil
        self.btn_edit_profile = tk.Button(self.root, text="Éditer le profil", command=self.edit_profile_page, font=("Helvetica", 12))
        self.btn_edit_profile.pack(pady=10)

        # Ajouter un bouton pour supprimer le profil
        self.btn_delete_profile = tk.Button(self.root, text="Supprimer le profil", command=self.delete_profile, font=("Helvetica", 12), fg="red")
        self.btn_delete_profile.pack(pady=10)

        # Ajouter un bouton de retour à la page d'accueil
        self.btn_back_home = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_home.pack(pady=10)

    def edit_profile_page(self):
        # Oublie la page précédente
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Implémentez la page d'édition du profil
        self.label_edit_profile = tk.Label(self.root, text="Page d'édition du profil", font=("Helvetica", 16))
        self.label_edit_profile.pack(pady=10)

        # Ajoutez des Entry avec les valeurs par défaut
        self.label_edit_firstname = tk.Label(self.root, text="Nom:", font=("Helvetica", 12))
        self.entry_edit_firstname = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_edit_firstname.insert(0, self.current_user['firstname'])  # Valeur par défaut

        self.label_edit_lastname = tk.Label(self.root, text="Prénom:", font=("Helvetica", 12))
        self.entry_edit_lastname = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_edit_lastname.insert(0, self.current_user['lastname'])  # Valeur par défaut

        self.label_edit_username = tk.Label(self.root, text="Email:", font=("Helvetica", 12))
        self.entry_edit_username = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_edit_username.insert(0, self.current_user['email'])  # Valeur par défaut
        
        self.label_edit_password = tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 12))
        self.entry_edit_password = tk.Entry(self.root, show="*", font=("Helvetica", 12))

        # Placement des widgets
        self.label_edit_firstname.pack(padx=10, pady=10)
        self.entry_edit_firstname.pack(padx=10, pady=10)

        self.label_edit_lastname.pack(padx=10, pady=10)
        self.entry_edit_lastname.pack(padx=10, pady=10)

        self.label_edit_username.pack(padx=10, pady=10)
        self.entry_edit_username.pack(padx=10, pady=10)
        
        self.label_edit_password.pack(padx=10, pady=10)
        self.entry_edit_password.pack(padx=10, pady=10)

        # Ajouter un bouton de sauvegarde des modifications
        self.btn_save_changes = tk.Button(self.root, text="Enregistrer les modifications", command=self.save_profile_changes, font=("Helvetica", 12))
        self.btn_save_changes.pack(pady=20)

        # Ajouter un bouton de retour à la page d'utilisateur
        self.btn_back_user_page = tk.Button(self.root, text="Retour à la page d'utilisateur", command=self.show_profile, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_user_page.pack(pady=10)

    def save_profile_changes(self):
        # Obtenez les nouvelles valeurs des Entry
        new_firstname = self.entry_edit_firstname.get()
        new_lastname = self.entry_edit_lastname.get()
        new_username = self.entry_edit_username.get()
        new_password = self.entry_edit_password.get()
        
        print('entrée : ', new_password)

        # Hacher le mot de passe avant de l'insérer dans la base de données
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        # old = hashlib.sha256(('admin').encode()).hexdigest()
        # print(old=="0b47e7b150390fdbd2255a14051797850f839f3ff21bfa2e7a5e33082b41a2e0")
        user = (new_firstname, new_lastname, new_username, hashed_password, self.current_user['email'])

        # Vérifier si le nom d'utilisateur existe déjà
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_name=%s", (new_username,))
        if cursor.fetchone() and new_username != self.current_user['email']:
            messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
        else:
            # Insérer le pharmacien dans la base de données
            cursor.execute("UPDATE user SET first_name=%s, last_name=%s, user_name=%s, password=%s WHERE user_name=%s", user)
            self.conn.commit()
            # self.current_user = {'firstname':new_firstname, 'lastname':new_lastname, 'email':new_username}
            messagebox.showinfo("Succès", "Mis à jour du profile réussie.")

            # Rediriger vers la page de connexion après l'inscription réussie
            self.show_profile()

    def delete_profile(self):
        # Boîte de dialogue de confirmation
        response = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer votre profil ?")

        if response:
            # L'utilisateur a confirmé la suppression
            cursor = self.conn.cursor()

            # Supprimer l'utilisateur de la base de données
            cursor.execute("DELETE FROM user WHERE user_name=%s", (self.current_user['email'],))
            self.conn.commit()

            # Afficher un message de confirmation
            messagebox.showinfo("Succès", "Profil supprimé avec succès.")

            # Déconnecter l'utilisateur
            self.logout()
