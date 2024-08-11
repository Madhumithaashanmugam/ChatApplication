
###############################################################################################
from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import configure_mappers
from dotenv import load_dotenv

# Import routers
from apis.auth import auth_router
from apis.chat_api import chat_api
from apis.user_api import user_routers
from apis.message_api import message_api
import websocket_file
from config.db.session import get_db
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Chat Application",
    docs_url="/api/docs",
    openapi_url="/api"
)

# CORS middleware setup
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure all models are loaded before configuring mappers
from models.chat.models import Chat
from models.message.models import Message
from models.users.models import User

configure_mappers()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    return response

# Include routers
# app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(auth_router, prefix="/api")
app.include_router(message_api, prefix="/api")
app.include_router(chat_api)
app.include_router(user_routers)

@app.websocket("/ws/{sender_id}")
async def websocket_route(websocket: WebSocket, sender_id: str, db: Session = Depends(get_db)):
    await websocket_file.websocket_endpoint(websocket, sender_id, db)

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
