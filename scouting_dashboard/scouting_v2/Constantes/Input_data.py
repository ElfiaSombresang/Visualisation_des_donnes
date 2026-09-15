"""
Constantes du projet + fonction de chargement des données.
Toute valeur "en dur" utilisée ailleurs dans l'app (chemin du fichier,
listes de référence, valeurs par défaut des filtres, couleurs) est
centralisée ici pour rester facile à modifier.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# Données source
# ----------------------------------------------------------------------
# Chemin construit relativement à ce fichier (et non au répertoire courant
# d'exécution) : Streamlit Cloud ne lance pas toujours le script depuis la
# racine du projet, un chemin relatif "nu" casse donc en déploiement.
RACINE_PROJET = Path(__file__).resolve().parent.parent
CSV_PATH = str(RACINE_PROJET / "all_players_clean.csv")

# ----------------------------------------------------------------------
# Référentiel métier
# ----------------------------------------------------------------------
# Les 5 grands championnats au sens sportif du terme
BIG5 = [
    "Premier League",
    "LALIGA EA SPORTS",
    "Bundesliga",
    "Serie A Enilive",
    "Ligue 1 McDonald's",
]

# ----------------------------------------------------------------------
# Valeurs par défaut des filtres (calées sur le besoin du directeur sportif :
# "un ailier rapide et bon dribbleur, hors des 5 grands championnats, OVR > 75")
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Postes : libellé français lisible + regroupement par famille
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

# Regroupement par famille : sélectionner "Ailier" renvoie LW + RW, etc.
POSITIONS_GROUPES = {
    "Gardien":                  ["GK"],
    "Défenseur central":        ["CB"],
    "Arrière latéral droit":    ["RB"],
    "Arrière latéral gauche":   ["LB"],
    "Milieu défensif":          ["CDM"],
    "Milieu central":           ["CM"],
    "Milieu offensif":          ["CAM"],
    "Milieu latéral droit":     ["RM"],
    "Milieu latéral gauche":    ["LM"],
    "Ailier droit":             ["RW"],
    "Ailier gauche":            ["LW"],
    "Attaquant":                ["ST"],
}

GROUPE_AILIER_PAR_DEFAUT = ["Ailier droit", "Ailier gauche"]
GENRES = {"Hommes": "M", "Femmes": "F"}
OVR_DEFAUT = 75
PAC_DEFAUT = 75
DRI_DEFAUT = 70

# ----------------------------------------------------------------------
# Colonnes utilisées pour le radar et le tableau final
# ----------------------------------------------------------------------
RADAR_STATS = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]

COLONNES_TABLEAU = [
    "Name", "Age", "Position", "League", "Team", "Nation",
    "OVR", "PAC", "DRI", "SHO", "PAS", "DEF", "PHY",
]

# ----------------------------------------------------------------------
# Habillage graphique (une seule couleur par graphique = respect
# de la contrainte "pas plus de 6 couleurs" ; palette séquentielle
# réservée aux variables continues comme OVR)
# ----------------------------------------------------------------------
COULEUR_HISTOGRAMME = "#4C72B0"
COULEUR_BOXPLOT = "#55A868"
PALETTE_SCATTER = "Viridis"


@st.cache_data
def charger_donnees(path: str = CSV_PATH) -> pd.DataFrame:
    """Charge le dataset et le met en cache pour éviter de le relire à chaque interaction."""
    return pd.read_csv(path)
