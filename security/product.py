import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mc
from config import dbinfo
from services.dbConnection import dbconnection

class Product:
    def __init__(self, root):
        self.root = root
        self.root.title("Products Management")
        self.conn = dbconnection(mc, dbinfo)
        self.page_size = 10  # Nombre de produits par page
        self.current_page = 1
        self.show_product_management_page()
        
    def mytree(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Nom du produit")
        self.tree.heading("Price", text="Prix")
        self.tree.heading("Quantity", text="Quantité en stock")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=220, anchor=tk.CENTER)
        self.tree.column("Price", width=120, anchor=tk.CENTER)
        self.tree.column("Quantity", width=220, anchor=tk.CENTER)

    def show_product_management_page(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.product_management_page()

        self.btn_back_home = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_home.pack(pady=10)

    def product_management_page(self):
        label_manage_products = tk.Label(self.root, text="Gestion des produits", font=("Helvetica", 16))
        label_manage_products.pack(pady=10)

        self.mytree()

        self.show_products_on_page()

        for col in ["ID", "Name", "Price", "Quantity"]:
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(pady=10)
        
        self.btn_search_product = tk.Button(self.root, text="Rechercher un produit", command=self.show_search_product, font=("Helvetica", 12))
        self.btn_search_product.pack(pady=10)

        # Ajouter des boutons pour naviguer entre les pages
        self.btn_prev_page = tk.Button(self.root, text="Page précédente", command=self.show_previous_page, font=("Helvetica", 12))
        self.btn_prev_page.pack(pady=10)

        self.btn_next_page = tk.Button(self.root, text="Page suivante", command=self.show_next_page, font=("Helvetica", 12))
        self.btn_next_page.pack(pady=10)
        
        if self.is_logged_in and self.current_user['is_admin'] == 1:

            self.btn_add_product = tk.Button(self.root, text="Ajouter un produit", command=self.add_product, font=("Helvetica", 12))
            self.btn_add_product.pack(pady=10)

            self.btn_edit_product = tk.Button(self.root, text="Éditer le produit", command=self.edit_product, font=("Helvetica", 12))
            self.btn_edit_product.pack(pady=10)

            self.btn_delete_product = tk.Button(self.root, text="Supprimer le produit", command=self.delete_product, font=("Helvetica", 12), fg="red")
            self.btn_delete_product.pack(pady=10)

    def show_products_on_page(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size

        products = self.products_list()
        for i, product in enumerate(products[start_index:end_index], start=1):
            self.tree.insert("", i, values=(product[0], product[1], product[2], product[3]))

    def show_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.show_products_on_page()

    def show_next_page(self):
        total_pages = -(-len(self.products_list()) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self.show_products_on_page()

    def products_list(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, price, stock FROM products ORDER BY name ASC")
        products = cursor.fetchall()
        return products
    
    
    def add_product(self):
        # Oublie la page précédente
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Implémentez la page d'édition du profil
        self.label_edit_product = tk.Label(self.root, text="Page d'édition de produit", font=("Helvetica", 16))
        self.label_edit_product.pack(pady=10)

        # Ajoutez des Entry avec les valeurs par défaut
        self.label_edit_name = tk.Label(self.root, text="Nom du produit:", font=("Helvetica", 12))
        self.entry_edit_name = tk.Entry(self.root, font=("Helvetica", 12))

        self.label_edit_price = tk.Label(self.root, text="prix:", font=("Helvetica", 12))
        self.entry_edit_price = tk.Entry(self.root, font=("Helvetica", 12))

        self.label_edit_quantity = tk.Label(self.root, text="Stock:", font=("Helvetica", 12))
        self.entry_edit_quantity = tk.Entry(self.root, font=("Helvetica", 12))

        # Placement des widgets
        self.label_edit_name.pack(padx=10, pady=10)
        self.entry_edit_name.pack(padx=10, pady=10)

        self.label_edit_price.pack(padx=10, pady=10)
        self.entry_edit_price.pack(padx=10, pady=10)

        self.label_edit_quantity.pack(padx=10, pady=10)
        self.entry_edit_quantity.pack(padx=10, pady=10)

        # Ajouter un bouton de sauvegarde des modifications
        self.btn_save_changes = tk.Button(self.root, text="Enregistrer les modifications", command=self.save_product_add, font=("Helvetica", 12))
        self.btn_save_changes.pack(pady=20)

        # Ajouter un bouton de retour à la page d'utilisateur
        self.btn_back_user_page = tk.Button(self.root, text="Retour à la page d'utilisateur", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_user_page.pack(pady=10)
            
    def save_product_add(self):
        # Obtenez les nouvelles valeurs des Entry
        name = self.entry_edit_name.get()
        price = self.entry_edit_price.get()
        stock = self.entry_edit_quantity.get()

        product = (name, price, stock)

        # Vérifier si le nom d'utilisateur existe déjà
        cursor = self.conn.cursor()

        # Insérer le pharmacien dans la base de données
        cursor.execute("INSERT INTO products (name, price, stock) VALUES(%s, %s, %s)", product)
        self.conn.commit()

        messagebox.showinfo("Succès", "Nouveau produit ajoué avec succès.")

        # Rediriger vers la page de produits
        self.show_product_management_page()

    def edit_product(self):
        selected_item = self.tree.selection()

        if selected_item:
            # Oublie la page précédente
            for widget in self.root.winfo_children():
                widget.pack_forget()

            item_values = self.tree.item(selected_item, "values")
            self.product_id = item_values[0]
            product_name = item_values[1]
            product_price = item_values[2]
            product_quantity = item_values[3]

            # Implémentez la page d'édition du profil
            self.label_edit_product = tk.Label(self.root, text="Page d'édition de produit", font=("Helvetica", 16))
            self.label_edit_product.pack(pady=10)

            # Ajoutez des Entry avec les valeurs par défaut
            self.label_edit_name = tk.Label(self.root, text="Nom du produit:", font=("Helvetica", 12))
            self.entry_edit_name = tk.Entry(self.root, font=("Helvetica", 12))
            self.entry_edit_name.insert(0, product_name)  # Valeur par défaut

            self.label_edit_price = tk.Label(self.root, text="prix:", font=("Helvetica", 12))
            self.entry_edit_price = tk.Entry(self.root, font=("Helvetica", 12))
            self.entry_edit_price.insert(0, product_price)  # Valeur par défaut

            self.label_edit_quantity = tk.Label(self.root, text="Stock:", font=("Helvetica", 12))
            self.entry_edit_quantity = tk.Entry(self.root, font=("Helvetica", 12))
            self.entry_edit_quantity.insert(0, product_quantity)  # Valeur par défaut

            # Placement des widgets
            self.label_edit_name.pack(padx=10, pady=10)
            self.entry_edit_name.pack(padx=10, pady=10)

            self.label_edit_price.pack(padx=10, pady=10)
            self.entry_edit_price.pack(padx=10, pady=10)

            self.label_edit_quantity.pack(padx=10, pady=10)
            self.entry_edit_quantity.pack(padx=10, pady=10)

            # Ajouter un bouton de sauvegarde des modifications
            self.btn_save_changes = tk.Button(self.root, text="Enregistrer les modifications", command=self.save_product_changes, font=("Helvetica", 12))
            self.btn_save_changes.pack(pady=20)

            # Ajouter un bouton de retour à la page d'utilisateur
            self.btn_back_user_page = tk.Button(self.root, text="Retour à la page d'utilisateur", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
            self.btn_back_user_page.pack(pady=10)
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner un produit à éditer.")
            
    def save_product_changes(self):
        # Obtenez les nouvelles valeurs des Entry
        name = self.entry_edit_name.get()
        price = self.entry_edit_price.get()
        stock = self.entry_edit_quantity.get()

        product = (name, price, stock, self.product_id)

        # Vérifier si le nom d'utilisateur existe déjà
        cursor = self.conn.cursor()

        # Insérer le pharmacien dans la base de données
        cursor.execute("UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s", product)
        self.conn.commit()

        messagebox.showinfo("Succès", "Mis à jour du produit réussie.")

        # Rediriger vers la page de produits
        self.show_product_management_page()

    def show_product_found(self):
        self.clear_widgets()
        self.products_found()

    def products_found(self):
        self.clear_widgets()
        
        label_products_found = tk.Label(self.root, text="Produits trouvés", font=("Helvetica", 16))
        label_products_found.pack(pady=10)

        # self.tree.delete(*self.tree.get_children())  # Nettoyer le Treeview

        self.mytree()  # Créer un nouveau Treeview

        products = self.search_product()
        for i, product in enumerate(products):
            self.tree.insert("", i, values=(product[0], product[1], product[2], product[3]))

        self.tree.pack(pady=10)
        
        self.btn_search_product = tk.Button(self.root, text="Rechercher un produit", command=self.show_search_product, font=("Helvetica", 12))
        self.btn_search_product.pack(pady=10)
        
        self.btn_back_user_page = tk.Button(self.root, text="Retour à la liste des produits", command=self.show_product_management_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_user_page.pack(pady=10)

    def search_product(self):
        search = self.entry_search.get()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, price, stock FROM products WHERE name LIKE %s ORDER BY name ASC", ('%' + search + '%',))
        products = cursor.fetchall()
        return products

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        
    def show_search_product(self):
        self.clear_widgets()

        # Ajoutez des Entry avec les valeurs par défaut
        self.label_search = tk.Label(self.root, text="Recherche de produit:", font=("Helvetica", 12))
        self.entry_search = tk.Entry(self.root, font=("Helvetica", 12))
    
        self.label_search.pack(padx=10, pady=10)
        self.entry_search.pack(padx=10, pady=10)
        
        self.btn_search = tk.Button(self.root, text="Rechercher", command=self.products_found, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_search.pack(pady=10)
        
        self.btn_back_user_page = tk.Button(self.root, text="Retour à la liste des produits", command=self.show_product_management_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_user_page.pack(pady=10)

    def delete_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_id = item_values[0]

            cursor = self.conn.cursor()

            # Supprimer l'utilisateur de la base de données
            cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
            self.conn.commit()

            # Afficher un message de confirmation
            messagebox.showinfo("Succès", "produit supprimé avec succès.")
            
            # Rediriger vers la page de produits
            self.show_product_management_page()

        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner un produit à supprimer.")
