import os
from minio import Minio

MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "secret123"
BUCKET_NAME = "cctv"
VIDEOS_DIR = "./videos"

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Crear bucket si no existe
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)

# Subir videos
for filename in os.listdir(VIDEOS_DIR):
    filepath = os.path.join(VIDEOS_DIR, filename)
    if os.path.isfile(filepath):
        print(f"Uploading {filename}...")
        client.fput_object(BUCKET_NAME, filename, filepath)
print("Done.") 