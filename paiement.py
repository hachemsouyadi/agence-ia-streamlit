class Paiement:
    def __init__(self, reservation, montant):
        self.reservation = reservation
        self.montant = montant

    def effectuer(self):
        if self.montant >= self.reservation.offre.prix:
            print(f"💳 Paiement de {self.montant}€ effectué avec succès pour {self.reservation.client.nom}")
        else:
            print("❌ Paiement insuffisant!")