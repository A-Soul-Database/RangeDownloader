# *-* coding:utf-8 -*-
APPVERSION = "V2.2.2" # Semantic Versioning
import webbrowser
import requests
import uvicorn
import Parse_Api
import ffmpeg_core
import uvicorn
from threading import Thread
import time
import sys
import tkinter.messagebox

def Check_Update():
    try:
        release_info = requests.get("https://api.github.com/repos/A-Soul-Database/RangeDownloader/releases/latest",timeout=0.5).json()
        latest_tag,release_body = release_info["tag_name"] , release_info["body"]
        if latest_tag != APPVERSION:
            return tkinter.messagebox.askokcancel(title="版本更新", message=f"小伙伴你好,分段下载有更新了!\n更新日志: {release_body}\n 点击 “确定” 跳转更新\n点击 “取消” 忽略")
        else:
            return False
    except Exception as e:
        print(f"Check Latest Version Failed {e}")
        return False


## Start Two Serivices
t1 = Thread(target=uvicorn.run,kwargs=({"app":ffmpeg_core.FFmpeg_api,"port":4399}),daemon=True)
t2 = Thread(target=uvicorn.run,kwargs=({"app":Parse_Api.Api,"port":4400}),daemon=True)
t1.start()
t2.start()
if Check_Update():
    webbrowser.open("https://github.com/A-Soul-Database/RangeDownloader/releases/latest")
else:
    webbrowser.open("https://rd.asdb.live")
    #webbrowser.open("https://asdb.live")
    ...
print("服务已启动")
while True:
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        print("Exit")
        sys.exit()
