from fastapi import APIRouter, HTTPException
from app.schemas import TrainRequest, PredictRequest, PredictResponse
from app.training import train_project, project_entity_cache
from app.intent_engine import predict_intent

router = APIRouter()

@router.post("/train")
def train(data: TrainRequest):
    train_project(data.project_id, data.intents)
    return {"status": "success"}

@router.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    intent, confidence, alternatives, entities = predict_intent(
        project_id=data.project_id,
        text=data.text,
    )

    if intent is None:
        raise HTTPException(status_code=404, detail="No intent matched")
    
    # ✅ Removed the duplicate extract_entities() call
    # The entities are already extracted inside predict_intent()

    return PredictResponse(
        intent=intent,
        confidence=confidence,
        alternatives=alternatives,
        entities=entities,
    )