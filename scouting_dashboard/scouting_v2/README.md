# Outil de scouting — README

**Question métier.** Le directeur sportif veut trouver rapidement des profils précis
(ex. « ailier rapide et bon dribbleur, hors des 5 grands championnats, OVR > 75 ») dans
une base de ~17 700 joueurs, sans avoir à écrire de code à chaque nouvelle demande.

**Filtres.** Championnat (multi-choix), case « hors 5 grands championnats », poste,
et trois seuils numériques (OVR, PAC, DRI) : ils couvrent large et se combinent en `ET`.

**Graphiques et pourquoi.**
- *Histogramme (DRI)* — variable quantitative seule : montre si le vivier filtré est
  homogène en dribble ou contient des profils hors norme.
- *Boxplot (PAC par championnat)* — quantitative × catégorielle : compare médiane et
  dispersion de la vitesse entre championnats sur un axe commun (honnêteté visuelle).
- *Nuage de points (PAC vs DRI, couleur = OVR)* — c'est la question métier elle-même :
  croiser vitesse et dribble pour repérer qui cumule les deux qualités.
- *Radar (bonus)* — comparaison fine de 2-3 finalistes seulement (illisible au-delà).

**Limite du dataset.** OVR/PAC/DRI/etc. sont des notes issues d'un jeu vidéo (FIFA/FC),
pas des mesures GPS ou statistiques de match réelles : elles reflètent l'équilibrage du
jeu et l'avis des évaluateurs du studio, pas nécessairement la performance sur le terrain.
Par ailleurs certaines ligues (ex. championnats féminins, 2e divisions) sont sous-
représentées, ce qui rend les comparaisons par championnat moins fiables statistiquement
quand l'échantillon filtré devient petit.

## Organisation du code
```
Constantes/Input_data.py   → constantes + chargement du CSV (mis en cache)
Main.py                    → orchestration Streamlit (aucun calcul métier)
Src/Barre_filtre.py        → widgets de filtre (sidebar)
Src/Analyse/Filtre.py      → application des filtres au dataframe
Src/Analyse/Tri.py         → tri du tableau des meilleurs profils
Src/Graphiques/Scatter.py  → nuage de points (relation)
Src/Graphiques/Aire.py     → histogramme, boxplot, radar
```

## Lancer en local
```
pip install -r requirements.txt
streamlit run Main.py
```
