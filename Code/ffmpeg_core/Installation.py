# *-* coding:utf-8 -*-
import subprocess
import requests
from contextlib import closing
import zipfile
import shutil
import sys
Install_Stage = 0  #0:Not_Call_Yet, 1:Downloading, 2:Unizzping, 3:finishedDownload_Progress = 0.0
Download_Progress = 0.0
def Install_FFmpeg():
    global Install_Stage
    global Download_Progress

    def Unzip_Win():
        for i in zipfile.ZipFile("./ffmpeg.zip").namelist():
            if i.split("/")[-1] == "ffmpeg.exe":
                zipfile.ZipFile("./ffmpeg.zip").extract(i,"./")
                shutil.move(i,"./ffmpeg.exe")
                break

    def Unzip_Mac():
        for i in zipfile.ZipFile("./ffmpeg.zip").namelist():
            zipfile.ZipFile("./ffmpeg.zip").extract(i,"./")
    
    if sys.platform == "win32":
        Download_Url = "https://ghproxy.com/" \
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n4.4-latest-win64-lgpl-4.4.zip"
    if sys.platform == "darwin" : 
        Download_Url = "https://evermeet.cx/ffmpeg/ffmpeg-107037-ge9107d16f3.zip"
    if sys.platform == "Linux":
        return # Linux 自行用包管理安装是最方便的

    with closing(requests.session().get(Download_Url,stream=True)) as response:
        Install_Stage = 1
        chunk_size = 1024*1024
        content_size = int(response.headers['content-length'])
        data_count = 0
        with open("ffmpeg.zip", "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count += len(data)
                Download_Progress = round(data_count / content_size, 2) * 100
    
    Install_Stage = 2

    if sys.platform == "win32": Unzip_Win()
    if sys.platform == "darwin": Unzip_Mac()

def Detect_FFmpeg():
    try:
        subprocess.check_output(["ffmpeg", "-version"])
        return True
    except:
        return False

def Get_Progress():
    return {"Install_Stage":Install_Stage,"Download_Progress":Download_Progress}