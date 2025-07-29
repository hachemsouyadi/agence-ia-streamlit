class Client:
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email

    def afficher_info(self):
        print(f"Client: {self.nom} | Email: {self.email}")