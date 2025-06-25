from fastapi import APIRouter
import boto3
import os
from datetime import timedelta

router = APIRouter()

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://minio:9000'),
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
)
bucket = os.getenv('MINIO_BUCKET', 'cctv')

def get_presigned_url(key: str, expires_in: int = 3600):
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expires_in
    )

@router.get('/')
def list_videos():
    try:
        resp = s3.list_objects_v2(Bucket=bucket)
        videos = []
        for obj in resp.get('Contents', []):
            if obj['Key'].endswith('.mp4'):
                video_url = get_presigned_url(obj['Key'])
                thumbnail_key = obj['Key'].replace('.mp4', '.jpg')
                try:
                    s3.head_object(Bucket=bucket, Key=thumbnail_key)
                    thumbnail_url = get_presigned_url(thumbnail_key)
                except:
                    thumbnail_url = None
                
                videos.append({
                    "id": obj['Key'],
                    "title": obj['Key'].split('/')[-1].replace('.mp4', ''),
                    "url": video_url,
                    "thumbnail_url": thumbnail_url,
                    "description": f"Video capturado el {obj['LastModified'].strftime('%d/%m/%Y')}"
                })
        return videos
    except Exception as e:
        print(f"Error listing videos: {e}")
        return []

@router.get('/{video_id}')
def get_video(video_id: str):
    try:
        obj = s3.head_object(Bucket=bucket, Key=video_id)
        video_url = get_presigned_url(video_id)
        thumbnail_key = video_id.replace('.mp4', '.jpg')
        try:
            s3.head_object(Bucket=bucket, Key=thumbnail_key)
            thumbnail_url = get_presigned_url(thumbnail_key)
        except:
            thumbnail_url = None
        
        return {
            "id": video_id,
            "title": video_id.split('/')[-1].replace('.mp4', ''),
            "url": video_url,
            "thumbnail_url": thumbnail_url,
            "description": f"Video capturado el {obj['LastModified'].strftime('%d/%m/%Y')}"
        }
    except Exception as e:
        print(f"Error getting video {video_id}: {e}")
        return None

@router.post('/reprocess')
def reprocess(video: str):
    # stub: real implementation would trigger reprocessing
    return {"status": "queued", "video": video}
