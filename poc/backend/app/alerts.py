from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
from .video import get_presigned_url
import boto3
import os
import json

router = APIRouter()

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://minio:9000'),
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
)
bucket = os.getenv('MINIO_BUCKET', 'cctv')
alerts_prefix = 'alerts/'

class Alert(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    timestamp: datetime
    video_url: str
    thumbnail_url: str | None

@router.get('/', response_model=List[Alert])
def list_alerts():
    try:
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=alerts_prefix)
        alerts = []
        for obj in resp.get('Contents', []):
            if obj['Key'].endswith('.json'):
                try:
                    alert_obj = s3.get_object(Bucket=bucket, Key=obj['Key'])
                    alert_data = json.loads(alert_obj['Body'].read())
                    
                    # Obtener URLs firmadas para el video y thumbnail
                    video_url = get_presigned_url(alert_data['video_key'])
                    thumbnail_key = alert_data['video_key'].replace('.mp4', '.jpg')
                    try:
                        s3.head_object(Bucket=bucket, Key=thumbnail_key)
                        thumbnail_url = get_presigned_url(thumbnail_key)
                    except:
                        thumbnail_url = None
                    
                    alerts.append(Alert(
                        id=obj['Key'],
                        title=alert_data['title'],
                        description=alert_data['description'],
                        severity=alert_data['severity'],
                        timestamp=datetime.fromisoformat(alert_data['timestamp']),
                        video_url=video_url,
                        thumbnail_url=thumbnail_url
                    ))
                except Exception as e:
                    print(f"Error processing alert {obj['Key']}: {e}")
                    continue
        
        # Ordenar por timestamp descendente
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        return alerts
    except Exception as e:
        print(f"Error listing alerts: {e}")
        return [] 