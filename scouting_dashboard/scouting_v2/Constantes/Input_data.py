"""
Constantes du projet + fonction de chargement des données.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# Données source
# ----------------------------------------------------------------------
RACINE_PROJET = Path(__file__).resolve().parent.parent
CSV_PATH = str(RACINE_PROJET / "all_players_clean.csv")

# ----------------------------------------------------------------------
# Référentiel métier
# ----------------------------------------------------------------------
BIG5 = [
    "Premier League",
    "LALIGA EA SPORTS",
    "Bundesliga",
    "Serie A Enilive",
    "Ligue 1 McDonald's",
]

# ----------------------------------------------------------------------
# Genre
# ----------------------------------------------------------------------
GENRES = {"Hommes": "M", "Femmes": "F"}

# ----------------------------------------------------------------------
# Postes : libellé français + regroupement par famille
# ----------------------------------------------------------------------
POSITIONS_LABELS = {
    "GK":  "Gardien",
    "CB":  "Défenseur central",
    "LB":  "Arrière gauche",
    "RB":  "Arrière droit",
    "CDM": "Milieu défensif",
    "CM":  "Milieu central",
    "CAM": "Milieu offensif",
    "LM":  "Milieu gauche",
    "RM":  "Milieu droit",
    "LW":  "Ailier gauche",
    "RW":  "Ailier droit",
    "ST":  "Attaquant",
}

POSITIONS_GROUPES = {
    "Gardien":            ["GK"],
    "Défenseur central":  ["CB"],
    "Arrière latéral":    ["LB", "RB"],
    "Milieu défensif":    ["CDM"],
    "Milieu central":     ["CM"],
    "Milieu offensif":    ["CAM"],
    "Milieu latéral":     ["LM", "RM"],
    "Ailier":             ["LW", "RW"],
    "Attaquant":          ["ST"],
}

GROUPE_AILIER_PAR_DEFAUT = ["Ailier"]

# ----------------------------------------------------------------------
# Pied préféré
# ----------------------------------------------------------------------
PIED_LABELS = {"Right": "Droitier", "Left": "Gaucher"}



# ----------------------------------------------------------------------
# Valeurs par défaut des filtres numériques
# ----------------------------------------------------------------------
OVR_DEFAUT = 75
PAC_DEFAUT = 75
DRI_DEFAUT = 70

# ----------------------------------------------------------------------
# Colonnes du radar et du tableau final
# ----------------------------------------------------------------------
RADAR_STATS = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]

COLONNES_TABLEAU = [
    "Name", "Age", "Position", "Pied", "League", "Team", "Nation",
    "OVR", "PAC", "DRI", "SHO", "PAS", "DEF", "PHY",
]

# ----------------------------------------------------------------------
# Habillage graphique
# ----------------------------------------------------------------------
COULEUR_HISTOGRAMME = "#4C72B0"
COULEUR_BOXPLOT = "#55A868"
COULEURS_PIED = {"Droitier": "#725C78", "Gaucher": "#B58D9B"}
PALETTE_SCATTER = "Viridis"


@st.cache_data
def charger_donnees(path: str = CSV_PATH) -> pd.DataFrame:
    """Charge le dataset et le met en cache pour éviter de le relire à chaque interaction."""
    return pd.read_csv(path)