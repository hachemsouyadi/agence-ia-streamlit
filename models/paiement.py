class Paiement:
    def __init__(self, reservation, montant):
        self.reservation = reservation
        self.montant = montant

    def effectuer(self):
        if self.montant >= self.reservation.offre.prix:
            return f"💳 Paiement de {self.montant}€ effectué avec succès"
        else:
            return "❌ Paiement insuffisant!"