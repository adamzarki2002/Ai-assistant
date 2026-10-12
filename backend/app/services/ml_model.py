from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")  # rapide, léger

def score_articles(user_query: str, articles: list[dict]) -> list[dict]:
    texts = [a["title"] + " " + a["abstract"] for a in articles]
    embeddings = model.encode(texts, convert_to_tensor=True)
    query_emb = model.encode(user_query, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(query_emb, embeddings)[0]

    # Attache le score à chaque article
    for i, score in enumerate(cosine_scores):
        articles[i]["ml_score"] = float(score)

    # Trie les articles par pertinence ML
    articles.sort(key=lambda x: x["ml_score"], reverse=True)
    return articles
