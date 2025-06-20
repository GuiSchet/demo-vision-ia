from fastapi import APIRouter, Body
from qdrant_client import QdrantClient
import requests
import os

router = APIRouter()

qdrant = QdrantClient(url=os.getenv('VECTOR_DB_URL', 'http://qdrant:6333'))
llm_api_url = os.getenv('QWEN_API_URL', '')
llm_api_key = os.getenv('QWEN_API_KEY', '')


def text_embedding(text: str):
    resp = requests.post(llm_api_url, headers={'Authorization': f'Bearer {llm_api_key}'}, json={'text': text})
    resp.raise_for_status()
    return resp.json().get('embedding', [])


@router.post('/query')
def query(text: str = Body(...)):
    emb = text_embedding(text)
    res = qdrant.search(collection_name='frames', query_vector=emb, limit=5)
    return [{"video_key": r.payload.get('video_key'), "timestamp": r.payload.get('timestamp')} for r in res]
