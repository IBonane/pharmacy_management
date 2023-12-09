import tkinter as tk
from user import User
from product import Product

class PharmacyApp(User, Product):
    def __init__(self, root):
        # Appeler le constructeur de la classe User et Product
        User.__init__(self, root)
        Product.__init__(self, root)


        self.root = root
        self.root.title("Pharmacy Management System")

        # Interface utilisateur
        self.home_page()

    def home_page(self):
        # Oublie la page précédente
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Ajuster la taille
        self.root.geometry("1200x920")

        # Éléments de la page d'accueil
        self.label_welcome = tk.Label(self.root, text="Bienvenue dans le système de gestion de pharmacie", font=("Helvetica", 14))

        if self.is_logged_in:
            self.label_welcome.pack(pady=10)
            
            if self.current_user['is_admin']:
                self.label_status = tk.Label(self.root, text="Connecté en tant que Pharmacien en Chef", font=("Helvetica", 12))
                self.label_status.pack(pady=10)
            else:
                self.label_status = tk.Label(self.root, text="Connecté en tant que Pharmacien", font=("Helvetica", 12))
                self.label_status.pack(pady=10)

            self.btn_view_profile = tk.Button(self.root, text="Voir le profil", command=self.show_profile, font=("Helvetica", 12))
            self.btn_view_profile.pack(pady=10)
            
            self.btn_manage_products = tk.Button(self.root, text="Gérer les produits", command=self.show_product_management_page, font=("Helvetica", 12))
            self.btn_manage_products.pack(pady=10)
            
            self.btn_selling_products = tk.Button(self.root, text="Vendre des produits", command=self.show_product_available, font=("Helvetica", 12))
            self.btn_selling_products.pack(pady=10)
            
            self.btn_histories_products_sold = tk.Button(self.root, text="Statistiques et graphiques des ventes", command=self.show_products_sold_history, font=("Helvetica", 12))
            self.btn_histories_products_sold.pack(pady=10)
            
            if self.current_user['is_admin'] == 1:
                self.btn_manage_products = tk.Button(self.root, text="Gérer les pharmaciens", command=self.pharmacist_management_page, font=("Helvetica", 12))
                self.btn_manage_products.pack(pady=10)

            self.btn_logout = tk.Button(self.root, text="Déconnexion", command=self.logout, font=("Helvetica", 12))
            self.btn_logout.pack(pady=10)
        else:
            self.btn_register = tk.Button(self.root, text="S'inscrire", command=self.show_registration_page, font=("Helvetica", 12), padx=10, pady=5)
            self.btn_register.pack(pady=10)

            self.btn_login = tk.Button(self.root, text="Se connecter", command=self.show_login_page, font=("Helvetica", 12), padx=10, pady=5)
            self.btn_login.pack(pady=10)
            
        self.btn_quit = tk.Button(self.root, text="Quitter", command=self.root.destroy, font=("Helvetica", 12), padx=10, pady=5)
        self.btn_quit.pack(pady=30)

        # Ajouter une image
        self.img_pharmacy = tk.PhotoImage(file="pharmacie/assets/img/pharma.png") 
        self.label_image = tk.Label(self.root, image=self.img_pharmacy)
        self.label_image.image = self.img_pharmacy
        self.label_image.pack(pady=20)

        # Ajouter un effet de survol sur les boutons
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.config(bg="#7fcce5"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.config(bg="white"))

        self.btn_login.bind("<Enter>", lambda e: self.btn_login.config(bg="#7fcce5"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.config(bg="white"))

        if self.is_logged_in:
            self.btn_logout.bind("<Enter>", lambda e: self.btn_logout.config(bg="#7fcce5"))
            self.btn_logout.bind("<Leave>", lambda e: self.btn_logout.config(bg="white"))
            
if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()