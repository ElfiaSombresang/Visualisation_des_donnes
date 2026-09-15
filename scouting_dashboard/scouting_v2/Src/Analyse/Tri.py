"""
Tri et mise en forme du tableau des meilleurs profils.
"""

import pandas as pd

from Constantes.Input_data import COLONNES_TABLEAU


def trier_profils(df: pd.DataFrame, colonne: str = "OVR", ascendant: bool = False) -> pd.DataFrame:
    """Trie les profils filtrés (par défaut OVR décroissant) et ne garde que les colonnes utiles à l'affichage."""
    trie = (
        df.sort_values(by=colonne, ascending=ascendant)[COLONNES_TABLEAU]
        .reset_index(drop=True)
    )
    trie.index = trie.index + 1  # classement lisible à partir de 1
    return trie
