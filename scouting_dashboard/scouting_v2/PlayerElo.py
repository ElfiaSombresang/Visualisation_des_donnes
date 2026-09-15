"""
Intégration API PlayerElo (https://playerelo.football/api-access) : récupère
la valeur marchande estimée d'un joueur à partir de son nom.

Limites connues de l'API gratuite :
- 500 requêtes/mois, 10 requêtes/minute.
- Pas d'endpoint de recherche par nom : on scanne /v1/players (classement
  par Elo, paginé) page par page jusqu'à trouver une correspondance exacte.
Ce module espace les appels et réessaie automatiquement en cas de 429
(limite de débit atteinte), en respectant l'en-tête Retry-After si l'API
le fournit.
"""

import time
import requests
import streamlit as st

BASE_URL = "https://data-api.playerelo.football"
DELAI_ENTRE_APPELS = 6.5  # secondes ; > 60/10 pour rester sous 10 req/min
NB_ESSAIS_MAX = 3


def _headers():
    cle_api = st.secrets.get("PLAYERELO_API_KEY", "")
    if not cle_api:
        raise RuntimeError(
            "Clé API PlayerElo manquante. Ajoute-la dans .streamlit/secrets.toml "
            "(clé PLAYERELO_API_KEY) — à obtenir gratuitement sur "
            "https://playerelo.football/api-access."
        )
    return {"Authorization": f"Bearer {cle_api}"}


def _appel_avec_retry(url, params=None):
    """Fait un GET en réessayant automatiquement sur 429, en respectant
    Retry-After si présent, jusqu'à NB_ESSAIS_MAX tentatives. Renvoie la
    réponse, ou None si toujours bloqué après plusieurs essais."""
    for essai in range(NB_ESSAIS_MAX):
        reponse = requests.get(url, headers=_headers(), params=params, timeout=10)

        if reponse.status_code == 429:
            attente = int(reponse.headers.get("Retry-After", 10))
            if essai < NB_ESSAIS_MAX - 1:
                time.sleep(attente)
                continue
            return None  # toujours bloqué après plusieurs essais

        reponse.raise_for_status()
        time.sleep(DELAI_ENTRE_APPELS)  # espace l'appel suivant, même en cas de succès
        return reponse

    return None


@st.cache_data(ttl=86400, show_spinner=False)
def _trouver_id_joueur(nom: str, pages_max: int = 2, taille_page: int = 100):
    """Cherche un joueur par nom exact (insensible à la casse) dans le
    classement Elo, en scannant au plus `pages_max` pages (réduit par
    défaut à 2 pour limiter la consommation de quota). Renvoie l'ID
    PlayerElo, ou None si non trouvé ou si l'API reste indisponible."""
    for page in range(pages_max):
        reponse = _appel_avec_retry(
            f"{BASE_URL}/v1/players",
            params={"limit": taille_page, "offset": page * taille_page},
        )
        if reponse is None:
            return None  # limite de débit toujours atteinte : on abandonne proprement

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
    introuvable (nom absent des pages scannées, ou API indisponible)."""
    id_joueur = _trouver_id_joueur(nom_joueur)
    if id_joueur is None:
        return None

    reponse = _appel_avec_retry(f"{BASE_URL}/v1/players/{id_joueur}/value")
    if reponse is None:
        return None
    return reponse.json().get("value")