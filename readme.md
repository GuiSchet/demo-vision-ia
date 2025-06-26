# Demo Vision IA · Proof-of-Concept

Un prototipo full-stack que combina análisis de vídeo CCTV con Large-Language-Models (LLM) para consultas en lenguaje natural. Permite cargar vídeos, extraer fotogramas representativos, indexarlos como embeddings y preguntar sobre el contenido a través de un chat.

---

## Arquitectura

- **MinIO** – Almacenamiento S3 para los vídeos y miniaturas.
- **Qdrant** – Base de datos vectorial donde se guardan los embeddings de los fotogramas.
- **Frame-Processor** – Servicio Python que descarga los MP4 desde MinIO, extrae frames con OpenCV, genera embeddings y los sube a Qdrant.
- **Backend (FastAPI)** – API REST con autenticación JWT que expone endpoints de vídeos, alertas y chat; interactúa con MinIO y Qdrant.
- **Frontend (Next.js 14 + shadcn-ui)** – Interfaz web que permite iniciar sesión, ver vídeos y conversar con el modelo.

> Diagrama simplificado: usuario ⇄ Frontend ⇄ Backend ⇄ {MinIO, Qdrant} ← Frame-Processor

---

## Estructura del repositorio

```text
poc/
├── docker-compose.yml   # Definición de la pila
├── backend/             # Servicio FastAPI (auth, vídeos, alertas, chat)
├── frame-processor/     # Extracción de frames y generación de embeddings
├── frontend/            # Aplicación Next.js 14
├── scripts/             # Utilidades de carga de vídeos
├── videos/              # MP4 de ejemplo para pruebas locales
└── .env                 # Claves | *no se sube al repo*
```

En la raíz encontrarás además un `.gitignore` actualizado y otros archivos de configuración del workspace.

---

## Requisitos

1. [Docker](https://docs.docker.com/get-docker/) + Docker Compose v2.
2. Crear `poc/.env` con:

```env
QWEN_API_KEY=<tu_token_qwen>
JWT_SECRET_KEY=<cualquier_cadena_segura>
```

---

## Puesta en marcha rápida

```bash
cd poc
docker compose up --build
```

Una vez construidas las imágenes:

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Frontend | http://localhost:3000 | – |
| Backend (OpenAPI) | http://localhost:8000/docs | – |
| MinIO Console | http://localhost:9001 | `admin` / `secret123` |
| Qdrant UI | http://localhost:6333/dashboard | – |

---

## Uso básico

1. Accede a la web e inicia sesión con `admin` / `admin123` (usuario sembrado en `backend/users.db`).
2. Explora la lista de vídeos y miniaturas.
3. Abre el chat y realiza preguntas del tipo «¿Qué sucede en el minuto 2?».
4. (Opcional) Sube nuevos `.mp4` al bucket `cctv` en MinIO; el *frame-processor* los detectará automáticamente.

---

## Desarrollo local

### Frontend

```bash
cd poc/frontend
pnpm install
pnpm dev
```

### Backend

```bash
cd poc/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frame-Processor

```bash
cd poc/frame-processor
pip install -r requirements.txt
python -m app.main
```

---

## Calidad de código

- **JavaScript/TypeScript** – [Biome](https://biomejs.dev/) + Prettier integrados (`frontend/biome.jsonc`).
- **Python** – [`ruff`](https://github.com/astral-sh/ruff) y `black` (ver `poc/backend/requirements.txt`).
- `.gitignore` actualizado para evitar subir artefactos de entorno, cachés y dependencias.

---

## Licencia

MIT © 2024 – Proyecto de demostración interno.
