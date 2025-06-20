from fastapi import FastAPI, Depends
from .auth import router as auth_router, get_current_user
from .video import router as video_router
from .chat import router as chat_router

app = FastAPI()

app.include_router(auth_router, prefix='/auth')
app.include_router(video_router, prefix='/videos', dependencies=[Depends(get_current_user)])
app.include_router(chat_router, prefix='/chat', dependencies=[Depends(get_current_user)])
