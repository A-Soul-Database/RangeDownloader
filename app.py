# *-* coding:utf-8 -*-
import uvicorn
import Api
import ffmpeg_core
import uvicorn
from threading import Thread

## Start Two Serivices
def Run():
    t1 = Thread(target=uvicorn.run,kwargs=({"app":ffmpeg_core.FFmpeg_api,"port":4399,"debug":True}),daemon=True)
    t2 = Thread(target=uvicorn.run,kwargs=({"app":Api.Api,"port":4400,"debug":True}),daemon=True)
    t1.start()
    t2.start()