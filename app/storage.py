import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_project_intents(project_id: int):
    # TEMP: hardcoded utterances for testing

    intents = {
        "get_rain_chances": [
            "Will it rain today",
            "What are the chances it will rain today",
            "How likely is it to rain",
            "What are the rain chances for today",
            "Is it going to rain today",
            "Do I need an umbrella today",
            "Is rain expected today",
        ],

        "get_weather_forecast": [
            "What’s the weather today",
            "What will the weather be like today",
            "Give me today’s weather forecast",
            "What’s the forecast for today",
            "How’s the weather looking today",
        ],

        "get_temperature": [
            "What’s the temperature right now",
            "How hot is it today",
            "What’s today’s high temperature",
            "What’s the low for tonight",
            "Is it going to be cold today",
        ],

        "get_current_time": [
            "What time is it",
            "Tell me the current time",
            "Do you know what time it is",
            "What’s the time right now",
        ],

        "get_current_date": [
            "What’s today’s date",
            "What day is it today",
            "Tell me today’s date",
            "What date is it",
        ],

        "define_word": [
            "What does serendipity mean",
            "Define the word ephemeral",
            "What is the meaning of resilience",
            "Can you define the word ambiguous",
        ],
    }

    # Encode all utterances for each intent
    encoded_intents = {}
    for intent_name, utterance_list in intents.items():
        embeddings = model.encode(utterance_list)
        encoded_intents[intent_name] = embeddings

    return encoded_intents
