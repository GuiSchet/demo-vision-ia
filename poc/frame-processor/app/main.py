import os
import tempfile
import boto3
from botocore.client import Config
import cv2
import requests
import time
import yaml
from qdrant_client import QdrantClient

def get_image_embedding(data: bytes, api_url: str, api_key: str):
    resp = requests.post(
        api_url,
        headers={'Authorization': f'Bearer {api_key}'},
        files={'image': ('frame.jpg', data, 'image/jpeg')}
    )
    resp.raise_for_status()
    return resp.json().get('embedding', [])

def load_config():
    config_path = 'config.yaml'  # Config file is in the same directory as main.py
    with open(config_path) as f:
        return yaml.safe_load(f)

def list_videos(s3, bucket):
    resp = s3.list_objects_v2(Bucket=bucket)
    return [obj['Key'] for obj in resp.get('Contents', []) if obj['Key'].endswith('.mp4')]

def process_video(s3, qdrant, bucket, key, interval, llm_api_url, llm_api_key):
    with tempfile.NamedTemporaryFile(suffix='.mp4') as tmp:
        s3.download_fileobj(bucket, key, tmp)
        tmp.flush()
        cap = cv2.VideoCapture(tmp.name)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_no = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_no % int(fps * interval) == 0:
                _, buf = cv2.imencode('.jpg', frame)
                emb = get_image_embedding(buf.tobytes(), llm_api_url, llm_api_key)
                payload = {'video_key': key, 'timestamp': frame_no / fps}
                qdrant.upload_collection_if_not_exists('frames', 768)
                qdrant.add('frames', vectors=[emb], payloads=[payload])
            frame_no += 1
        cap.release()

def ensure_bucket_exists(s3, bucket):
    try:
        s3.head_bucket(Bucket=bucket)
    except:
        s3.create_bucket(Bucket=bucket)

def main():
    cfg = load_config()
    s3 = boto3.client('s3',
                     endpoint_url=cfg['s3_endpoint'],
                     aws_access_key_id='admin',
                     aws_secret_access_key='secret123',
                     aws_session_token=None,
                     config=Config(signature_version='s3v4'),
                     verify=False)
    bucket = cfg['s3_bucket']
    ensure_bucket_exists(s3, bucket)  # Create bucket if it doesn't exist
    qdrant = QdrantClient(url=cfg['vector_db_url'])
    interval = cfg.get('frame_interval_sec', 5)
    llm_api_url = cfg['llm_api_url']
    llm_api_key = cfg['llm_api_key']
    processed = set()
    while True:
        for key in list_videos(s3, bucket):
            if key not in processed:
                process_video(s3, qdrant, bucket, key, interval, llm_api_url, llm_api_key)
                processed.add(key)
        time.sleep(10)

if __name__ == "__main__":
    print("Frame processor running...")
    main()
