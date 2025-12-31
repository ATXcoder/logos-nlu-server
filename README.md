# Logos NLU

**Logos NLU** is a lightweight, self-hosted Natural Language Understanding (NLU) service for intent classification and entity extraction.

It is designed to be:
- ✅ Simple
- ✅ Inspectable
- ✅ Deterministic
- ✅ Free from cloud lock-in

Logos NLU focuses on **semantic intent detection using sentence embeddings**, not black-box AI pipelines.

---

## Why Logos NLU?

Most NLU systems are either:
- Overly complex
- Tied to SaaS platforms
- Hard to debug
- Impossible to extend cleanly

Logos NLU takes a different approach:
- Uses sentence embeddings + cosine similarity
- No retraining required after restart
- Intents and embeddings are persisted
- Entities are explicit and hackable

> If you can read Python, you can understand Logos NLU.

---

## Features

- 🧠 Semantic intent classification (SentenceTransformers)
- 📦 Project-based intent storage
- 💾 Persistent embeddings (no retrain on restart)
- 🧩 Simple entity extraction (regex & keyword-based)
- ⚡ FastAPI-based HTTP API
- 🧪 Easy to test and extend

---

## Non-Goals

Logos NLU intentionally does **not** aim to:
- Replace large LLMs
- Do generative AI
- Perform end-to-end dialogue management
- Hide complexity behind configuration magic

This is an **NLU engine**, not a chatbot.

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/logos-nlu.git
cd logos-nlu

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app.main:app --reload --port 8001
```
API will be available at `http://localhost:8001`

## Example Dataset

Logos NLU operates on projects.
Each project has:

- Intents
- Training utterances
- Stored embeddings

See: data/projects/example_project/intents.json

## Training a Project

Send training data to the training endpoint (or call train_project directly).

Example structure

```json
{
  "project_id": 1,
  "intents": {
    "greet": [
      "hello",
      "hi there",
      "hey"
    ],
    "order_pizza": [
      "I want to order a pizza",
      "Can I get a pepperoni pizza",
      "I'd like to order food"
    ]
  }
}
```

Training generates embeddings and persists them to disk.

## Predicting an Intent

Request

```http
POST /v1/predict
Content-Type: application/json
```
```json
{
  "project_id": 1,
  "text": "I want a large pepperoni pizza"
}
```

Response

```json
{
  "intent": "order_pizza",
  "confidence": 0.82,
  "alternatives": [
    { "intent": "greet", "confidence": 0.41 }
  ],
  "entities": {
    "size": "large",
    "topping": "pepperoni"
  }
}
```