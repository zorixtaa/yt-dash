import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="YouTube Automation Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Titre et introduction
st.title("YouTube Automation Dashboard")
st.markdown("Système d'automatisation pour chaînes YouTube ciblant les pays anglophones à fort CPM")

# Interface simple
st.header("Configuration")
colab_url = st.text_input("URL du notebook Google Colab")
if st.button("Connecter à Google Colab"):
    if colab_url:
        st.success("Connexion simulée à Google Colab réussie!")
    else:
        st.error("Veuillez entrer l'URL du notebook Google Colab")

# Affichage des pays cibles
st.header("Pays cibles (anglophones à fort CPM)")
countries = ["US", "CA", "GB", "AU"]
st.write(", ".join(countries))

# Tableau de données simple
st.header("Niches à fort CPM")
data = {
    "Niche": ["Passive Income", "SaaS Tools", "AI for Content Creators"],
    "CPM Score": [9.6, 9.1, 8.4],
    "Opportunity": ["Élevée", "Moyenne", "Élevée"]
}
df = pd.DataFrame(data)
st.dataframe(df)

# Informations sur le système
st.sidebar.title("Navigation")
st.sidebar.selectbox("Sélectionnez une page", ["Accueil", "Configuration", "Niches", "Vidéos", "Performance"])
st.sidebar.markdown("---")
st.sidebar.markdown("### Système d'automatisation YouTube")
st.sidebar.markdown("Version 1.0")
st.sidebar.markdown("© 2025")
