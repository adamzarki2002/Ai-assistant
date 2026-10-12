import requests
from bs4 import BeautifulSoup

def extract_article_scraper(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tentatives génériques
        selectors = [
            'section#abstract',
            'div.abstract',
            'div#abstract',
            'meta[name="description"]',
            'meta[name="dc.Description"]',
        ]

        for selector in selectors:
            if selector.startswith('meta'):
                tag = soup.select_one(selector)
                if tag and tag.get('content'):
                    return tag['content']
            else:
                tag = soup.select_one(selector)
                if tag and tag.text.strip():
                    return tag.text.strip()

        return "Abstract non trouvé."
    except Exception as e:
        return f"Erreur lors du scraping : {str(e)}"
