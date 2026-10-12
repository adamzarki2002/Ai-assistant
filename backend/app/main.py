from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import chat_router
from app.routes.asreview import router as asreview_router
from app.routes.search import router as search_router
from app.routes.extract import router as extract_router
from app.routes import extract
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Assistant IA prêt 🚀"}

app.include_router(chat_router, prefix="/api")
app.include_router(asreview_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(extract_router, prefix="/api")
