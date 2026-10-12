# AI Literature Research Assistant

A full-stack assistant for scientific literature research: search papers across several open databases, rank them by relevance with machine learning, extract full texts and discuss them with an LLM-powered chat.

## Features

- **Multi-source search** – queries Crossref, Europe PMC, Semantic Scholar and arXiv in one request
- **Relevance screening** – ranks results with ASReview (TF-IDF + SVM) and semantic similarity (Sentence Transformers)
- **Full-text extraction** – extracts article content from URLs (Diffbot API or scraper fallback)
- **AI chat assistant** – asks questions about papers via LLMs through the OpenRouter API
- **Dashboard & visualizations** – result statistics with Chart.js, recent searches, collections
- **Multilingual UI** – German and English (vue-i18n)

## Tech stack

| Layer | Technologies |
| --- | --- |
| Backend | Python, FastAPI, Uvicorn, httpx, Pydantic, MongoDB (Motor), ASReview |
| Frontend | Vue 3, TypeScript, Vite, Pinia, Vue Router, Tailwind CSS, Chart.js |
| AI / ML | OpenRouter (LLM), ASReview, Sentence Transformers, PyTorch, scikit-learn, BeautifulSoup |

## Project structure

```
backend/
  app/
    main.py            # FastAPI app, CORS, router registration
    routes/            # /api/search, /api/chat, /api/extract, /api/asreview/filter
    services/          # OpenRouter, Diffbot, scraper, ML scoring
    models/            # Pydantic schemas
  requirements.txt
frontend/
  src/
    views/             # Search, results, chat, documents, collections
    components/        # Dashboard, search and layout components
    locales/           # de / en translations
```

## Getting started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your API keys
uvicorn app.main:app --reload
```

The API runs on `http://localhost:8000` (interactive docs at `/docs`).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app runs on `http://localhost:5173`.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/search?q=` | Search papers across all sources |
| POST | `/api/asreview/filter` | Rank articles by relevance |
| GET | `/api/extract?url=` | Extract the full text of an article |
| POST | `/api/chat` | Ask the AI assistant |

## Author

Adam Zarki – [LinkedIn](https://linkedin.com/in/adam-zarki-b259912b3)
