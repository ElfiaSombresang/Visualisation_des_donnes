"""
Graphique de relation : nuage de points (scatter).
Répond à la question "un joueur peut-il être à la fois rapide ET bon
dribbleur ?" en croisant deux variables quantitatives.
Les lignes de repère (Q1, médiane, Q3) sur chaque axe permettent de
situer un joueur par rapport au reste du vivier filtré, plutôt que de
juger sa position dans l'absolu.
"""

import plotly.express as px

from Constantes.Input_data import PALETTE_SCATTER


def scatter_vitesse_dribble(df):
    """Nuage de points PAC (x) vs DRI (y), couleur = OVR (palette séquentielle),
    avec Q1/médiane/Q3 tracés sur les deux axes pour profiler les joueurs."""
    fig = px.scatter(
        df,
        x="PAC",
        y="DRI",
        color="OVR",
        color_continuous_scale=PALETTE_SCATTER,
        hover_data=["Name", "Team", "League", "Age"],
        labels={"PAC": "Vitesse", "DRI": "Dribble", "OVR": "OVR"},
    )
    fig.update_layout(margin=dict(t=10, b=10))

    # --- Repères statistiques sur l'axe X (PAC) ---
    q1_x, med_x, q3_x = df["PAC"].quantile([0.25, 0.5, 0.75])
    for valeur, label, style in [
        (q1_x, "Q1", "dot"),
        (med_x, "Médiane", "dash"),
        (q3_x, "Q3", "dot"),
    ]:
        fig.add_vline(
            x=valeur,
            line_dash=style,
            line_color="grey",
            opacity=0.6,
            annotation_text=f"{label} PAC = {valeur:.0f}",
            annotation_position="top",
            annotation_font_size=10,
        )

    # --- Repères statistiques sur l'axe Y (DRI) ---
    q1_y, med_y, q3_y = df["DRI"].quantile([0.25, 0.5, 0.75])
    for valeur, label, style in [
        (q1_y, "Q1", "dot"),
        (med_y, "Médiane", "dash"),
        (q3_y, "Q3", "dot"),
    ]:
        fig.add_hline(
            y=valeur,
            line_dash=style,
            line_color="grey",
            opacity=0.6,
            annotation_text=f"{label} DRI = {valeur:.0f}",
            annotation_position="right",
            annotation_font_size=10,
        )

    return fig