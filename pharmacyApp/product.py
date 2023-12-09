import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mc
from config import dbinfo
from services.dbConnection import dbconnection
from datetime import datetime
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict

class Product:
    def __init__(self, root):
        self.root = root
        self.root.title("Products Management")
        self.conn = dbconnection(mc, dbinfo)
        self.page_size = 10  # Nombre de produits par page
        self.current_page = 1
        print(self.tenBestSeller())
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

    #SECTION DE VISUALISATION DES PRODUITS
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
    
    #SECTION D'AJOUT DE PRODUIT
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

    #SECTION DE MODIFICATION DE PRODUIT
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

    #SECTION DE RECHERCHE DE PRODUIT
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

    #SECTION SUPPRESSION DE PRODUIT
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
            
            
    #SECTION VENTE DE PRODUIT
    def show_product_available(self):
        self.clear_widgets()
        self.products_available()

    def products_available(self):
        self.clear_widgets()
        
        label_products_available = tk.Label(self.root, text="Produits en stock", font=("Helvetica", 16))
        label_products_available.pack(pady=10)

        self.mytree()  # Créer un nouveau Treeview

        products = self.products_list_in_stock()
        for i, product in enumerate(products):
            self.tree.insert("", i, values=(product[0], product[1], product[2], product[3]))

        self.tree.pack(pady=10)
        
        self.label_selling = tk.Label(self.root, text="Selectionner un produit et metter la quantité ici:", font=("Helvetica", 12))
        self.entry_selling_quantity = tk.Entry(self.root, font=("Helvetica", 12))

        self.label_selling.pack(padx=10, pady=10)
        self.entry_selling_quantity.pack(padx=10, pady=10)
        
        self.btn_selling = tk.Button(self.root, text="Valider la vente", command=self.selling_product, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_selling.pack(pady=10)
        
        self.btn_back_home_page = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_home_page.pack(pady=10)
        
        self.btn_histories_products_sold = tk.Button(self.root, text="Statistiques et graphiques des ventes", command=self.show_products_sold_history, font=("Helvetica", 12))
        self.btn_histories_products_sold.pack(pady=10)

    def selling_product(self):
        selling_product = self.tree.selection()
        
        if selling_product:
            quantity = int(self.entry_selling_quantity.get())
            item_values = self.tree.item(selling_product, "values")
            product_id = item_values[0]
            product_stock = int(item_values[3])
            sold_by = self.current_user['id']
            
            today = datetime.now()
            sold_at = today.strftime('%Y-%m-%d %H:%M:%S') 
            
            if product_stock >= quantity:
                availableStock = product_stock - quantity

                cursor = self.conn.cursor()

                #Rajouté en base le produit vendu et sa qunatité
                valuesInserted = (product_id, quantity, sold_by, sold_at)
                saleQuery = "INSERT INTO sale (id_product, quantity_sold, sold_by, sold_at) VALUES(%s, %s, %s, %s)"
                cursor.execute(saleQuery, valuesInserted)
                self.conn.commit()
            
                # mettre à jour la quantité du produit en base de données
                updateProductSale = "UPDATE products SET stock=%s WHERE id=%s"
                cursor.execute(updateProductSale, (availableStock, product_id,))
                self.conn.commit()

                # Afficher un message de confirmation
                messagebox.showinfo("Succès", "produit vendu avec succès.")
                
                # Rediriger vers la page de produits en stock
                self.show_product_available()
            else:
                messagebox.showwarning("Sélection nécessaire", "vente impossible: Quantité entrée supérieur au stock disponible.")   

        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner un produit à vendre.")
        
    def products_list_in_stock(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, price, stock FROM products WHERE stock > 0 ORDER BY name ASC")
        products = cursor.fetchall()
        return products
    
    #SECTION DE L'HISTORIQUE DES VENTES
    def show_products_sold_history(self):
        self.clear_widgets()
        self.products_sold_history()

    def products_sold_history(self):
        self.clear_widgets()
        
        label_products_sold = tk.Label(self.root, text="Produits Vendus", font=("Helvetica", 16))
        label_products_sold.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Quantity", "Stock", "SoldBy", "SoldAt"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Nom du produit")
        self.tree.heading("Price", text="Prix")
        self.tree.heading("Quantity", text="Quantité vendue")
        self.tree.heading("Stock", text="Quantité en stock")
        self.tree.heading("SoldBy", text="Vendu par")
        self.tree.heading("SoldAt", text="Vendu le")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=220, anchor=tk.CENTER)
        self.tree.column("Price", width=120, anchor=tk.CENTER)
        self.tree.column("Quantity", width=220, anchor=tk.CENTER)
        self.tree.column("Stock", width=220, anchor=tk.CENTER)
        self.tree.column("SoldBy", width=220, anchor=tk.CENTER)
        self.tree.column("SoldAt", width=220, anchor=tk.CENTER)
        
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size

        histories = self.histories()
        for i, history in enumerate(histories[start_index:end_index], start=1):
            id = history[0]
            name = history[1]
            price = history[2]
            quantity_sold = history[3]
            stock_available = history[4]
            sold_by = history[5] + ' ' + history[6]
            sold_at = history[7].strftime('%Y-%m-%d %H:%M:%S')
            self.tree.insert("", i, values=(id, name, price, quantity_sold, stock_available, sold_by, sold_at))

        self.tree.pack(pady=10)
        
        # Ajouter des boutons pour naviguer entre les pages 
        self.btn_pre_page = tk.Button(self.root, text="Page précédente", command=self.show_pre_page, font=("Helvetica", 12))
        self.btn_pre_page.pack(pady=10)

        self.btn_aft_page = tk.Button(self.root, text="Page suivante", command=self.show_aft_page, font=("Helvetica", 12))
        self.btn_aft_page.pack(pady=10)
        
        self.btn_graphs_page = tk.Button(self.root, text="Voir les graphiques de ventes", command=self.show_graphics, font=("Helvetica", 12))
        self.btn_graphs_page.pack(pady=10)
        
        self.btn_back_home_page = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_home_page.pack(pady=10)
        
        self.btn_back_selling = tk.Button(self.root, text="Retour à la vente", command=self.show_product_available, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_back_selling.pack(pady=10)
    
    def show_pre_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.products_sold_history()

    def show_aft_page(self):
        total_pages = -(-len(self.histories()) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self.products_sold_history()
            
    def histories(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT s.id, p.name, p.price, quantity_sold, stock, u.first_name, u.last_name, sold_at 
                FROM sale AS s 
                INNER JOIN products AS p ON p.id = s.id_product
                INNER JOIN user AS u ON u.id = s.sold_by
                ORDER BY sold_at DESC
            """
        )
        histories = cursor.fetchall()
        return histories

    #SECTION GRAPHIQUES DES VENTES
    def tenBestSeller(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT p.name, sum(quantity_sold) as quantity_sold, sold_at
                FROM sale AS s
                INNER JOIN products AS p ON p.id = s.id_product
                GROUP BY p.name
                ORDER BY stock DESC
                LIMIT 10
            """
        )
        bestSeller = cursor.fetchall()
        return bestSeller

    def show_graphics(self):
        self.clear_widgets()
        self.draw_graphics()
    
    def draw_graphics(self):
        # Votre liste de données
        data = self.tenBestSeller()

        # Graphique 1: Diagramme à barres pour la quantité des 10 produits les vendus
        products_quantity = defaultdict(int)

        for item in data:
            product_name = item[0]
            quantity_sold = item[1]
            products_quantity[product_name] += quantity_sold

        # Création du diagramme à barres
        fig1, ax1 = plt.subplots(figsize=(8, 4))  # Taille ajustée
        ax1.bar(products_quantity.keys(), products_quantity.values())
        ax1.set_title('Quantité des 10 produits les vendus')
        ax1.set_xlabel('Produit')
        ax1.set_ylabel('Quantité vendue')
        
        # Utilisez set_xticklabels pour la rotation des étiquettes
        ax1.set_xticklabels(products_quantity.keys(), rotation=45, ha='right') 
        
        plt.tight_layout(pad=3.0) 

        # Graphique 2: Graphique linéaire pour l'évolution des 10 meilleurs produits vendus par jours
        sales_by_day = defaultdict(int)

        for item in data:
            sales_date = item[2].date()
            quantity_sold = item[1]
            sales_by_day[sales_date] += quantity_sold

        # Tri des données par date
        sorted_sales = sorted(sales_by_day.items())

        # Création du graphique linéaire
        fig2, ax2 = plt.subplots(figsize=(8, 4))  # Taille ajustée
        dates, quantities = zip(*sorted_sales)
        ax2.plot(dates, quantities, marker='o')
        ax2.set_title('Évolution des ventes en fonction des jours')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Quantité vendue')

        # Utilisez set_xticklabels pour la rotation des étiquettes
        ax2.set_xticklabels(dates, rotation=45, ha='right')  

        # Ajustements pour éviter le chevauchement
        plt.tight_layout(pad=3.0)

        # Intégration des graphiques dans l'interface Tkinter
        canvas1 = FigureCanvasTkAgg(fig1, master=self.root)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Bouton pour revenir à la page principale
        btn_back = tk.Button(self.root, text="Retour aux stats", command=self.show_products_sold_history, font=("Helvetica", 12), padx=10, pady=5)
        btn_back.pack(pady=10)