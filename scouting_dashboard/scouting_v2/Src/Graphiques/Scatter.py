"""
Graphique de relation : nuage de points (scatter).
Répond à la question "un joueur peut-il être à la fois rapide ET bon
dribbleur ?" en croisant deux variables quantitatives.
"""

import plotly.express as px

from Constantes.Input_data import PALETTE_SCATTER


def scatter_vitesse_dribble(df):
    """Nuage de points PAC (x) vs DRI (y), couleur = OVR (palette séquentielle)."""
    fig = px.scatter(
        df,
        x="PAC",
        y="DRI",
        color="OVR",
        color_continuous_scale=PALETTE_SCATTER,
        hover_data=["Name", "Team", "League", "Age"],
        labels={"PAC": "Vitesse (PAC)", "DRI": "Dribble (DRI)", "OVR": "OVR"},
    )
    fig.update_layout(margin=dict(t=10, b=10))
    return fig
