# Demo Vision IA Proof of Concept

This repository demonstrates a simple CCTV analysis stack. It uses MinIO for S3 compatible storage, Qdrant for vector search, a Python service that extracts frame embeddings, a FastAPI backend with JWT authentication and a React frontend.

## Directory layout

```
poc/
├── docker-compose.yml  # service definitions
├── .env                # API keys and secrets used by the compose stack
├── videos/             # example MP4 files preloaded into MinIO
├── scripts/
│   └── preload_videos.sh
├── frame-processor/    # extracts frames and uploads embeddings
├── backend/            # FastAPI application
└── frontend/           # minimal React client
```

## Services

- **minio** – stores uploaded videos using the credentials `admin`/`secret123`.
- **qdrant** – vector database that holds the frame embeddings.
- **frame-processor** – downloads new videos from MinIO, extracts frames with OpenCV and uploads embeddings to Qdrant.
- **api** – FastAPI server providing authentication, video listing and chat endpoints.
- **frontend** – React UI that consumes the API.

## Running the stack

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/).
2. Edit `poc/.env` and provide values for `QWEN_API_KEY` and `JWT_SECRET_KEY`.
3. From the `poc` directory run:

   ```bash
   docker-compose up --build
   ```

The backend will expose `http://localhost:8000` and the frontend will be available on `http://localhost:3000`.

## Using the application

- Obtain a token by sending a POST request to `/auth/login` with form fields `username` and `password` (default user is `admin`/`admin123`).
- List videos with `GET /videos/list` using the token.
- Issue chat queries with `POST /chat/query` sending JSON `{ "text": "your question" }`.

The frontend implements a very small React interface that lets you log in, view videos and query the chat endpoint.

## Deployment notes

The provided videos are empty placeholders. Replace the contents of `poc/videos` with real MP4 files before deploying. The compose stack will automatically upload them to MinIO on startup and the frame processor will begin generating embeddings.
