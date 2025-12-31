import pickle
from pathlib import Path

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def save_project_embeddings(project_id: int, embeddings: dict):
    with open(MODEL_DIR / f"project_{project_id}.pkl", "wb") as f:
        pickle.dump(embeddings, f)

def load_project_embeddings(project_id: int):
    path = MODEL_DIR / f"project_{project_id}.pkl"
    if path.exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_project_entities(project_id: int, entities: list):
    """
    Save raw entity definitions.
    Could be:
    - JSON file
    - SQLite
    - Postgres
    """
    pass  # Implement as needed

def load_project_entities(project_id: int):
    """
    Load raw entity definitions.
    Could be:
    - JSON file
    - SQLite
    - Postgres
    """
    pass  # Implement as needed