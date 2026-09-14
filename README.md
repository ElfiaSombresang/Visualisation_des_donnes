# Outil de scouting — README

**Question métier.** La cellule de recrutement veut filtrer rapidement les
~17 700 joueurs du dataset pour répondre à des demandes type « un ailier
rapide et bon dribbleur, hors des cinq grands championnats, OVR > 75 », sans
écrire de code à chaque nouvelle recherche.

**Choix des filtres.** Trois filtres minimum imposés : championnat (avec un
raccourci pour exclure les 5 grands championnats), poste, et un seuil
numérique — ici deux seuils (OVR et PAC) car la demande porte à la fois sur
le niveau général et la vitesse.

**Choix des graphiques.**
- *Histogramme (distribution)* sur l'OVR : répond à « le vivier retenu est-il
  large ou restreint ? », nécessaire avant de creuser plus loin.
- *Boxplot (comparaison de groupes)* de l'OVR par championnat (top 8
  représentés, une seule couleur, axes partagés) : répond à « quel
  championnat scouter en priorité ? » sans multiplier les couleurs.
- *Nuage de points (relation)* PAC vs DRI, couleur séquentielle sur l'OVR :
  répond directement à « qui cumule vitesse et dribble ? », le cœur de la
  demande du directeur sportif.

**Limite du dataset.** Les notes (OVR, PAC, DRI…) sont des évaluations issues
d'un jeu vidéo (EA FC), pas des statistiques mesurées en match : elles
reflètent un jugement d'expert simplifié, pas la performance réelle sur le
terrain, et la couverture des championnats mineurs est probablement moins
fiable que celle des grands championnats.

## Lancer en local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publier
Pousser ce dossier sur GitHub puis déployer sur https://share.streamlit.io
(fichier principal : `app.py`).
