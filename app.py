import streamlit as st
import os
from datetime import datetime, timedelta
import sys

# Ajouter le répertoire calcule_Heure au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'calcule_Heure'))

from graphique import generer_graphiques
from add_data import ajouter_donnees
from colcul import calculer_moyennes
from open_csv import lire_horaires

# Configuration de la page
st.set_page_config(
    page_title="Gestion des Horaires",
    page_icon="⏰",
    layout="wide"
)

# Titre principal
st.title("⏰ Application de Gestion des Horaires")
st.markdown("---")

fichier_csv = 'calcule_Heure/horaires.csv'

# Création d'onglets
tab1, tab2 = st.tabs(["📝 Ajouter une Saisie", "📊 Analyser les Données"])

# ========== ONGLET 1 : AJOUTER UNE SAISIE ==========
with tab1:
    st.header("Ajouter une nouvelle saisie")
    st.write("Entrez vos horaires de travail pour calculer automatiquement l'heure de départ.")

    # Formulaire de saisie
    with st.form("formulaire_horaires"):
        col1, col2, col3 = st.columns(3)

        with col1:
            heure_debut = st.time_input(
                "Heure de début de travail",
                value=datetime.strptime("08:00", "%H:%M").time()
            )

        with col2:
            heure_pause_debut = st.time_input(
                "Heure de début de pause",
                value=datetime.strptime("12:00", "%H:%M").time()
            )

        with col3:
            heure_pause_fin = st.time_input(
                "Heure de fin de pause",
                value=datetime.strptime("12:45", "%H:%M").time()
            )

        submitted = st.form_submit_button("💾 Enregistrer et Calculer")

        if submitted:
            # Conversion en format string HH:MM
            debut_str = heure_debut.strftime("%H:%M")
            pause_debut_str = heure_pause_debut.strftime("%H:%M")
            pause_fin_str = heure_pause_fin.strftime("%H:%M")

            try:
                # Calcul de l'heure de départ
                heure_depart = ajouter_donnees(debut_str, pause_debut_str, pause_fin_str)

                st.success(f"✅ Données enregistrées avec succès!")
                st.info(f"🕐 **Vous devez partir à : {heure_depart}**")

                # Afficher les informations saisies
                st.subheader("Récapitulatif")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Début de travail", debut_str)
                with col2:
                    st.metric("Début de pause", pause_debut_str)
                with col3:
                    st.metric("Fin de pause", pause_fin_str)
                with col4:
                    st.metric("Départ calculé", heure_depart)

            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement : {str(e)}")

# ========== ONGLET 2 : ANALYSER LES DONNÉES ==========
with tab2:
    st.header("Analyse des données et graphiques")

    if not os.path.exists(fichier_csv):
        st.warning("⚠️ Aucune donnée disponible. Ajoutez d'abord une saisie dans l'onglet 'Ajouter une Saisie'.")
    else:
        try:
            # Lecture des données
            horaires = lire_horaires(fichier_csv)

            if len(horaires) == 0:
                st.warning("⚠️ Le fichier est vide. Ajoutez des données d'abord.")
            else:
                # Affichage du nombre d'entrées
                st.metric("Nombre total d'entrées", len(horaires))

                # Calcul des moyennes
                depart_moy, pause_moy, arrivee_moy = calculer_moyennes(horaires)

                if depart_moy and pause_moy and arrivee_moy:
                    # Affichage des moyennes
                    st.subheader("📈 Statistiques Moyennes")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Heure moyenne d'arrivée", arrivee_moy)
                    with col2:
                        st.metric("Heure moyenne de départ", depart_moy)
                    with col3:
                        st.metric("Durée moyenne de pause", pause_moy)

                    st.markdown("---")

                    # Génération des graphiques
                    st.subheader("📊 Graphiques d'évolution")

                    fig1, fig2, fig3 = generer_graphiques(horaires, depart_moy, arrivee_moy)

                    if fig1 and fig2 and fig3:
                        st.pyplot(fig1)
                        st.pyplot(fig2)
                        st.pyplot(fig3)
                    else:
                        st.error("❌ Impossible de générer les graphiques.")
                else:
                    st.error("❌ Erreur lors du calcul des moyennes.")

                # Affichage du tableau de données
                st.subheader("📋 Tableau des données")
                import pandas as pd
                df = pd.DataFrame(horaires)
                st.dataframe(df, use_container_width=True)

        except FileNotFoundError:
            st.error(f"❌ Le fichier '{fichier_csv}' est introuvable.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'analyse : {str(e)}")

# ========== FOOTER ==========
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Application de Gestion des Horaires | Développé avec Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
