from fastapi import FastAPI
from app.api import router
from app.persistence import load_project_embeddings

app = FastAPI(
    title="Intent NLU Service",
    version="0.1.0"
)

app.include_router(router, prefix="/v1")