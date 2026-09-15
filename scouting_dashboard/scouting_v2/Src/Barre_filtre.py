"""
Barre de filtres (sidebar Streamlit).
Ce module n'a qu'une responsabilité : afficher les widgets de filtre et
renvoyer les valeurs choisies par l'utilisateur sous forme de dict.
Il ne touche jamais au dataframe complet — le filtrage lui-même est
délégué à Src.Analyse.Filtre pour séparer "affichage" et "calcul".
"""

import streamlit as st

from Constantes.Input_data import (
    POSITIONS_GROUPES,
    GROUPE_AILIER_PAR_DEFAUT,
    OVR_DEFAUT,
    PAC_DEFAUT,
    DRI_DEFAUT,
    GENRES,
)


def afficher_filtres(df) -> dict:
    """Affiche les filtres dans la sidebar et renvoie les valeurs sélectionnées."""
    st.sidebar.header("🔎 Filtres")

    leagues_available = sorted(df["League"].dropna().unique().tolist())
    selected_leagues = st.sidebar.multiselect(
        "Championnat",
        options=leagues_available,
        default=leagues_available,
        help="Par défaut, tous les championnats sont inclus.",
    )

    exclude_big5 = st.sidebar.checkbox(
        "Exclure les 5 grands championnats (Premier League, LaLiga, Bundesliga, Serie A, Ligue 1)",
        value=True,
    )

    positions_available = sorted(df["Position"].dropna().unique().tolist())
    default_positions = [p for p in POSITIONS_AILIERS_PAR_DEFAUT if p in positions_available]
    selected_positions = st.sidebar.multiselect(
        "Poste",
        options=positions_available,
        default=default_positions,
        help="LW/RW = ailiers gauche/droit.",
    )

    ovr_min = st.sidebar.slider(
        "OVR minimum (note générale)",
        min_value=int(df["OVR"].min()),
        max_value=int(df["OVR"].max()),
        value=OVR_DEFAUT,
    )

    pac_min = st.sidebar.slider(
        "PAC minimum (vitesse)",
        min_value=int(df["PAC"].min()),
        max_value=int(df["PAC"].max()),
        value=PAC_DEFAUT,
    )

    dri_min = st.sidebar.slider(
        "DRI minimum (dribble)",
        min_value=int(df["DRI"].min()),
        max_value=int(df["DRI"].max()),
        value=DRI_DEFAUT,
    )

    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.sidebar.slider(
        "Âge",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
    )

    selected_genres_labels = st.sidebar.multiselect(
        "Genre",
        options=list(GENRES.keys()),
        default=list(GENRES.keys()),
    )
    selected_genres = [GENRES[label] for label in selected_genres_labels]

    return {
        "leagues": selected_leagues,
        "exclude_big5": exclude_big5,
        "positions": selected_positions,
        "ovr_min": ovr_min,
        "pac_min": pac_min,
        "dri_min": dri_min,
        "age_range": age_range,
        "genres": selected_genres,
    }
