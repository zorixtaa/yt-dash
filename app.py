import streamlit as st
import pandas as pd
import json
import requests
import time
import os
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="YouTube Automation Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF0000;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #606060;
    }
    .status-ok {
        color: #00CC00;
        font-weight: bold;
    }
    .status-warning {
        color: #FFA500;
        font-weight: bold;
    }
    .status-error {
        color: #FF0000;
        font-weight: bold;
    }
    .metric-card {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Fonctions d'initialisation
def initialize_session_state():
    if 'colab_url' not in st.session_state:
        st.session_state.colab_url = ""
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False
    if 'youtube_credentials' not in st.session_state:
        st.session_state.youtube_credentials = {
            "api_key": "",
            "client_id": "",
            "client_secret": "",
            "refresh_token": ""
        }
    if 'target_countries' not in st.session_state:
        st.session_state.target_countries = ["US", "CA", "GB", "AU"]
    if 'current_niches' not in st.session_state:
        st.session_state.current_niches = []
    if 'videos' not in st.session_state:
        st.session_state.videos = []
    if 'performance_data' not in st.session_state:
        st.session_state.performance_data = []

# Fonctions d'API
def connect_to_colab_api(colab_url):
    try:
        # Simuler la connexion à l'API Colab
        st.session_state.api_connected = True
        st.success("Connexion à Google Colab établie avec succès!")
        return True
    except Exception as e:
        st.error(f"Erreur de connexion à Google Colab: {str(e)}")
        return False

def get_api_status():
    if not st.session_state.api_connected:
        return "Non connecté"
    
    # Simuler un statut d'API
    return "Connecté et opérationnel"

def find_niches(limit=5):
    if not st.session_state.api_connected:
        st.error("Veuillez d'abord connecter l'API Colab")
        return []
    
    # Simuler la recherche de niches
    niches = [
        {
            "id": 1,
            "name": "Passive Income for Beginners",
            "category": "finance",
            "cpm_score": 9.6,
            "competition_score": 7.8,
            "trend_score": 8.5,
            "opportunity_score": 8.7,
            "keywords": ["passive income", "investing for beginners", "financial freedom", "side hustle"],
            "target_countries": st.session_state.target_countries
        },
        {
            "id": 2,
            "name": "SaaS Tools for Small Business",
            "category": "business",
            "cpm_score": 9.1,
            "competition_score": 7.2,
            "trend_score": 8.3,
            "opportunity_score": 8.3,
            "keywords": ["saas tools", "small business software", "productivity tools", "business automation"],
            "target_countries": st.session_state.target_countries
        },
        {
            "id": 3,
            "name": "AI Tools for Content Creators",
            "category": "technology",
            "cpm_score": 8.4,
            "competition_score": 6.9,
            "trend_score": 9.2,
            "opportunity_score": 8.2,
            "keywords": ["ai tools", "content creation", "artificial intelligence", "creator economy"],
            "target_countries": st.session_state.target_countries
        }
    ]
    
    st.session_state.current_niches = niches[:limit]
    return niches[:limit]

def generate_content(niche_id, video_type="standard"):
    if not st.session_state.api_connected:
        st.error("Veuillez d'abord connecter l'API Colab")
        return None
    
    # Trouver la niche correspondante
    niche = next((n for n in st.session_state.current_niches if n["id"] == niche_id), None)
    if not niche:
        st.error(f"Niche ID {niche_id} non trouvée")
        return None
    
    # Simuler la génération de contenu
    video_id = len(st.session_state.videos) + 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    video = {
        "id": video_id,
        "niche_id": niche_id,
        "niche_name": niche["name"],
        "title": f"How {niche['keywords'][0]} Can Transform Your {niche['category']} Strategy",
        "description": f"In this video, we explore {niche['name']} and how it can help you achieve your goals.",
        "script_path": f"data/output/scripts/script_{niche_id}_{timestamp}.txt",
        "audio_path": f"data/output/audio/audio_{niche_id}_{timestamp}.wav",
        "video_path": None,
        "thumbnail_path": None,
        "youtube_id": None,
        "status": "script_generated",
        "created_at": datetime.now().isoformat(),
        "published_at": None
    }
    
    st.session_state.videos.append(video)
    return video

def produce_video(video_id):
    if not st.session_state.api_connected:
        st.error("Veuillez d'abord connecter l'API Colab")
        return None
    
    # Trouver la vidéo correspondante
    video_index = next((i for i, v in enumerate(st.session_state.videos) if v["id"] == video_id), None)
    if video_index is None:
        st.error(f"Vidéo ID {video_id} non trouvée")
        return None
    
    # Simuler la production vidéo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    st.session_state.videos[video_index]["video_path"] = f"data/output/video/video_{video_id}_{timestamp}.mp4"
    st.session_state.videos[video_index]["thumbnail_path"] = f"data/output/thumbnails/thumbnail_{video_id}_{timestamp}.jpg"
    st.session_state.videos[video_index]["status"] = "video_produced"
    
    return st.session_state.videos[video_index]

def publish_video(video_id):
    if not st.session_state.api_connected:
        st.error("Veuillez d'abord connecter l'API Colab")
        return None
    
    # Trouver la vidéo correspondante
    video_index = next((i for i, v in enumerate(st.session_state.videos) if v["id"] == video_id), None)
    if video_index is None:
        st.error(f"Vidéo ID {video_id} non trouvée")
        return None
    
    # Vérifier que la vidéo est produite
    if st.session_state.videos[video_index]["status"] != "video_produced":
        st.error(f"La vidéo ID {video_id} n'est pas encore produite")
        return None
    
    # Simuler la publication
    youtube_id = f"yt{video_id}_{int(time.time())}"
    
    st.session_state.videos[video_index]["youtube_id"] = youtube_id
    st.session_state.videos[video_index]["status"] = "published"
    st.session_state.videos[video_index]["published_at"] = datetime.now().isoformat()
    
    return st.session_state.videos[video_index]

def analyze_performance(video_id=None):
    if not st.session_state.api_connected:
        st.error("Veuillez d'abord connecter l'API Colab")
        return None
    
    # Si video_id est spécifié, analyser uniquement cette vidéo
    if video_id:
        video_index = next((i for i, v in enumerate(st.session_state.videos) if v["id"] == video_id), None)
        if video_index is None:
            st.error(f"Vidéo ID {video_id} non trouvée")
            return None
        
        if st.session_state.videos[video_index]["status"] != "published":
            st.error(f"La vidéo ID {video_id} n'est pas encore publiée")
            return None
        
        videos_to_analyze = [st.session_state.videos[video_index]]
    else:
        # Analyser toutes les vidéos publiées
        videos_to_analyze = [v for v in st.session_state.videos if v["status"] == "published"]
    
    if not videos_to_analyze:
        st.error("Aucune vidéo publiée à analyser")
        return None
    
    performance_data = []
    
    for video in videos_to_analyze:
        # Simuler des données de performance
        views = int(1000 + 9000 * video["id"] * 0.5 * (0.5 + 0.5 * (datetime.now() - datetime.fromisoformat(video["published_at"])).days / 7))
        ctr = 4.0 + (video["id"] % 4)
        watch_time = 200 + 100 * (video["id"] % 4)
        likes = int(views * 0.1)
        comments = int(views * 0.02)
        
        # Obtenir la niche pour le CPM
        niche = next((n for n in st.session_state.current_niches if n["id"] == video["niche_id"]), None)
        cpm_score = niche["cpm_score"] if niche else 5.0
        
        # Estimer le CPM et les revenus
        estimated_cpm = cpm_score
        estimated_revenue = round((views / 1000) * estimated_cpm, 2)
        
        # Générer des données par pays
        country_data = {}
        for country in st.session_state.target_countries:
            if country == "US":
                country_views = int(views * 0.5)
            elif country == "GB":
                country_views = int(views * 0.2)
            elif country == "CA":
                country_views = int(views * 0.15)
            elif country == "AU":
                country_views = int(views * 0.1)
            else:
                country_views = int(views * 0.05)
            
            country_data[country] = {
                "views": country_views,
                "watch_time": int(watch_time * (country_views / views)),
                "estimated_revenue": round((country_views / 1000) * estimated_cpm, 2)
            }
        
        performance = {
            "video_id": video["id"],
            "youtube_id": video["youtube_id"],
            "title": video["title"],
            "views": views,
            "ctr": ctr,
            "watch_time": watch_time,
            "likes": likes,
            "comments": comments,
            "estimated_cpm": estimated_cpm,
            "estimated_revenue": estimated_revenue,
            "country_data": country_data,
            "measured_at": datetime.now().isoformat()
        }
        
        performance_data.append(performance)
    
    # Mettre à jour les données de performance
    st.session_state.performance_data = performance_data
    
    return performance_data

# Pages de l'application
def show_home_page():
    st.markdown("<h1 class='main-header'>YouTube Automation Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Système d'automatisation pour chaînes YouTube ciblant les pays anglophones à fort CPM</p>", unsafe_allow_html=True)
    
    # Statut du système
    st.markdown("## Statut du système")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### API Colab")
        api_status = get_api_status()
        status_class = "status-ok" if st.session_state.api_connected else "status-error"
        st.markdown(f"<p class='{status_class}'>{api_status}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### Niches identifiées")
        niche_count = len(st.session_state.current_niches)
        st.markdown(f"<p>{niche_count}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### Vidéos publiées")
        published_videos = len([v for v in st.session_state.videos if v["status"] == "published"])
        st.markdown(f"<p>{published_videos}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Actions rapides
    st.markdown("## Actions rapides")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Découvrir des niches", disabled=not st.session_state.api_connected):
            with st.spinner("Recherche de niches en cours..."):
                niches = find_niches(limit=5)
                st.success(f"{len(niches)} niches identifiées!")
    
    with col2:
        if st.button("Générer du contenu", disabled=not st.session_state.api_connected or len(st.session_state.current_niches) == 0):
            with st.spinner("Génération de contenu en cours..."):
                niche_id = st.session_state.current_niches[0]["id"]
                video = generate_content(niche_id)
                if video:
                    st.success(f"Contenu généré: {video['title']}")
    
    with col3:
        if st.button("Analyser les performances", disabled=not st.session_state.api_connected or len([v for v in st.session_state.videos if v["status"] == "published"]) == 0):
            with st.spinner("Analyse des performances en cours..."):
                performance_data = analyze_performance()
                if performance_data:
                    st.success(f"Analyse complétée pour {len(performance_data)} vidéos!")
    
    # Résumé des performances
    if st.session_state.performance_data:
        st.markdown("## Résumé des performances")
        
        total_views = sum(p["views"] for p in st.session_state.performance_data)
        total_revenue = sum(p["estimated_revenue"] for p in st.session_state.performance_data)
        avg_ctr = sum(p["ctr"] for p in st.session_state.performance_data) / len(st.session_state.performance_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown("### Vues totales")
            st.markdown(f"<p>{total_views:,}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown("### Revenus estimés")
            st.markdown(f"<p>${total_revenue:.2f}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown("### CTR moyen")
            st.markdown(f"<p>{avg_ctr:.1f}%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Graphique des vues par pays
        if st.session_state.performance_data:
            st.markdown("### Répartition des vues par pays")
            
            country_views = {}
            for country in st.session_state.target_countries:
                country_views[country] = 0
            
            for perf in st.session_state.performance_data:
                for country, data in perf["country_data"].items():
                    if country in country_views:
                        country_views[country] += data["views"]
            
            country_df = pd.DataFrame({
                "Pays": list(country_views.keys()),
                "Vues": list(country_views.values())
            })
            
            fig = px.bar(country_df, x="Pays", y="Vues", color="Pays")
            st.plotly_chart(fig, use_container_width=True)

def show_configuration_page():
    st.markdown("<h1 class='main-header'>Configuration</h1>", unsafe_allow_html=True)
    
    # Configuration de Google Colab
    st.markdown("## Configuration de Google Colab")
    
    colab_url = st.text_input("URL du notebook Google Colab", value=st.session_state.colab_url)
    
    if st.button("Connecter à Google Colab"):
        if colab_url:
            with st.spinner("Connexion à Google Colab en cours..."):
                if connect_to_colab_api(colab_url):
                    st.session_state.colab_url = colab_url
        else:
            st.error("Veuillez entrer l'URL du notebook Google Colab")
    
    # Configuration de l'API YouTube
    st.markdown("## Configuration de l'API YouTube")
    
    with st.form("youtube_api_form"):
        api_key = st.text_input("Clé API YouTube", value=st.session_state.youtube_credentials["api_key"])
        client_id = st.text_input("Client ID OAuth", value=st.session_state.youtube_credentials["client_id"])
        client_secret = st.text_input("Client Secret OAuth", value=st.session_state.youtube_credentials["client_secret"], type="password")
        refresh_token = st.text_input("Refresh Token", value=st.session_state.youtube_credentials["refresh_token"], type="password")
        
        submitted = st.form_submit_button("Enregistrer les identifiants")
        
        if submitted:
            st.session_state.youtube_credentials = {
                "api_key": api_key,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
            }
            st.success("Identifiants YouTube enregistrés avec succès!")
    
    # Configuration des pays cibles
    st.markdown("## Pays cibles")
    
    countries = ["US", "CA", "GB", "AU", "NZ", "IE"]
    selected_countries = st.multiselect(
        "Sélectionnez les pays cibles (anglophones à fort CPM)",
        options=countries,
        default=st.session_state.target_countries
    )
    
    if st.button("Enregistrer les pays cibles"):
        if selected_countries:
            st.session_state.target_countries = selected_countries
            st.success("Pays cibles enregistrés avec succès!")
        else:
            st.error("Veuillez sélectionner au moins un pays cible")

def show_niches_page():
    st.markdown("<h1 class='main-header'>Gestion des niches</h1>", unsafe_allow_html=True)
    
    # Découverte de niches
    st.markdown("## Découverte de niches")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("Découvrez des niches à fort CPM avec moins de concurrence dans les pays anglophones cibles.")
    
    with col2:
        limit = st.number_input("Nombre de niches à découvrir", min_value=1, max_value=10, value=5)
    
    if st.button("Découvrir des niches", disabled=not st.session_state.api_connected):
        with st.spinner("Recherche de niches en cours..."):
            niches = find_niches(limit=limit)
            st.success(f"{len(niches)} niches identifiées!")
    
    # Affichage des niches
    if st.session_state.current_niches:
        st.markdown("## Niches identifiées")
        
        for niche in st.session_state.current_niches:
            with st.expander(f"{niche['name']} (Score d'opportunité: {niche['opportunity_score']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Catégorie:** {niche['category']}")
                    st.markdown(f"**Score CPM:** {niche['cpm_score']}")
                    st.markdown(f"**Score de concurrence:** {niche['competition_score']}")
                    st.markdown(f"**Score de tendance:** {niche['trend_score']}")
                
                with col2:
                    st.markdown(f"**Mots-clés:** {', '.join(niche['keywords'])}")
                    st.markdown(f"**Pays cibles:** {', '.join(niche['target_countries'])}")
                
                if st.button(f"Générer du contenu pour cette niche", key=f"gen_content_{niche['id']}"):
                    with st.spinner("Génération de contenu en cours..."):
                        video = generate_content(niche['id'])
                        if video:
                            st.success(f"Contenu généré: {video['title']}")

def show_videos_page():
    st.markdown("<h1 class='main-header'>Gestion des vidéos</h1>", unsafe_allow_html=True)
    
    # Filtres
    st.markdown("## Filtres")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.multiselect(
            "Filtrer par statut",
            options=["script_generated", "video_produced", "published"],
            default=[]
        )
    
    with col2:
        niche_filter = st.multiselect(
            "Filtrer par niche",
            options=[n["name"] for n in st.session_state.current_niches],
            default=[]
        )
    
    # Filtrer les vidéos
    filtered_videos = st.session_state.videos
    
    if status_filter:
        filtered_videos = [v for v in filtered_videos if v["status"] in status_filter]
    
    if niche_filter:
        filtered_videos = [v for v in filtered_videos if v["niche_name"] in niche_filter]
    
    # Affichage des vidéos
    if filtered_videos:
        st.markdown("## Vidéos")
        
        for video in filtered_videos:
            with st.expander(f"{video['title']} (ID: {video['id']}, Statut: {video['status']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Niche:** {video['niche_name']}")
                    st.markdown(f"**Statut:** {video['status']}")
                    st.markdown(f"**Créé le:** {datetime.fromisoformat(video['created_at']).strftime('%Y-%m-%d %H:%M')}")
                    
                    if video["published_at"]:
                        st.markdown(f"**Publié le:** {datetime.fromisoformat(video['published_at']).strftime('%Y-%m-%d %H:%M')}")
                    
                    if video["youtube_id"]:
                        st.markdown(f"**ID YouTube:** {video['youtube_id']}")
                        st.markdown(f"**URL YouTube:** https://youtu.be/{video['youtube_id']}") 
                
                with col2:
                    if video["status"] == "script_generated":
                        if st.button(f"Produire cette vidéo", key=f"produce_{video['id']}"):
                            with st.spinner("Production de la vidéo en cours..."):
                                produced_video = produce_video(video['id'])
                                if produced_video:
                                    st.success(f"Vidéo produite avec succès!")
                    
                    elif video["status"] == "video_produced":
                        if st.button(f"Publier cette vidéo", key=f"publish_{video['id']}"):
                            with st.spinner("Publication de la vidéo en cours..."):
                                published_video = publish_video(video['id'])
                                if published_video:
                                    st.success(f"Vidéo publiée avec succès! URL: https://youtu.be/{published_video['youtube_id']}") 
                    
                    elif video["status"] == "published":
                        if st.button(f"Analyser les performances", key=f"analyze_{video['id']}"):
                            with st.spinner("Analyse des performances en cours..."):
                                performance_data = analyze_performance(video['id'])
                                if performance_data:
                                    st.success(f"Analyse des performances complétée!")
                
                st.markdown("### Description")
                st.text_area("", value=video["description"], height=100, key=f"desc_{video['id']}", disabled=True)

def show_performance_page():
    st.markdown("<h1 class='main-header'>Analyse des performances</h1>", unsafe_allow_html=True)
    
    # Actions
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("Analysez les performances de vos vidéos YouTube pour optimiser votre stratégie.")
    
    with col2:
        if st.button("Actualiser les données", disabled=not st.session_state.api_connected):
            with st.spinner("Actualisation des données de performance..."):
                performance_data = analyze_performance()
                if performance_data:
                    st.success(f"Données actualisées pour {len(performance_data)} vidéos!")
    
    # Affichage des performances
    if st.session_state.performance_data:
        # Créer un DataFrame pour l'affichage
        perf_data = []
        for perf in st.session_state.performance_data:
            perf_data.append({
                "ID": perf["video_id"],
                "Titre": perf["title"],
                "Vues": perf["views"],
                "CTR (%)": perf["ctr"],
                "Temps de visionnage (s)": perf["watch_time"],
                "Likes": perf["likes"],
                "Commentaires": perf["comments"],
                "CPM estimé ($)": perf["estimated_cpm"],
                "Revenus estimés ($)": perf["estimated_revenue"]
            })
        
        df = pd.DataFrame(perf_data)
        st.dataframe(df)
        
        # Graphiques
        st.markdown("## Graphiques de performance")
        
        tab1, tab2, tab3 = st.tabs(["Vues", "Revenus", "Engagement"])
        
        with tab1:
            # Graphique des vues
            st.markdown("### Vues par vidéo")
            
            fig = px.bar(
                df,
                x="Titre",
                y="Vues",
                color="Vues",
                labels={"Vues": "Nombre de vues", "Titre": "Titre de la vidéo"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Graphique des vues par pays
            st.markdown("### Répartition des vues par pays")
            
            country_data = []
            for perf in st.session_state.performance_data:
                for country, data in perf["country_data"].items():
                    country_data.append({
                        "Pays": country,
                        "Vidéo": perf["title"],
                        "Vues": data["views"]
                    })
            
            country_df = pd.DataFrame(country_data)
            
            fig = px.bar(
                country_df,
                x="Pays",
                y="Vues",
                color="Vidéo",
                barmode="group",
                labels={"Vues": "Nombre de vues", "Pays": "Pays"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Graphique des revenus
            st.markdown("### Revenus estimés par vidéo")
            
            fig = px.bar(
                df,
                x="Titre",
                y="Revenus estimés ($)",
                color="Revenus estimés ($)",
                labels={"Revenus estimés ($)": "Revenus ($)", "Titre": "Titre de la vidéo"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Graphique des revenus par pays
            st.markdown("### Répartition des revenus par pays")
            
            country_revenue = []
            for perf in st.session_state.performance_data:
                for country, data in perf["country_data"].items():
                    country_revenue.append({
                        "Pays": country,
                        "Vidéo": perf["title"],
                        "Revenus": data["estimated_revenue"]
                    })
            
            country_rev_df = pd.DataFrame(country_revenue)
            
            fig = px.bar(
                country_rev_df,
                x="Pays",
                y="Revenus",
                color="Vidéo",
                barmode="group",
                labels={"Revenus": "Revenus estimés ($)", "Pays": "Pays"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Graphique d'engagement
            st.markdown("### Métriques d'engagement par vidéo")
            
            engagement_df = df[["Titre", "CTR (%)", "Likes", "Commentaires"]].copy()
            
            fig = px.bar(
                engagement_df,
                x="Titre",
                y=["CTR (%)", "Likes", "Commentaires"],
                barmode="group",
                labels={"value": "Valeur", "Titre": "Titre de la vidéo", "variable": "Métrique"}
            )
            st.plotly_chart(fig, use_container_width=True)

def show_logs_page():
    st.markdown("<h1 class='main-header'>Logs du système</h1>", unsafe_allow_html=True)
    
    # Simuler des logs
    logs = [
        {"timestamp": "2025-03-21 12:00:00", "level": "INFO", "message": "Système initialisé"},
        {"timestamp": "2025-03-21 12:05:23", "level": "INFO", "message": "Connexion à l'API Colab établie"},
        {"timestamp": "2025-03-21 12:10:45", "level": "INFO", "message": "Recherche de niches démarrée"},
        {"timestamp": "2025-03-21 12:12:30", "level": "INFO", "message": "5 niches identifiées"},
        {"timestamp": "2025-03-21 12:15:10", "level": "INFO", "message": "Génération de contenu pour la niche 'Passive Income for Beginners'"},
        {"timestamp": "2025-03-21 12:18:45", "level": "INFO", "message": "Script généré avec succès"},
        {"timestamp": "2025-03-21 12:20:15", "level": "INFO", "message": "Conversion TTS démarrée"},
        {"timestamp": "2025-03-21 12:22:30", "level": "INFO", "message": "Audio généré avec succès"},
        {"timestamp": "2025-03-21 12:25:00", "level": "INFO", "message": "Production vidéo démarrée"},
        {"timestamp": "2025-03-21 12:30:45", "level": "INFO", "message": "Vidéo produite avec succès"},
        {"timestamp": "2025-03-21 12:35:20", "level": "INFO", "message": "Publication YouTube démarrée"},
        {"timestamp": "2025-03-21 12:38:10", "level": "INFO", "message": "Vidéo publiée avec succès"},
        {"timestamp": "2025-03-21 13:00:00", "level": "INFO", "message": "Analyse des performances démarrée"},
        {"timestamp": "2025-03-21 13:02:15", "level": "INFO", "message": "Analyse des performances complétée"}
    ]
    
    # Filtres
    col1, col2 = st.columns(2)
    
    with col1:
        level_filter = st.multiselect(
            "Filtrer par niveau",
            options=["INFO", "WARNING", "ERROR"],
            default=["INFO", "WARNING", "ERROR"]
        )
    
    with col2:
        search_term = st.text_input("Rechercher dans les logs")
    
    # Filtrer les logs
    filtered_logs = logs
    
    if level_filter:
        filtered_logs = [log for log in filtered_logs if log["level"] in level_filter]
    
    if search_term:
        filtered_logs = [log for log in filtered_logs if search_term.lower() in log["message"].lower()]
    
    # Affichage des logs
    st.markdown("## Logs du système")
    
    log_df = pd.DataFrame(filtered_logs)
    st.dataframe(log_df, use_container_width=True)

# Fonction principale
def main():
    # Initialiser l'état de session
    initialize_session_state()
    
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    
    page = st.sidebar.selectbox(
        "Sélectionnez une page",
        ["Accueil", "Configuration", "Niches", "Vidéos", "Performance", "Logs"]
    )
    
    # Afficher la page sélectionnée
    if page == "Accueil":
        show_home_page()
    elif page == "Configuration":
        show_configuration_page()
    elif page == "Niches":
        show_niches_page()
    elif page == "Vidéos":
        show_videos_page()
    elif page == "Performance":
        show_performance_page()
    elif page == "Logs":
        show_logs_page()
    
    # Afficher le statut de connexion dans la sidebar
    st.sidebar.markdown("---")
    
    if st.session_state.api_connected:
        st.sidebar.markdown("🟢 **API Colab connectée**")
    else:
        st.sidebar.markdown("🔴 **API Colab non connectée**")
    
    # Informations sur le système
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Système d'automatisation YouTube")
    st.sidebar.markdown("Version 1.0")
    st.sidebar.markdown("Cible : Pays anglophones à fort CPM")
    st.sidebar.markdown("© 2025 - Tous droits réservés")

if __name__ == "__main__":
    main()
