"""
Intégration API PlayerElo (https://playerelo.football/api-access) : récupère
la valeur marchande estimée d'un joueur à partir de son nom.

Limite connue de l'API publique : pas d'endpoint de recherche par nom,
seulement /v1/players (classement par Elo, paginé). On scanne donc ce
classement page par page pour trouver une correspondance exacte de nom,
avec un nombre de pages plafonné par défaut pour préserver le quota gratuit
(500 requêtes/mois, 10/min). Résultats mis en cache pour ne jamais
interroger deux fois le même joueur.
"""

import requests
import streamlit as st

BASE_URL = "https://data-api.playerelo.football"


def _headers():
    cle_api = st.secrets.get("PLAYERELO_API_KEY", "")
    if not cle_api:
        raise RuntimeError(
            "Clé API PlayerElo manquante. Ajoute-la dans .streamlit/secrets.toml "
            "(clé PLAYERELO_API_KEY) — à obtenir gratuitement sur "
            "https://playerelo.football/api-access."
        )
    return {"Authorization": f"Bearer {cle_api}"}


@st.cache_data(ttl=86400, show_spinner=False)
def _trouver_id_joueur(nom: str, pages_max: int = 5, taille_page: int = 100):
    """Cherche un joueur par nom exact (insensible à la casse) dans le
    classement Elo, en scannant au plus `pages_max` pages. Renvoie l'ID
    PlayerElo, ou None si non trouvé dans les pages scannées."""
    for page in range(pages_max):
        reponse = requests.get(
            f"{BASE_URL}/v1/players",
            headers=_headers(),
            params={"limit": taille_page, "offset": page * taille_page},
            timeout=10,
        )
        reponse.raise_for_status()
        joueurs = reponse.json()
        if not joueurs:
            break
        for j in joueurs:
            if j.get("player_name", "").strip().lower() == nom.strip().lower():
                return j.get("player_id") or j.get("id")
    return None


@st.cache_data(ttl=86400, show_spinner=False)
def get_valeur_marchande(nom_joueur: str):
    """Renvoie la valeur marchande estimée (€) d'un joueur, ou None si
    introuvable (nom absent des pages scannées, ou hors périmètre PlayerElo)."""
    id_joueur = _trouver_id_joueur(nom_joueur)
    if id_joueur is None:
        return None

    reponse = requests.get(
        f"{BASE_URL}/v1/players/{id_joueur}/value",
        headers=_headers(),
        timeout=10,
    )
    if reponse.status_code != 200:
        return None
    return reponse.json().get("value")
