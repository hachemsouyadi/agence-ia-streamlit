from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.client import Client
from models.pays import Pays
from models.destination import Destination
from models.offre import Offre
from models.reservation import Reservation
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("frontend"):
    os.makedirs("frontend")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/ui")
def show_ui():
    return FileResponse("frontend/index.html")

class ClientIn(BaseModel):
    nom: str
    email: str

class OffreIn(BaseModel):
    titre: str
    ville: str
    pays: str
    continent: str
    prix: float

class ReservationIn(BaseModel):
    nom_client: str
    titre_offre: str

class Question(BaseModel):
    question: str

clients = []
offres = []
reservations = []

@app.get("/")
def welcome():
    return {"message": "Bienvenue sur l'API de l'agence de voyage"}

@app.post("/clients")
def ajouter_client(client: ClientIn):
    c = Client(client.nom, client.email)
    clients.append(c)
    return {"message": f"Client {c.nom} ajouté"}

@app.post("/offres")
def ajouter_offre(offre: OffreIn):
    pays = Pays(offre.pays, offre.continent)
    destination = Destination(offre.ville, pays)
    o = Offre(offre.titre, destination, offre.prix)
    offres.append(o)
    return {"message": f"Offre '{o.titre}' ajoutée"}

@app.post("/reservations")
def reserver(data: ReservationIn):
    client = next((c for c in clients if c.nom == data.nom_client), None)
    offre = next((o for o in offres if o.titre == data.titre_offre), None)
    if client and offre:
        r = Reservation(client, offre)
        reservations.append(r)
        return {"message": f"Réservation confirmée pour {client.nom} vers {offre.destination.ville}"}
    return {"error": "Client ou offre introuvable"}

@app.post("/question")
def ask_ai(data: Question):
    try:
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un agent de voyage intelligent qui conseille les clients."},
                {"role": "user", "content": data.question}
            ]
        )
        return {"réponse": chat_response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
