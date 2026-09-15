"""
Graphiques "en aire" : histogramme (distribution), boxplot (comparaison de
groupes) et radar (bonus, comparaison de 2-3 joueurs). Contrairement au
nuage de points (Scatter.py), ces trois graphiques représentent des
surfaces/volumes (barres, boîtes, aires remplies) plutôt que des points
individuels.
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

from Constantes.Input_data import COULEUR_HISTOGRAMME, COULEUR_BOXPLOT, RADAR_STATS


def histogramme_dribble(df):
    """Distribution de la note de dribble (DRI) dans le vivier filtré."""
    fig = px.histogram(
        df,
        x="DRI",
        nbins=20,
        color_discrete_sequence=[COULEUR_HISTOGRAMME],
        labels={"DRI": "Note de dribble (DRI)"},
    )
    fig.update_layout(
        yaxis_title="Nombre de joueurs",
        bargap=0.05,
        margin=dict(t=10, b=10),
    )
    return fig

def histogramme_vitesse(df):
    """Distribution de la vitesse (PAC) dans le vivier filtré."""
    fig = px.histogram(
        df,
        x="PAC",
        nbins=20,
        color_discrete_sequence=[COULEUR_BOXPLOT],
        labels={"PAC": "Vitesse (PAC)"},
    )
    fig.update_layout(
        yaxis_title="Nombre de joueurs",
        bargap=0.05,
        margin=dict(t=10, b=10),
    )
    return fig


def radar_comparaison(df, noms_joueurs: list):
    """Radar Matplotlib comparant 2 ou 3 joueurs sur PAC/SHO/PAS/DRI/DEF/PHY."""
    angles = np.linspace(0, 2 * np.pi, len(RADAR_STATS), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    for nom in noms_joueurs:
        ligne = df[df["Name"] == nom].iloc[0]
        valeurs = [ligne[s] for s in RADAR_STATS]
        valeurs += valeurs[:1]
        ax.plot(angles, valeurs, linewidth=2, label=nom)
        ax.fill(angles, valeurs, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(RADAR_STATS)
    ax.set_ylim(0, 100)
    ax.set_title("Comparaison de profils", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1))
    return fig
