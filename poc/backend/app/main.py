from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router, get_current_user
from .video import router as video_router
from .chat import router as chat_router
from .alerts import router as alerts_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth_router, prefix='/auth')
app.include_router(video_router, prefix='/videos', dependencies=[Depends(get_current_user)])
app.include_router(alerts_router, prefix='/alerts', dependencies=[Depends(get_current_user)])
app.include_router(chat_router, prefix='/chat', dependencies=[Depends(get_current_user)])
