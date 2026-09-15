# -*- coding: utf-8 -*-
"""
Dashboard de scouting — Cellule de recrutement
================================================
Question métier : trouver rapidement des profils du type « ailier rapide et
bon dribbleur, hors des cinq grands championnats, note générale (OVR) > 75 ».

Structure du fichier (voir README.md pour les choix de graphiques) :
    1. Chargement des données
    2. Filtres (sidebar)
    3. Bandeau de chiffres clés (KPI)
    4. Trois graphiques : distribution / comparaison de groupes / relation
    5. Tableau des meilleurs profils
    6. Bonus : radar chart de comparaison de 2 joueurs
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Config générale de la page
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Scouting — Trouver un profil",
    # page_icon="⚽",
    layout="wide",
)

COULEUR_UNIQUE = "#2E5EAA"  # une seule couleur pour histogramme / boxplot / barplot
CINQ_GRANDS_CHAMPIONNATS = [
    "Premier League",
    "LALIGA EA SPORTS",
    "Bundesliga",
    "Ligue 1 McDonald's",
    "Serie A Enilive",
]

STATS_RADAR = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]

# ----------------------------------------------------------------------------
# 1. Chargement des données
# ----------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/all_players_clean.csv")
    # On ne garde que les joueurs de champ pour ce cas d'usage scouting
    # (les colonnes GK.* sont ~99% vides et hors sujet ici)
    df = df[df["Position"] != "GK"].copy()
    df["Nom complet"] = df["Name"]
    return df


df = load_data()

st.title("⚽ Outil de scouting — trouver un profil")
st.caption(
    "Exemple de recherche : *un ailier rapide et bon dribbleur, hors des cinq "
    "grands championnats, note générale supérieure à 75.*"
)

# ----------------------------------------------------------------------------
# 2. Filtres (sidebar) — au moins 3 filtres : championnat, poste, seuil numérique
# ----------------------------------------------------------------------------
st.sidebar.header("🔎 Filtres")

exclure_big5 = st.sidebar.checkbox(
    "Exclure les 5 grands championnats",
    value=True,
    help="Premier League, LaLiga, Bundesliga, Ligue 1, Serie A",
)

leagues_dispo = sorted(df["League"].dropna().unique().tolist())
leagues_defaut = (
    [l for l in leagues_dispo if l not in CINQ_GRANDS_CHAMPIONNATS]
    if exclure_big5
    else leagues_dispo
)

championnats = st.sidebar.multiselect(
    "Championnat",
    options=leagues_dispo,
    default=leagues_defaut,
)

postes_dispo = sorted(df["Position"].dropna().unique().tolist())
postes_defaut = [p for p in ["LW", "RW"] if p in postes_dispo] or postes_dispo
postes = st.sidebar.multiselect(
    "Poste",
    options=postes_dispo,
    default=postes_defaut,
    help="LW / RW = ailiers gauche / droit",
)

ovr_min = st.sidebar.slider(
    "Note générale minimale (OVR)",
    min_value=int(df["OVR"].min()),
    max_value=int(df["OVR"].max()),
    value=75,
)

pac_min = st.sidebar.slider(
    "Vitesse minimale (PAC)",
    min_value=int(df["PAC"].min()),
    max_value=int(df["PAC"].max()),
    value=int(df["PAC"].min()),
)

age_min, age_max = st.sidebar.slider(
    "Âge",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max())),
)

# ----------------------------------------------------------------------------
# Application des filtres
# ----------------------------------------------------------------------------
filtre = (
    df["League"].isin(championnats)
    & df["Position"].isin(postes)
    & (df["OVR"] >= ovr_min)
    & (df["PAC"] >= pac_min)
    & (df["Age"].between(age_min, age_max))
)
df_filtre = df[filtre].copy()

# ----------------------------------------------------------------------------
# Gestion de l'état vide : aucun joueur ne correspond
# ----------------------------------------------------------------------------
if df_filtre.empty:
    st.warning(
        "⚠️ Aucun joueur ne correspond à ces critères. "
        "Essayez d'élargir un filtre (championnats, poste, OVR ou PAC minimum)."
    )
    st.stop()

# ----------------------------------------------------------------------------
# 3. Bandeau de chiffres clés (KPI)
# ----------------------------------------------------------------------------
st.subheader("📊 Chiffres clés de la sélection")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Joueurs sélectionnés", f"{len(df_filtre):,}".replace(",", " "))
c2.metric("OVR moyen", f"{df_filtre['OVR'].mean():.1f}")
c3.metric("PAC moyen", f"{df_filtre['PAC'].mean():.1f}")
c4.metric("DRI moyen", f"{df_filtre['DRI'].mean():.1f}")
c5.metric("Âge moyen", f"{df_filtre['Age'].mean():.1f} ans")

st.divider()

# ----------------------------------------------------------------------------
# 4. Trois graphiques de familles différentes
# ----------------------------------------------------------------------------
col_a, col_b = st.columns(2)

# --- Graphique 1 : DISTRIBUTION (histogramme) -------------------------------
with col_a:
    st.markdown("#### Distribution des notes générales (OVR)")
    fig_hist = px.histogram(
        df_filtre,
        x="OVR",
        nbins=20,
        color_discrete_sequence=[COULEUR_UNIQUE],
    )
    fig_hist.update_layout(
        xaxis_title="Note générale (OVR, /99)",
        yaxis_title="Nombre de joueurs",
        bargap=0.05,
    )
    fig_hist.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_hist, use_container_width=True)
    st.caption(
        "➡️ Montre si le vivier de profils correspondant aux filtres est "
        "large (répartition étalée) ou restreint (barres concentrées) : "
        "utile pour juger si le brief est réaliste sur ce marché."
    )

# --- Graphique 2 : COMPARAISON DE GROUPES (boxplot) -------------------------
with col_b:
    st.markdown("#### Comparaison du OVR par championnat (Top 8 représentés)")
    top_leagues = (
        df_filtre["League"].value_counts().nlargest(8).index.tolist()
    )
    df_box = df_filtre[df_filtre["League"].isin(top_leagues)]
    # ordre des championnats par médiane décroissante, pour une lecture honnête
    ordre = (
        df_box.groupby("League")["OVR"].median().sort_values(ascending=False).index
    )
    fig_box = px.box(
        df_box,
        x="League",
        y="OVR",
        category_orders={"League": list(ordre)},
        color_discrete_sequence=[COULEUR_UNIQUE],
    )
    fig_box.update_layout(
        xaxis_title="Championnat",
        yaxis_title="Note générale (OVR, /99)",
    )
    st.plotly_chart(fig_box, use_container_width=True)
    st.caption(
        "➡️ Compare le niveau (médiane et dispersion de l'OVR) entre les "
        "championnats les plus représentés dans la sélection, pour prioriser "
        "les compétitions à prospecter."
    )

st.markdown("#### Relation entre vitesse (PAC) et dribble (DRI)")
fig_scatter = px.scatter(
    df_filtre,
    x="PAC",
    y="DRI",
    color="OVR",
    color_continuous_scale="Viridis",  # palette séquentielle : OVR est une variable continue
    hover_data=["Name", "Team", "League", "Position", "Age"],
)
fig_scatter.update_layout(
    xaxis_title="Vitesse (PAC, /99)",
    yaxis_title="Dribble (DRI, /99)",
    coloraxis_colorbar_title="OVR",
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption(
    "➡️ Chaque point cumulant un PAC et un DRI élevés (en haut à droite, "
    "couleur claire = OVR fort) est un profil qui correspond directement à "
    "la demande « rapide et bon dribbleur »."
)

st.divider()

# ----------------------------------------------------------------------------
# 5. Tableau des meilleurs profils, trié
# ----------------------------------------------------------------------------
st.subheader("🏆 Meilleurs profils correspondant aux critères")

df_table = df_filtre.copy()
df_table["Score vitesse + dribble"] = (
    (df_table["PAC"] + df_table["DRI"]) / 2
).round(1)
df_table = df_table.sort_values(
    by=["Score vitesse + dribble", "OVR"], ascending=[False, False]
)

colonnes_affichees = [
    "Name",
    "Team",
    "League",
    "Position",
    "Age",
    "OVR",
    "PAC",
    "DRI",
    "SHO",
    "Score vitesse + dribble",
]
st.dataframe(
    df_table[colonnes_affichees].head(25).reset_index(drop=True),
    use_container_width=True,
)
st.caption(
    f"{len(df_table)} joueur(s) au total répondent aux critères — 25 premiers "
    "affichés, triés par score vitesse + dribble puis par OVR."
)

st.divider()

# ----------------------------------------------------------------------------
# 6. Bonus : radar chart de comparaison (2 à 3 joueurs)
# ----------------------------------------------------------------------------
st.subheader("🕸️ Comparer 2 à 3 joueurs (radar)")
noms_dispo = df_table["Name"].tolist()
joueurs_choisis = st.multiselect(
    "Sélectionner 2 ou 3 joueurs à comparer",
    options=noms_dispo,
    default=noms_dispo[:2] if len(noms_dispo) >= 2 else noms_dispo,
    max_selections=3,
)

if len(joueurs_choisis) < 2:
    st.info("Sélectionnez au moins 2 joueurs pour afficher le radar.")
else:
    fig_radar = go.Figure()
    for nom in joueurs_choisis:
        ligne = df_table[df_table["Name"] == nom].iloc[0]
        valeurs = [ligne[s] for s in STATS_RADAR]
        fig_radar.add_trace(
            go.Scatterpolar(
                r=valeurs + [valeurs[0]],
                theta=STATS_RADAR + [STATS_RADAR[0]],
                fill="toself",
                name=nom,
            )
        )
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 99])),
        showlegend=True,
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.caption(
        "⚠️ Lecture à prendre avec précaution : un radar n'est lisible que "
        "pour 2-3 joueurs, et l'ordre des axes influence la forme perçue "
        "(ne pas comparer visuellement des radars aux axes réordonnés)."
    )