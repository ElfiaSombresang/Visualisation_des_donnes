"""Graphiques en barres : pied préféré (comparaison de groupes) et top 10."""

import plotly.express as px

from Constantes.Input_data import PIED_LABELS, COULEURS_PIED


def barplot_pied_prefere(df):
    """Nombre de joueurs droitiers vs gauchers dans la sélection."""
    df_pied = df.copy()
    df_pied["Pied"] = df_pied["Preferred.foot"].map(PIED_LABELS)

    resume = df_pied["Pied"].value_counts().reset_index()
    resume.columns = ["Pied", "Nombre"]

    fig = px.bar(
        resume, x="Pied", y="Nombre", color="Pied",
        color_discrete_map=COULEURS_PIED, text="Nombre",
        labels={"Pied": "Pied préféré", "Nombre": "Nombre de joueurs"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        margin=dict(t=30, b=10), showlegend=False,
        yaxis_range=[0, resume["Nombre"].max() * 1.15],
    )
    return fig


def barres_top10(df_top10, critere_tri, stats=None):
    """Barres horizontales : stats choisies (OVR/PAC/DRI) des joueurs du top 10,
    triées par ordre décroissant du critère choisi (meilleur joueur en haut)."""
    if not stats:
        stats = ["OVR", "PAC", "DRI"]

    couleurs_stats = {"OVR": "#3B82F6", "PAC": "#8B5CF6", "DRI": "#EC4899"}
    ordre_joueurs = df_top10.sort_values(by=critere_tri, ascending=True)["Name"].tolist()

    data_long = df_top10.melt(
        id_vars="Name", value_vars=stats, var_name="Statistique", value_name="Valeur",
    )

    fig = px.bar(
        data_long, x="Valeur", y="Name", color="Statistique",
        barmode="group", orientation="h",
        category_orders={"Name": ordre_joueurs},
        color_discrete_map={s: couleurs_stats[s] for s in stats},
        labels={"Valeur": "Note", "Name": ""},
    )
    fig.update_layout(margin=dict(t=10, b=10), xaxis_range=[0, 100], legend_title_text="", height=450)
    return fig