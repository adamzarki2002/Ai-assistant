from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.openrouter import get_ai_response
from app.routes.search import cached_documents  # ⚠️ Assure-toi que ce module est bien importé

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")
    if not user_message:
        return {"reply": "❌ Aucune question reçue."}

    # 🔍 Regarder si des documents favoris sont cochés pour useInChat
    context = ""
    for doc in cached_documents.values():
        if doc.get("useInChat") is True:
            abstract = doc.get("abstract", "").strip()
            if abstract and abstract.lower() not in ["", "abstract not available", "erreur"]:
                context += f"- {doc.get('title', 'Untitled')}:\n{abstract}\n\n"

    # 🛑 Aucun contexte valide → refuser de répondre
    if not context:
        return JSONResponse(content={
            "reply": "🛑 No items selected with 'useInChat'. Please activate at least one item in your collection."
        })

    # ✅ Contexte disponible → construire prompt intelligent
    prompt = f"""Tu es un assistant intelligent.
Tu dois répondre à la question suivante uniquement en te basant sur les résumés ci-dessous.
Si l'information n'est pas disponible dans les résumés, dis simplement que tu ne peux pas répondre.

### Résumés d'articles :
{context}

### Question :
{user_message}
"""

    try:
        response = await get_ai_response(prompt)
        return {"reply": response}
    except Exception as e:
        return {"reply": f"❌ Erreur de communication avec OpenRouter : {str(e)}"}
