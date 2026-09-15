"""
Barre de filtres (sidebar Streamlit).
Ce module n'a qu'une responsabilité : afficher les widgets de filtre et
renvoyer les valeurs choisies par l'utilisateur sous forme de dict.
Il ne touche jamais au dataframe complet — le filtrage lui-même est
délégué à Src.Analyse.Filtre pour séparer "affichage" et "calcul".
"""

import streamlit as st

from Constantes.Input_data import (
    OVR_DEFAUT,
    PAC_DEFAUT,
    DRI_DEFAUT,
    GENRES,
    POSITIONS_GROUPES,
    GROUPE_AILIER_PAR_DEFAUT,
    PIED_LABELS,
)


def afficher_filtres(df) -> dict:
    """Affiche les filtres dans la sidebar et renvoie les valeurs sélectionnées."""
    st.sidebar.header("Filtres")

    #Genre : Hommes / Femmes
    selected_genres_labels = st.sidebar.multiselect(
        "Genre",
        options=list(GENRES.keys()),
        default=list(GENRES.keys()),
    )
    selected_genres = [GENRES[label] for label in selected_genres_labels]


    # Age : slider
    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.sidebar.slider(
        "Âge",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
    )

    # --- Pied préféré ---
    selected_pieds_labels = st.sidebar.multiselect(
        "Pied préféré",
        options=list(PIED_LABELS.values()),
        default=list(PIED_LABELS.values()),
    )
    # on retrouve les valeurs brutes ("Right"/"Left") à partir des libellés cochés
    selected_pieds = [
        valeur_brute
        for valeur_brute, label in PIED_LABELS.items()
        if label in selected_pieds_labels
    ]


    # Championnat : multiselect + boutons "Tout sélectionner / Tout désélectionner"
    leagues_available = sorted(df["League"].dropna().unique().tolist())

    col_a, col_b = st.sidebar.columns(2)
    if col_a.button("Tout sélectionner", use_container_width=True):
        st.session_state["leagues_filtre"] = leagues_available
    if col_b.button("Tout désélectionner", use_container_width=True):
        st.session_state["leagues_filtre"] = []

    selected_leagues = st.sidebar.multiselect(
        "Championnat",
        options=leagues_available,
        default=leagues_available,
        key="leagues_filtre",
        help="Champ déroulant à choix multiple : cliquez pour ajouter/retirer un championnat, ou tapez pour rechercher.",
    )

    exclude_big5 = st.sidebar.checkbox(
        "Exclure les 5 grands championnats (Premier League, LaLiga, Bundesliga, Serie A, Ligue 1)",
        value=True,
    )

    # Postes : multiselect regroupé par famille (ex. "Ailier" = LW + RW)
    groupes_disponibles = [
        g for g in POSITIONS_GROUPES
        if any(code in df["Position"].unique() for code in POSITIONS_GROUPES[g])
    ]
    groupes_selectionnes = st.sidebar.multiselect(
        "Poste",
        options=groupes_disponibles,
        default=[g for g in GROUPE_AILIER_PAR_DEFAUT if g in groupes_disponibles],
        help="Regroupement par famille (ex. « Ailier » = ailier gauche + ailier droit).",
    )
    # on déplie les familles choisies en codes de poste réels (LW, RW, ...)
    selected_positions = [
        code
        for groupe in groupes_selectionnes
        for code in POSITIONS_GROUPES[groupe]
    ]

    # OVR / PAC / DRI : sliders
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


    return {
        "leagues": selected_leagues,
        "exclude_big5": exclude_big5,
        "positions": selected_positions,
        "ovr_min": ovr_min,
        "pac_min": pac_min,
        "dri_min": dri_min,
        "age_range": age_range,
        "genres": selected_genres,
        "pieds": selected_pieds,
    }