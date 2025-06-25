from fastapi import APIRouter, Body
from qdrant_client import QdrantClient
import requests
import os
from typing import List
from pydantic import BaseModel

router = APIRouter()

qdrant = QdrantClient(url=os.getenv('VECTOR_DB_URL', 'http://qdrant:6333'))
llm_api_url = os.getenv('QWEN_API_URL', '')
llm_api_key = os.getenv('QWEN_API_KEY', '')

class ChatMessage(BaseModel):
    message: str

def text_embedding(text: str):
    resp = requests.post(llm_api_url + '/embedding', 
                        headers={'Authorization': f'Bearer {llm_api_key}'}, 
                        json={'text': text})
    resp.raise_for_status()
    return resp.json().get('embedding', [])

def get_context_from_vector_db(text: str) -> List[dict]:
    emb = text_embedding(text)
    results = qdrant.search(
        collection_name='frames',
        query_vector=emb,
        limit=5
    )
    return [{"video_key": r.payload.get('video_key'),
             "timestamp": r.payload.get('timestamp'),
             "text": r.payload.get('text', '')} for r in results]

@router.post('/')
def chat(message: ChatMessage):
    try:
        # Obtener contexto relevante de la base vectorial
        context = get_context_from_vector_db(message.message)
        
        # Construir el prompt con el contexto
        context_text = "\n".join([f"- {c['text']}" for c in context])
        prompt = f"""Basado en el siguiente contexto de los videos:
{context_text}

Pregunta del usuario: {message.message}

Por favor, responde la pregunta usando solo la información proporcionada en el contexto."""

        # Llamar al LLM para obtener la respuesta
        resp = requests.post(
            llm_api_url + '/chat',
            headers={'Authorization': f'Bearer {llm_api_key}'},
            json={'prompt': prompt}
        )
        resp.raise_for_status()
        
        return {
            "response": resp.json().get('response', 'Lo siento, no pude procesar tu pregunta.')
        }
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {
            "response": "Lo siento, ocurrió un error al procesar tu pregunta."
        }
