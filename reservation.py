class Reservation:
    def __init__(self, client, offre):
        self.client = client
        self.offre = offre

    def confirmer(self):
        print(f"✅ Réservation confirmée pour {self.client.nom} vers {self.offre.destination.ville}")