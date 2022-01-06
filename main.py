"""
    To Download a range file 
    Please Install and config Ffmpeg proprely.
"""
from urllib.parse import quote, urlparse, unquote
import Extract
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Extracts = [
    "www.bilibili.com","ali.asoul-rec.com","nf.asoul-rec.com" #It should obey the RFC 1808 rule.
]

class Get_Request_Body(BaseModel):
    url:str
    start:str
    end:str

@app.post("/api/v1/parse/{info:path}")
async def Parse(args:Get_Request_Body):
    url = args.url
    start = args.start.replace('：',":")
    end = args.end.replace('：',":")
    
    if urlparse(url).hostname in Extracts:
        Parser = Extract.Extract(url)
    else:
        Parser = {
            "args":"",
            "url":url,
            "name":url.split("/")[-1].split("?")[0].replace(" ","")
        }
    
    Parser["url"] = unquote(Parser["url"])
    Parser["name"] = unquote(Parser["name"])
    cmd = f"ffmpeg {Parser['args']} -ss {start} -i '{Parser['url']}'  -to {end} -c copy -y '{Parser['name']}'"
    Parser["cmd"] = cmd
    return Parser
