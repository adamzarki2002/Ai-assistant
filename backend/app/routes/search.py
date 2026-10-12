from fastapi import APIRouter, Query, Body
from fastapi.responses import JSONResponse
import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
from app.services.diffbot_service import extract_article_diffbot
from app.services.ml_model import score_articles
router = APIRouter()
cached_documents = {}

def clean_jats(abstract: str) -> str:
    return re.sub(r'<[^>]+>', '', abstract).strip()

def normalize_id(doi: str) -> str:
    return doi.replace("/", "_").replace(".", "_")

def restore_id(encoded: str) -> str:
    return encoded.replace("_", "/")

@router.get("/search")
def search_articles(q: str = Query(..., description="Mot-clé de recherche")):
    results = []
    LIMIT = 200

    # CrossRef
    try:
        url = f"https://api.crossref.org/works?query={q}&rows={LIMIT}"
        res = requests.get(url)
        for item in res.json().get("message", {}).get("items", []):
            doi = item.get("DOI", "")
            results.append({
                "title": item.get("title", [""])[0],
                "source": item.get("container-title", [""])[0] if item.get("container-title") else "CrossRef",
                "year": item.get("issued", {}).get("date-parts", [[None]])[0][0],
                "doi": doi,
                "url": item.get("URL", f"https://doi.org/{doi}") if doi else "",
                "authors": [f"{a.get('given', '')} {a.get('family', '')}" for a in item.get("author", [])] if item.get("author") else [],
                "abstract": clean_jats(item.get("abstract", "") or ""),
                "keywords": [],
                "metrics": {"relevance": 75, "methodQuality": 70, "novelty": 80, "impactFactor": 2.5},
                "sections": [], "references": 0, "figures": 0, "tables": 0,
            })
    except Exception as e:
        print("CrossRef Error:", e)

    # EuropePMC
    try:
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&pageSize={LIMIT}"
        res = requests.get(url)
        for item in res.json().get("resultList", {}).get("result", []):
            full_text_url = ""
            ft_list = item.get("fullTextUrlList", {}).get("fullTextUrl", [])
            if ft_list:
                full_text_url = ft_list[0].get("url", "")
            elif item.get("doi"):
                full_text_url = f"https://doi.org/{item['doi']}"

            results.append({
                "title": item.get("title", ""),
                "source": item.get("journalTitle", "EuropePMC"),
                "year": item.get("pubYear", ""),
                "doi": item.get("doi", ""),
                "url": full_text_url,
                "authors": item.get("authorString", "").split(", ") if item.get("authorString") else [],
                "abstract": clean_jats(item.get("abstract", "") or ""),
                "keywords": [],
                "metrics": {"relevance": 70, "methodQuality": 65, "novelty": 70, "impactFactor": 2.0},
                "sections": [], "references": 0, "figures": 0, "tables": 0,
            })
    except Exception as e:
        print("EuropePMC Error:", e)

    # Semantic Scholar
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&limit={LIMIT}&fields=title,year,venue,url,externalIds"
        res = requests.get(url)
        for item in res.json().get("data", []):
            doi = item.get("externalIds", {}).get("DOI", "")
            raw_url = item.get("url", "")
            doi_url = f"https://doi.org/{doi}" if doi else ""
            final_url = raw_url if raw_url and "semanticscholar.org" not in raw_url else doi_url

            results.append({
                "title": item.get("title", ""),
                "source": item.get("venue", "Semantic Scholar"),
                "year": item.get("year", ""),
                "doi": doi,
                "url": final_url,
                "authors": [],
                "abstract": "",
                "keywords": [],
                "metrics": {"relevance": 65, "methodQuality": 60, "novelty": 60, "impactFactor": 1.5},
                "sections": [], "references": 0, "figures": 0, "tables": 0,
            })
    except Exception as e:
        print("Semantic Scholar Error:", e)

    # arXiv
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{q}&start=0&max_results={LIMIT}"
        res = requests.get(url)
        root = ET.fromstring(res.text)
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
            published = entry.find("{http://www.w3.org/2005/Atom}published").text[:4]
            authors = [a.find("{http://www.w3.org/2005/Atom}name").text for a in entry.findall("{http://www.w3.org/2005/Atom}author")]
            paper_url = entry.find("{http://www.w3.org/2005/Atom}id").text.strip()

            results.append({
                "title": title,
                "source": "arXiv",
                "year": published,
                "doi": "",
                "url": paper_url,
                "authors": authors,
                "abstract": "",
                "keywords": [],
                "metrics": {"relevance": 60, "methodQuality": 60, "novelty": 70, "impactFactor": 1.2},
                "sections": [], "references": 0, "figures": 0, "tables": 0,
            })
    except Exception as e:
        print("arXiv Error:", e)

    # CORE
    try:
        core_url = f"https://core.ac.uk:443/api-v2/search/{q}?page=1&pageSize={LIMIT}&metadata=true"
        headers = {"Authorization": "Bearer YOUR_API_KEY_HERE"}
        res = requests.get(core_url, headers=headers)
        if res.status_code == 200:
            for item in res.json().get("data", []):
                landing = item.get("urls", {}).get("landingPage", "")
                download = item.get("downloadUrl", "")
                results.append({
                    "title": item.get("title", ""),
                    "source": "CORE",
                    "year": item.get("yearPublished", ""),
                    "doi": "",
                    "url": download or landing,
                    "authors": item.get("authors", []),
                    "abstract": clean_jats(item.get("abstract", "") or ""),
                    "keywords": [],
                    "metrics": {"relevance": 55, "methodQuality": 50, "novelty": 60, "impactFactor": 1.0},
                    "sections": [], "references": 0, "figures": 0, "tables": 0,
                })
    except Exception as e:
        print("CORE Error:", e)

    if "test openaccess" in q.lower():
        results.append({
            "title": "🧪 Test Article Lecture Directe",
            "source": "EuropePMC",
            "year": 2023,
            "doi": "10.1234/test.openaccess",
            "url": "https://europepmc.org/articles/PMC9448476",
            "authors": ["Dr. Lecteur"],
            "abstract": "Ceci est un test avec accès complet au texte via EuropePMC.",
            "keywords": ["test", "access", "epmc"],
            "metrics": {"relevance": 95, "methodQuality": 90, "novelty": 85, "impactFactor": 6.0},
            "sections": [], "references": 12, "figures": 3, "tables": 2,
        })

    results = [r for r in results if r.get("url", "").startswith("http") and "example.com" not in r["url"]]
    # 🔥 Classement intelligent par SBERT
    try:
        results = score_articles(q, results)
    except Exception as e:
        print("Erreur scoring ML :", e)
    return JSONResponse(content=results)

@router.post("/cache-document")
def cache_document(article: dict = Body(...)):
    from pprint import pprint
    print("🔄 Document reçu :")
    pprint(article)

    doi = article.get("doi", "")
    doc_id = normalize_id(doi) if doi else str(len(cached_documents) + 1)
    #print(f"📝 Document ajouté dans cache avec ID: {doc_id}")
    cached_documents[doc_id] = article
    return {"id": doc_id}

@router.get("/document/{id}")
def get_document(id: str):
    doc = cached_documents.get(id)
    if not doc:
        return JSONResponse(status_code=404, content={"detail": "Document not found"})
    return doc
@router.post("/fetch-abstract")
def fetch_abstract(payload: dict = Body(...)):
    url = payload.get("url")
    if not url:
        return JSONResponse(status_code=400, content={"detail": "URL manquante"})

    try:
        # Cas EuropePMC (PMCxxxxxxx)
        match = re.search(r'PMC(\d+)', url)
        if match:
            pmc_id = match.group(1)
            api_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/PMC{pmc_id}/abstractText"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200 and response.text.strip():
                return {"abstract": response.text.strip()}

        # Sinon, fallback avec Diffbot
        abstract = extract_article_diffbot(url)
        return {"abstract": abstract}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
