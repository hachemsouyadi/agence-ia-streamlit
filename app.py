import streamlit as st
from database.json_manager import JSONManager
from openai import OpenAI
import os
from dotenv import load_dotenv

# 🌍 Configuration
st.set_page_config(page_title="Agence IA", layout="centered", page_icon="🌍")
load_dotenv()
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
json_mgr = JSONManager()

# 📦 Chargement des données
data = json_mgr.charger()
clients = data.get("clients", [])
offres = data.get("offres", [])
reservations = data.get("reservations", [])

# 🔄 Sauvegarde automatique
def save_all():
    json_mgr.enregistrer({
        "clients": clients,
        "offres": offres,
        "reservations": reservations
    })

# 🧭 Barre latérale
st.sidebar.title("📂 Menu de navigation")
menu = st.sidebar.radio(
    "Aller vers",
    ["🏠 Accueil", "👤 Client", "🌴 Offre", "📆 Réservation", "🤖 Agent IA", "📊 Données", "🗑️ Réinitialiser"]
)


# 🏠 Accueil
if menu == "🏠 Accueil":
    st.title("🌍 Bienvenue dans l'Agence de Voyage IA")
    st.markdown("Ce tableau de bord vous permet de gérer vos clients, offres et réservations avec l'aide d'une intelligence artificielle ✈️.")
    st.image("accueil.jpg", width=300)

# 👤 Ajouter client
elif menu == "👤 Client":
    st.markdown("## 👤 Ajouter un client")
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom du client")
    with col2:
        email = st.text_input("Email")

    if st.button("✅ Ajouter le client"):
        if nom and email:
            clients.append({"nom": nom, "email": email})
            save_all()
            st.success(f"Client **{nom}** ajouté avec succès !")
        else:
            st.warning("Veuillez remplir les deux champs.")

# 🌴 Ajouter offre
elif menu == "🌴 Offre":
    st.markdown("## 🌴 Ajouter une offre de voyage")
    col1, col2 = st.columns(2)
    with col1:
        titre = st.text_input("Titre de l'offre")
        ville = st.text_input("Ville")
    with col2:
        pays = st.text_input("Pays")
        continent = st.text_input("Continent")
    prix = st.number_input("Prix (€)", min_value=0.0)

    if st.button("✅ Ajouter l'offre"):
        if all([titre, ville, pays, continent]):
            offres.append({
                "titre": titre,
                "ville": ville,
                "pays": pays,
                "continent": continent,
                "prix": prix
            })
            save_all()
            st.success(f"Offre **{titre}** ajoutée avec succès !")
        else:
            st.warning("Tous les champs sont requis.")

# 📆 Réservation
elif menu == "📆 Réservation":
    st.markdown("## 📆 Créer une réservation")
    if not clients or not offres:
        st.info("Ajoutez d'abord des clients et des offres.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            client_nom = st.selectbox("Nom du client", [c["nom"] for c in clients])
        with col2:
            offre_titre = st.selectbox("Offre disponible", [o["titre"] for o in offres])

        if st.button("📥 Réserver"):
            reservations.append({
                "client": client_nom,
                "offre": offre_titre
            })
            save_all()
            st.success(f"Réservation pour **{client_nom}** vers **{offre_titre}** confirmée ✅")

# 🤖 Agent IA
elif menu == "🤖 Agent IA":
    st.markdown("## 🤖 Posez une question à l’agent IA")
    question = st.text_area("Votre question...")
    if st.button("✉️ Envoyer"):
        with st.spinner("Agent IA réfléchit..."):
            try:
                response = client_ai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un agent de voyage professionnel qui conseille les clients."},
                        {"role": "user", "content": question}
                    ]
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Erreur : {e}")

# 📊 Données sauvegardées
elif menu == "📊 Données":
    st.markdown("## 📊 Données enregistrées")
    st.subheader("👥 Clients")
    if clients:
        st.table(clients)
    else:
        st.info("Aucun client enregistré.")

    st.subheader("🌐 Offres")
    if offres:
        st.table(offres)
    else:
        st.info("Aucune offre enregistrée.")

    st.subheader("📆 Réservations")
    if reservations:
        st.table(reservations)
    else:
        st.info("Aucune réservation enregistrée.")

# 🗑️ Réinitialisation
elif menu == "🗑️ Réinitialiser":
    st.markdown("## 🧹 Réinitialiser toutes les données")
    if st.button("⚠️ Tout supprimer maintenant"):
        clients.clear()
        offres.clear()
        reservations.clear()
        save_all()
        st.success("✅ Toutes les données ont été supprimées.")