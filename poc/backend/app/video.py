from fastapi import APIRouter
import boto3
import os

router = APIRouter()

s3 = boto3.client('s3', endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://minio:9000'))
bucket = os.getenv('MINIO_BUCKET', 'cctv')

@router.get('/list')
def list_videos():
    resp = s3.list_objects_v2(Bucket=bucket)
    return [obj['Key'] for obj in resp.get('Contents', []) if obj['Key'].endswith('.mp4')]

@router.post('/reprocess')
def reprocess(video: str):
    # stub: real implementation would trigger reprocessing
    return {"status": "queued", "video": video}
