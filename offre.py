class Offre:
    def __init__(self, titre, destination, prix):
        self.titre = titre
        self.destination = destination
        self.prix = prix

    def afficher_info(self):
        print(f"Offre: {self.titre} - {self.destination.ville} à {self.prix}€")