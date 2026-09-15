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

from Constantes.Input_data import COULEUR_HISTOGRAMME, COULEUR_BOXPLOT, RADAR_STATS, PIED_LABELS, COULEURS_PIED

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

    couleurs_stats = {"OVR": "#4C72B0", "PAC": "#55A868", "DRI": "#C44E52"}

    # df_top10 est déjà trié décroissant par critere_tri (via trier_profils) :
    # on garde cet ordre tel quel comme ordre des catégories.
    ordre_joueurs = df_top10["Name"].tolist()

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
    # Plotly place par défaut la première catégorie en bas : on inverse
    # l'axe pour que le 1er du classement (df_top10[0]) apparaisse en haut.
    fig.update_yaxes(autorange="reversed")
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
