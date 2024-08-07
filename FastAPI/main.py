from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from dotenv import load_dotenv
load_dotenv()

from apis.user_api import user_routers
from apis.auth import auth_router

app = FastAPI(
    title="LMS", docs_url="/api/docs", openapi_url="/api"
)
app.include_router(auth_router)
app.include_router(user_routers)

origins = ["*"]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    return response




