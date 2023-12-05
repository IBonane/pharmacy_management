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

    def show_product_management_page(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.product_management_page()

        btn_back_home = tk.Button(self.root, text="Retour à l'accueil", command=self.home_page, font=("Helvetica", 12), padx=10, pady=5)
        btn_back_home.pack(pady=10)

    def product_management_page(self):
        label_manage_products = tk.Label(self.root, text="Gestion des produits", font=("Helvetica", 16))
        label_manage_products.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Nom du produit")
        self.tree.heading("Price", text="Prix")
        self.tree.heading("Quantity", text="Quantité en stock")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=220, anchor=tk.CENTER)
        self.tree.column("Price", width=120, anchor=tk.CENTER)
        self.tree.column("Quantity", width=220, anchor=tk.CENTER)

        self.show_products_on_page()

        for col in ["ID", "Name", "Price", "Quantity"]:
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(pady=10)

        btn_edit_product = tk.Button(self.root, text="Éditer le produit", command=self.edit_product, font=("Helvetica", 12))
        btn_edit_product.pack(pady=10)

        btn_delete_product = tk.Button(self.root, text="Supprimer le produit", command=self.delete_product, font=("Helvetica", 12), fg="red")
        btn_delete_product.pack(pady=10)

        # Ajouter des boutons pour naviguer entre les pages
        btn_prev_page = tk.Button(self.root, text="Page précédente", command=self.show_previous_page, font=("Helvetica", 12))
        btn_prev_page.pack(pady=10)

        btn_next_page = tk.Button(self.root, text="Page suivante", command=self.show_next_page, font=("Helvetica", 12))
        btn_next_page.pack(pady=10)

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
        cursor.execute("SELECT id, name, price, stock FROM products;")
        products = cursor.fetchall()
        return products

    def edit_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_id = item_values[0]
            product_name = item_values[1]
            product_quantity = item_values[2]
            print(f"Éditer le produit : ID={product_id}, Nom={product_name}, Quantité={product_quantity}")
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner un produit à éditer.")

    def delete_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_id = item_values[0]
            product_name = item_values[1]
            print(f"Supprimer le produit : ID={product_id}, Nom={product_name}")
        else:
            messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner un produit à supprimer.")
