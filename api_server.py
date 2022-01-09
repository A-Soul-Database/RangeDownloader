"""
    To Download a range file 
    Please Install and config Ffmpeg proprely.
"""
from urllib.parse import quote, urlparse, unquote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
import core
app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Get_Request_Body(BaseModel):
    url:str


@app.post("/api/v1/parse/info")
async def Parse(args:Get_Request_Body):
    return core.Parse(args)