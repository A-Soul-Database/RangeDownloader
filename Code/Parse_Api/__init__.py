from urllib.parse import  unquote
from . import Parser as Ps

##### Fast Api Config #####
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
Api = FastAPI()
origins = ["https://livedb.asoulfan.com","http://localhost","*"]
Api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
############ End #############

Extracts = [
    "bilibili.com","asoul-rec.com","knaifen.workers.dev","rec.ddindexs.com","alist.ddindexs.com"
]

class Parse_Model(BaseModel):
    url:str

class Parse_Template():
    Url:str
    Args:str=""
    Download_Url:str
    Play_Html:str
    Web_Title:str
    Save_Name:str
    Video_Format:str="mp4"
    Download_Tool:str="ffmpeg"
    Dash : bool = False
    
@Api.get("/ping")
def ping():
    return "Parse_Api pong"


@Api.post("/Parse")
def Parse(Parse_Model_Url:Parse_Model):
    url = Parse_Model_Url.url
    Temp = Parse_Template()
    Temp.Url = url
    Special = False
    for item in Extracts:
        if item in url:
            Special = True
            del Temp
            Temp = Ps.Parse(url)
    if Special==False:
        Temp.Download_Url= url
        Temp.Play_Html = f"<video src='{url}' controls></video>"
        Temp.Web_Title = url.split("/")[-1].replace("?","").replace(" ","")
        Temp.Save_Name = url.split("/")[-1].replace("?","").replace(" ","")
    #Temp.Download_Url = unquote(Temp.Download_Url)
    Temp.Play_Html = unquote(Temp.Play_Html)
    Temp.Save_Name = unquote(Temp.Save_Name)
    return Temp

@Api.get("/Save_BiliBili_Cookie/{cookie:path}")
def Save_BiliBili_Cookie(Cookie:str):
    return Ps.Save_BiliBili_Cookie(Cookie)

@Api.get("/Get_BiliBili_Cookie")
def Get_BiliBili_Cookie():
    return Ps.Get_BiliBili_Cookie()
