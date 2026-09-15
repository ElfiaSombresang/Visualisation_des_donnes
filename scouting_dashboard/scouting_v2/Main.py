# -*- coding: utf-8 -*-
"""
Main.py — Point d'entrée du dashboard de scouting.

Ce fichier ne fait QUE de l'orchestration : il appelle les fonctions des
autres modules dans l'ordre (données → filtres → filtrage → KPI →
graphiques → tableau → bonus) et gère l'affichage Streamlit. Toute la
logique de calcul vit dans Src/ et Constantes/.

Lancer avec : streamlit run Main.py
"""

import streamlit as st

from Constantes.Input_data import charger_donnees, COULEUR_HISTOGRAMME
from Src.Barre_filtre import afficher_filtres
from Src.Analyse.Filtre import appliquer_filtres
from Src.Analyse.Tri import trier_profils
from Src.Graphiques.Scatter import scatter_vitesse_dribble
from Src.Graphiques.Aire import (
    histogramme_dribble,
    histogramme_vitesse,
    barplot_pied_prefere,
    barres_top10,
    radar_comparaison
)

st.set_page_config(page_title="Scouting — Recherche de profils", layout="wide")

# ----------------------------------------------------------------------
# 1. CHARGEMENT DES DONNÉES
# ----------------------------------------------------------------------
df = charger_donnees()

st.title("Outil de scouting — Recherche de profils")
# st.caption(
#     "Cellule de recrutement · Filtrez le vivier de joueurs par championnat, poste et niveau "
#     "pour faire émerger des profils correspondant à un besoin (ex. un ailier rapide et bon "
#     "dribbleur, hors des cinq grands championnats, OVR > 75)."
# )

# ----------------------------------------------------------------------
# 2. FILTRES (sidebar) + APPLICATION DES FILTRES
# ----------------------------------------------------------------------
filtres = afficher_filtres(df)
filtered = appliquer_filtres(df, filtres)

# ----------------------------------------------------------------------
# ÉTAT VIDE
# ----------------------------------------------------------------------
if filtered.empty:
    st.warning(
        "⚠️ Aucun joueur ne correspond à ces critères. Essayez d'élargir un filtre "
        "(ex. baisser le seuil OVR/PAC/DRI, ajouter un poste ou un championnat)."
    )
    st.stop()

# ----------------------------------------------------------------------
# 3. BANDEAU DE CHIFFRES CLÉS
# ----------------------------------------------------------------------
st.subheader("Chiffres clés du vivier sélectionné")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Joueurs trouvés", f"{len(filtered)}")
c2.metric("OVR moyen", f"{filtered['OVR'].mean():.1f}")
c3.metric("PAC moyen", f"{filtered['PAC'].mean():.1f}")
c4.metric("DRI moyen", f"{filtered['DRI'].mean():.1f}")
c5.metric("Âge moyen", f"{filtered['Age'].mean():.1f} ans")

st.divider()

# ----------------------------------------------------------------------
# 4. TROIS GRAPHIQUES (distribution / comparaison / relation)
# ----------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Distribution du dribble (DRI)")
    st.plotly_chart(histogramme_dribble(filtered), use_container_width=True)
    # st.caption(
    #     "**Pourquoi un histogramme ?** DRI est une variable quantitative continue : "
    #     "l'histogramme montre si le vivier sélectionné est homogène en dribble ou s'il "
    #     "contient quelques profils nettement au-dessus du lot."
    # )

with col2:
    st.markdown("#### Distribution du vitesse (PAC)")
    st.plotly_chart(histogramme_vitesse(filtered), use_container_width=True)
    # st.caption(
    #     "**Pourquoi un boxplot ?** Il compare médiane et dispersion de PAC entre "
    #     "championnats (quantitative × catégorielle) sur un axe commun, pour repérer où "
    #     "se trouvent les joueurs les plus rapides (limité aux 8 championnats les plus "
    #     "représentés dans la sélection, pour la lisibilité)."
    # )

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Nombre de joueurs droitiers vs gauchers")
    st.plotly_chart(barplot_pied_prefere(filtered), use_container_width=True)
    # st.caption(
    #     "**Pourquoi un barplot ?** Compare une variable quantitative (OVR moyen) entre "
    #     "deux groupes d'une variable catégorielle (pied préféré) ; l'effectif de chaque "
    #     "groupe (n=) est affiché pour éviter de comparer des moyennes peu fiables sur un "
    #     "petit échantillon."
    # )

with col4:
    st.markdown("#### Niveau des joueurs : vitesse vs dribble")
    st.plotly_chart(scatter_vitesse_dribble(filtered), use_container_width=True)
    # st.caption(
    #     "**Pourquoi un nuage de points ?** Croiser vitesse et dribble permet de repérer "
    #     "les joueurs qui cumulent les deux qualités. Les lignes Q1/médiane/Q3 (grises) "
    #     "situent chaque joueur par rapport au reste du vivier filtré."
    # )


st.divider()

# ----------------------------------------------------------------------
# 5. TABLEAU DES MEILLEURS PROFILS
# ----------------------------------------------------------------------
st.subheader("Top 10 des meilleurs profils")

critere_tri = st.radio(
    "Trier par",
    options=["OVR", "PAC", "DRI"],
    horizontal=True,
)

top_profiles = trier_profils(filtered, colonne=critere_tri, ascendant=False, top_n=10)
st.dataframe(top_profiles, use_container_width=True, height=400)
st.caption(f"Top {len(top_profiles)} sur {len(filtered)} joueur(s) filtré(s), trié par {critere_tri} décroissant.")

stats_choisies = st.multiselect(
    "Statistiques à afficher",
    options=["OVR", "PAC", "DRI"],
    default=["OVR", "PAC", "DRI"],
)

st.markdown("#### Top 10 — comparaison des joueurs")
if stats_choisies:
    st.plotly_chart(
        barres_top10(top_profiles, critere_tri, stats=stats_choisies),
        use_container_width=True,
    )

else:
    st.info("Sélectionnez au moins une statistique pour afficher le graphique.")

st.divider()

# ----------------------------------------------------------------------
# 6. BONUS : RADAR DE COMPARAISON (2-3 JOUEURS)
# ----------------------------------------------------------------------
st.subheader("Comparer 2 ou 3 joueurs")
# st.caption(
#     "Un radar n'est lisible que pour 2 ou 3 joueurs à la fois, et l'ordre des axes influence "
#     "la forme perçue : à utiliser pour affiner un choix final, pas pour trier tout le vivier."
# )

player_names = top_profiles["Name"].tolist()
selected_players = st.multiselect(
    "Choisir 2 ou 3 joueurs à comparer",
    options=player_names,
    default=player_names[:2] if len(player_names) >= 2 else player_names,
    max_selections=3,
)

if len(selected_players) >= 2:
    st.pyplot(radar_comparaison(filtered, selected_players))
else:
    st.info("Sélectionnez au moins 2 joueurs pour afficher le radar.")
