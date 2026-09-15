"""
Tri et mise en forme du tableau des meilleurs profils.
"""

import pandas as pd

from Constantes.Input_data import COLONNES_TABLEAU, POSITIONS_LABELS, PIED_LABELS

def trier_profils(df: pd.DataFrame, colonne: str = "OVR", ascendant: bool = False, top_n: int | None = None) -> pd.DataFrame:
    """Trie les profils filtrés et ajoute les libellés lisibles (poste, pied)."""
    df_enrichi = df.copy()
    df_enrichi["Pied"] = df_enrichi["Preferred.foot"].map(PIED_LABELS)

    trie = (
        df_enrichi.sort_values(by=colonne, ascending=ascendant)[COLONNES_TABLEAU]
        .reset_index(drop=True)
    )
    trie["Position"] = trie["Position"].map(POSITIONS_LABELS).fillna(trie["Position"])
    trie = trie.rename(columns={"Pied": "Pied de préférence"})

    if top_n is not None:
        trie = trie.head(top_n)

    trie.index = trie.index + 1
    return trie