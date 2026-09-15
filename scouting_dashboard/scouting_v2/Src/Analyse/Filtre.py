"""
Application des filtres au dataframe complet.
Fonction pure (pas de composant Streamlit) : facile à tester unitairement,
prend un df + un dict de filtres, renvoie un df filtré.
"""

import pandas as pd

from Constantes.Input_data import BIG5


def appliquer_filtres(df: pd.DataFrame, filtres: dict) -> pd.DataFrame:
    """Renvoie le sous-ensemble de joueurs correspondant aux filtres sélectionnés."""
    age_min, age_max = filtres["age_range"]

    masque = (
        df["League"].isin(filtres["leagues"])
        & df["Position"].isin(filtres["positions"])
        & (df["OVR"] >= filtres["ovr_min"])
        & (df["PAC"] >= filtres["pac_min"])
        & (df["DRI"] >= filtres["dri_min"])
        & df["Age"].between(age_min, age_max)
        & df["gender"].isin(filtres["genres"])
        & df["Preferred.foot"].isin(filtres["pieds"])
    )
    resultat = df[masque].copy()

    if filtres["exclude_big5"]:
        resultat = resultat[~resultat["League"].isin(BIG5)]

    return resultat
