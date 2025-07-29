from pydantic import BaseModel

class OffreIn(BaseModel):
    titre: str
    ville: str
    pays: str
    continent: str
    prix: float