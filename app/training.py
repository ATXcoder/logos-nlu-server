from sentence_transformers import SentenceTransformer
from app.persistence import save_project_embeddings, save_project_entities
from app.normalization import normalize
from app.intent_engine import project_embedding_cache,project_entity_cache

model = SentenceTransformer("all-MiniLM-L6-v2")

def train_project(
        project_id: int, 
        intents: dict,
        entities: list | None = None,
    ):
    
    embeddings = {}

    for intent_name, utterances in intents.items():
        cleaned = [normalize(u) for u in utterances]
        embeddings[intent_name] = model.encode(cleaned)

    project_embedding_cache[project_id] = embeddings
    save_project_embeddings(project_id, embeddings)

    # ----- Cache + persist entities (NO training) -----
    if entities is not None:
        project_entity_cache[project_id] = entities
        save_project_entities(project_id, entities)