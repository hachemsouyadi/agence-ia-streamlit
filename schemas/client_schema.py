from pydantic import BaseModel

class ClientIn(BaseModel):
    nom: str
    email: str