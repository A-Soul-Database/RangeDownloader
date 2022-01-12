import FFmpeg_Core
import Installation

from fastapi import FastAPI
FFmpeg_api = FastAPI()
#####

@FFmpeg_api.get("/Detect")
def a():
    return Installation.Detect_FFmpeg()

    
@FFmpeg_api.get("/Install_FFmpeg")
def b():
    return Installation.Install_FFmpeg()

@FFmpeg_api.get("/Seek")
def c(Start_Time:int,End_Time:int,Url:str,Seek_type:str="Input",Threads:int=4,args:str=""):
    return FFmpeg_Core.Multi_Thread_Seeking(Start_Time,End_Time,Url,Seek_type,Threads,args)

@FFmpeg_api.get("/Progress")
def d(Uniq_ID:str):
    return FFmpeg_Core.Get_Progress(Uniq_ID)


@FFmpeg_api.get("/thread_operation")
def e(Uniq_ID:str,Instance_id:int,Running:int):
    return FFmpeg_Core.thread_operation(Uniq_ID,Instance_id,Running)

