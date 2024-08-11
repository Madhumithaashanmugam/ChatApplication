# from fastapi import FastAPI, Depends, status,WebSocket
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.requests import Request
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from starlette.responses import Response
# from apis.chat_api import chat_api
# from apis.user_api import user_routers
# from apis.message_api import message_api
# import websocket_file
# websocket_file
# # main.py

# import asyncio
# import uvicorn
# from fastapi import FastAPI

# app = FastAPI()

# # Example long-running task
# async def long_running_task():
#     try:
#         while True:
#             # Simulate long-running work
#             await asyncio.sleep(1)
#     except asyncio.CancelledError:
#         print("Task was cancelled")
#         raise

# @app.on_event("startup")
# async def startup_event():
#     # Start any long-running tasks here
#     app.state.task = asyncio.create_task(long_running_task())

# @app.on_event("shutdown")
# async def shutdown_event():
#     # Cancel the long-running task on shutdown
#     app.state.task.cancel()
#     await app.state.task

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# if __name__ == "__main__":
#     try:
#         # Start the FastAPI server using uvicorn
#         asyncio.run(uvicorn.run(app, host="0.0.0.0", port=8000))
#     except KeyboardInterrupt:
#         print("Server shut down gracefully.")


# from dotenv import load_dotenv
# load_dotenv()

# from apis.auth import auth_router


        
# app = FastAPI(

#     title="Chat Application", docs_url="/api/docs", openapi_url="/api"
# )

# origins = ["*"]
# # Set all CORS enabled origins

# app.add_middleware(  # type: ignore
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     # request.state.db = SessionLocal()
#     response = await call_next(request)
#     # request.state.db.close()
#     return response


# app.include_router(auth_router, prefix="/api", tags=["auth"])
# app.include_router(message_api)
# app.include_router(chat_api)
# app.include_router(user_routers)


# #-------------------
# from websocket_file import websocket_endpoint
# from config.db.session import get_db
# from sqlalchemy.orm import Session

# app.include_router(message_api, prefix="/api")

# @app.websocket("/ws/{sender_id}")
# async def websocket_route(websocket: WebSocket, sender_id: str, db: Session = Depends(get_db)):
#     await websocket_endpoint(websocket, sender_id, db)
    
    
###################################################################################
# from fastapi import FastAPI, Depends, status, WebSocket
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.requests import Request
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from starlette.responses import Response
# from sqlalchemy.orm import configure_mappers  # Import configure_mappers here
# from apis.auth import auth_router
# from apis.chat_api import chat_api
# from apis.user_api import user_routers
# from apis.message_api import message_api
# import websocket_file
# websocket_file
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI(
#     title="Chat Application", docs_url="/api/docs", openapi_url="/api"
# )

# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Ensure all models are loaded before configuring mappers
# from models.chat.models import Chat
# from models.message.models import Message
# from models.users.models import User

# configure_mappers()  # Call configure_mappers after importing models

# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = await call_next(request)
#     return response

# app.include_router(auth_router, prefix="/api", tags=["auth"])
# app.include_router(message_api)
# app.include_router(chat_api)
# app.include_router(user_routers)

# from websocket_file import websocket_endpoint
# from config.db.session import get_db
# from sqlalchemy.orm import Session

# app.include_router(message_api, prefix="/api")

# @app.websocket("/ws/{sender_id}")
# async def websocket_route(websocket: WebSocket, sender_id: str, db: Session = Depends(get_db)):
#     await websocket_endpoint(websocket, sender_id, db)

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
app.include_router(auth_router)
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
