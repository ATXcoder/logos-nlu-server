from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.entities import extract_entities
from app.persistence import load_project_embeddings
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Cache for embeddings per project
project_embedding_cache = {}

project_entity_cache = {}

def normalize(text: str) -> str:
    return text.lower().strip()

def predict_intent(
    project_id: int,
    text: str,
    top_n: int = 3,
    confidence_threshold: float = 0.55,
):
    # 🔁 Lazy load embeddings
    if project_id not in project_embedding_cache:
        embeddings = load_project_embeddings(project_id)
        if not embeddings:
            return None, 0.0, [], {}
        project_embedding_cache[project_id] = embeddings

    project_intents = project_embedding_cache.get(project_id)
    
    if not project_intents:
        return None, 0.0, [], {}

    input_vec = model.encode([text])[0]

    scores = []
    for intent_name, utterance_vectors in project_intents.items():
        # ✅ Fix: Check if utterance_vectors is empty or invalid
        if utterance_vectors is None or len(utterance_vectors) == 0:
            continue  # Skip intents with no training examples
        
        # ✅ Fix: Ensure utterance_vectors is 2D
        if isinstance(utterance_vectors, list):
            utterance_vectors = np.array(utterance_vectors)
        
        if utterance_vectors.ndim == 1:
            utterance_vectors = utterance_vectors.reshape(1, -1)
        
        sim_score = cosine_similarity([input_vec], utterance_vectors).max()
        scores.append((intent_name, float(sim_score)))

    # ✅ Handle case where no valid intents were found
    if not scores:
        return None, 0.0, [], {}

    scores.sort(key=lambda x: x[1], reverse=True)
    best_intent, best_score = scores[0]

    alternatives = [
        {"intent": intent, "confidence": score}
        for intent, score in scores[1 : top_n + 1]
    ]

    # ✅ Extract entities here
    entities = extract_entities(text)

    if best_score < confidence_threshold:
        return None, best_score, alternatives, entities

    return best_intent, best_score, alternatives, entities