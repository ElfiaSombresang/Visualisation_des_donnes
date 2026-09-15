"""Graphiques de distribution : histogrammes."""

import plotly.express as px

from Constantes.Input_data import COULEUR_HISTOGRAMME, COULEUR_BOXPLOT


def histogramme_dribble(df):
    """Distribution de la note de dribble (DRI) dans le vivier filtré."""
    fig = px.histogram(
        df, x="DRI", nbins=20,
        color_discrete_sequence=[COULEUR_HISTOGRAMME],
        labels={"DRI": "Note de dribble (DRI)"},
    )
    fig.update_layout(yaxis_title="Nombre de joueurs", bargap=0.05, margin=dict(t=10, b=10))
    return fig


def histogramme_vitesse(df):
    """Distribution de la vitesse (PAC) dans le vivier filtré."""
    fig = px.histogram(
        df, x="PAC", nbins=20,
        color_discrete_sequence=[COULEUR_HISTOGRAMME],
        labels={"PAC": "Vitesse (PAC)"},
    )
    fig.update_layout(yaxis_title="Nombre de joueurs", bargap=0.05, margin=dict(t=10, b=10))
    return fig