from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from asreview.models.classifiers import SVMClassifier
from asreview.models.feature_extraction import Tfidf

router = APIRouter()


@router.post("/asreview/filter")
async def filter_articles(request: Request):
    try:
        data = await request.json()
        articles = data.get("articles", [])
        if not articles:
            return JSONResponse(content={"error": "Pas d'articles fournis"}, status_code=400)

        df = pd.DataFrame(articles)

        required_cols = {"title", "abstract", "authors", "year", "source"}
        if not required_cols.issubset(df.columns):
            return JSONResponse(
                content={"error": "Colonnes requises manquantes", "details": list(required_cols - set(df.columns))},
                status_code=400
            )

        df["text"] = df["title"].astype(str) + " " + df["abstract"].astype(str)
        df = shuffle(df, random_state=42).reset_index(drop=True)

        vectorizer = Tfidf()
        X = vectorizer.fit_transform(df["text"])
        y_dummy = np.tile([0, 1], len(df) // 2 + 1)[:len(df)].flatten()

        model = SVMClassifier()
        model.fit(X, y_dummy)

        df["score"] = model.predict_proba(X).astype(float)

        df_sorted = df.sort_values("score", ascending=False)

        return JSONResponse(content=df_sorted.to_dict(orient="records"))

    except Exception as e:
        return JSONResponse(content={"error": "Erreur interne", "details": str(e)}, status_code=500)
