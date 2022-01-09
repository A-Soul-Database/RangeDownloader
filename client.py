# -*- coding: UTF-8 -*-
from importlib.abc import PathEntryFinder
import zipfile
import requests
import webview
import base64
import subprocess
import json
import os
import core
from contextlib import closing
import shutil
from threading import Thread
me = os.popen("whoami").read().replace("\n","").split("\\")[1]
Download_path = "C:/Users/"+me+"/Downloads"

def detect_ffmpeg():
    """
        没有ffmpeg的话就要下载
    """
    with subprocess.Popen('ffmpeg -h',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as f:
        if len(str(f.stdout.read())):
            return True
        if len(str(f.stderr.read())):
            window.evaluate_js(f"alert('检测到没有必备组件ffmpeg,正在下载')")
            return download_ffmpeg()

ffmpeg = detect_ffmpeg()
Parse = {}
Download_Threads = []

class Get_Request_Body:
    url:str


def download_ffmpeg():
    ffmpeg = "https://mirror.ghproxy.com/https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n4.4-latest-win64-lgpl-4.4.zip"
    with closing(requests.session().get(ffmpeg,stream=True)) as response:
        chunk_size = 1024
        with open("ffmpeg.zip", "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
    for i in zipfile.ZipFile("./ffmpeg.zip").namelist():
        if i.split("/")[-1] == "ffmpeg.exe":
            zipfile.ZipFile("./ffmpeg.zip").extract(i,"./")
            shutil.move(i,"./ffmpeg.exe")
            break


def single_download(strat_time:str,end_time:str):
    def to_second(a:str):
        if a.count(":") == 1:
            return int(a.split(":")[0])*60 + int(a.split(":")[1])
        elif a.count(":") == 3:
            return int(a.split(":")[0])*3600 + int(a.split(":")[1])*60 + int(a.split(":")[2])
        else:
            return int(a)
    start = to_second(strat_time.replace("：",":"))
    end = to_second(end_time.replace("：",":"))
    if end<start:
        return window.evaluate_js(f"alert('错误:结束时间不能小于开始时间')")
    cmd = f'ffmpeg {Parse["args"]} -ss {start} -i "{Parse["download_url"]}"  -to {end-start} -c copy -y "{Download_path}/{Parse["Save_Name"]}"' if start > 0 else f'ffmpeg {Parse["args"]} -i "{Parse["download_url"]}" -to {end} -c copy -y "{Download_path}/{Parse["Save_Name"]}"'
    with subprocess.Popen(cmd,stdout=subprocess.PIPE) as proc:
        pass
    window.evaluate_js(f"snackbar('下载完成,请访问 /下载 文件夹查看')")
    return True

class Api():
    def download(self,strat_time:str,end_time:str):
        Download_Threads.append(Thread(target=single_download,args=(strat_time,end_time)))
        Download_Threads[-1].start()

    def parse(self,args):
        global Parse
        args = json.loads(args)
        info = Get_Request_Body
        info.url= args["url"]
        Parse = core.Parse(info)
        cmd = str(base64.b64encode(str(Parse["Play_Html"]+"\n"+Parse["Web_Title"]).encode('utf-8')),'utf-8')
        window.evaluate_js(f"get_parsed('{cmd}')")
        #把解析好的扔回去 因为包含单双引号,先base64一下


api = Api()
window = webview.create_window('Asdb media range downloader', './client.html',js_api=api,width=960)
webview.start()