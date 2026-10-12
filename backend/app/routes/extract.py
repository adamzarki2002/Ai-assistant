from fastapi import APIRouter, Query
from app.services.diffbot_service import extract_article_diffbot
# from app.services.scraper import extract_article_scraper  # Optionnel si fallback

router = APIRouter()

@router.get("/extract")
def extract_from_url(url: str = Query(..., description="URL de l'article")):
    # ✅ Appel principal à Diffbot
    abstract = extract_article_diffbot(url)

    # 🔁 Fallback scraping si échec (optionnel)
    if abstract.lower() in ["", "abstract non disponible", "aucun contenu trouvé"]:
        from app.services.scraper import extract_article_scraper
        abstract = extract_article_scraper(url)

    return {"abstract": abstract}
