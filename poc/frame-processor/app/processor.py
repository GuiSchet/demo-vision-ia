import os
import tempfile
import boto3
import cv2
from .utils import get_image_embedding
from qdrant_client import QdrantClient


class FrameProcessor:
    def __init__(self, cfg):
        self.s3 = boto3.client('s3', endpoint_url=cfg['s3_endpoint'])
        self.bucket = cfg['s3_bucket']
        self.qdrant = QdrantClient(url=cfg['vector_db_url'])
        self.interval = cfg.get('frame_interval_sec', 5)
        self.llm_api_url = cfg['llm_api_url']
        self.llm_api_key = cfg['llm_api_key']
        self.processed = set()

    def list_videos(self):
        resp = self.s3.list_objects_v2(Bucket=self.bucket)
        return [obj['Key'] for obj in resp.get('Contents', []) if obj['Key'].endswith('.mp4')]

    def check_new_videos(self):
        for key in self.list_videos():
            if key not in self.processed:
                self.process_video(key)
                self.processed.add(key)

    def process_video(self, key):
        with tempfile.NamedTemporaryFile(suffix='.mp4') as tmp:
            self.s3.download_fileobj(self.bucket, key, tmp)
            tmp.flush()
            cap = cv2.VideoCapture(tmp.name)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_no = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_no % int(fps * self.interval) == 0:
                    _, buf = cv2.imencode('.jpg', frame)
                    emb = get_image_embedding(buf.tobytes(), self.llm_api_url, self.llm_api_key)
                    payload = {'video_key': key, 'timestamp': frame_no / fps}
                    self.qdrant.upload_collection_if_not_exists('frames', 768)
                    self.qdrant.add('frames', vectors=[emb], payloads=[payload])
                frame_no += 1
            cap.release()
