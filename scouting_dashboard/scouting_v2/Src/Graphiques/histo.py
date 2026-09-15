"""
Graphiques "en aire" : histogramme (distribution), boxplot (comparaison de
groupes) et radar (bonus, comparaison de 2-3 joueurs). Contrairement au
nuage de points (Scatter.py), ces trois graphiques représentent des
surfaces/volumes (barres, boîtes, aires remplies) plutôt que des points
individuels.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

from Constantes.Input_data import COULEUR_HISTOGRAMME, COULEUR_BOXPLOT, PIED_LABELS, COULEURS_PIED

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
        color_discrete_sequence=[COULEUR_HISTOGRAMME],
        labels={"PAC": "Vitesse (PAC)"},
    )
    fig.update_layout(
        yaxis_title="Nombre de joueurs",
        bargap=0.05,
        margin=dict(t=10, b=10),
    )
    return fig


def barplot_pied_prefere(df):
    """Nombre de joueurs droitiers vs gauchers dans la sélection."""
    df_pied = df.copy()
    df_pied["Pied"] = df_pied["Preferred.foot"].map(PIED_LABELS)

    resume = (
        df_pied["Pied"]
        .value_counts()
        .reset_index()
    )
    resume.columns = ["Pied", "Nombre"]

    fig = px.bar(
        resume,
        x="Pied",
        y="Nombre",
        color="Pied",
        color_discrete_map=COULEURS_PIED,
        text="Nombre",
        labels={"Pied": "Pied préféré", "Nombre": "Nombre de joueurs"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        margin=dict(t=30, b=10),
        showlegend=False,
        yaxis_range=[0, resume["Nombre"].max() * 1.15],  # barres à zéro, honnêteté visuelle
    )
    return fig



def barres_top10(df_top10, critere_tri, stats=None):
    """Barres horizontales : stats choisies (OVR/PAC/DRI) des joueurs du top 10,
    triés par ordre décroissant du critère choisi (meilleur joueur en haut)."""
    if not stats:
        stats = ["OVR", "PAC", "DRI"]

    couleurs_stats = {"OVR": "#3B82F6", "PAC": "#EC4899", "DRI": "#8B5CF6"}

    # df_top10 est déjà trié décroissant par critere_tri (via trier_profils).
    # Plotly place par défaut le 1er élément de category_orders en BAS du
    # graphique horizontal : on lui donne donc l'ordre croissant (le moins
    # bon en bas, le meilleur en haut).
    ordre_joueurs = (
        df_top10.sort_values(by=critere_tri, ascending=False)["Name"].tolist()
    )

    data_long = df_top10.melt(
        id_vars="Name",
        value_vars=stats,
        var_name="Statistique",
        value_name="Valeur",
    )

    fig = px.bar(
        data_long,
        x="Valeur",
        y="Name",
        color="Statistique",
        barmode="group",
        orientation="h",
        category_orders={"Name": ordre_joueurs},
        color_discrete_map={s: couleurs_stats[s] for s in stats},
        labels={"Valeur": "Note", "Name": ""},
    )
    fig.update_layout(
        margin=dict(t=10, b=10),
        xaxis_range=[0, 100],
        legend_title_text="",
        height=450,
    )
    return fig



