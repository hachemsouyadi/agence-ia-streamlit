class Pays:
    def __init__(self, nom, continent):
        self.nom = nom
        self.continent = continent

    def afficher_info(self):
        print(f"Pays: {self.nom} ({self.continent})")