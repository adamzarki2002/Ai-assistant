import requests
import os

DIFFBOT_TOKEN = os.getenv("DIFFBOT_TOKEN")

def extract_article_diffbot(url: str) -> str:
    if not DIFFBOT_TOKEN:
        return "Token Diffbot manquant"

    try:
        api_url = f"https://api.diffbot.com/v3/article"
        params = {
            "token": DIFFBOT_TOKEN,
            "url": url
        }

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Analyse la réponse
        objects = data.get("objects", [])
        if not objects:
            return "Aucun contenu trouvé"

        article = objects[0]
        abstract = article.get("text", "") or article.get("metaDescription", "")

        return abstract if abstract else "Abstract non disponible"
    except Exception as e:
        return f"Erreur lors de l'extraction : {str(e)}"
