from . import FFmpeg_Core
from . import Installation
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

FFmpeg_api = FastAPI()
origins = ["https://livedb.asoulfan.com","http://localhost","*"]
FFmpeg_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#####
class Seek(BaseModel):
    Start_Time:int
    End_Time:int
    Url:str
    Save_Name:str
    Seek_type:str="Input"
    Threads:int=4
    Args:str=""

@FFmpeg_api.get("/ping")
def ping():
    return "ffmpeg_api pong"

@FFmpeg_api.get("/Detect")
def a():
    return Installation.Detect_FFmpeg()

@FFmpeg_api.get("/Install_FFmpeg")
def b():
    return Installation.Install_FFmpeg()

@FFmpeg_api.post("/Seek")
def c(Seek_Item:Seek):
    return FFmpeg_Core.Multi_Thread_Seeking(Start_Time=Seek_Item.Start_Time,End_Time=Seek_Item.End_Time,
    Url=Seek_Item.Url,Save_Name=Seek_Item.Save_Name,Seek_type=Seek_Item.Seek_type,Threads=Seek_Item.Threads,Args=Seek_Item.Args)

@FFmpeg_api.get("/Progress")
def d():
    return FFmpeg_Core.Get_Progress()

@FFmpeg_api.get("/thread_operation")
def e(Uniq_ID:str,Instance_id:int,Running:int):
    return FFmpeg_Core.thread_operation(Uniq_ID,Instance_id,Running)

@FFmpeg_api.get("/Open_Folder")
def open_folder(Save_Name:str=""):
    os.system(f"explorer {os.getcwd()}")

@FFmpeg_api.get("/Install_Progress")
def f():
    return Installation.Get_Progress()