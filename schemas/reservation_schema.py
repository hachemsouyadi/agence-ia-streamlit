from pydantic import BaseModel

class ReservationIn(BaseModel):
    nom_client: str
    titre_offre: str