class Destination:
    def __init__(self, ville, pays):
        self.ville = ville
        self.pays = pays

    def afficher_info(self):
        print(f"Destination: {self.ville}, {self.pays.nom}")