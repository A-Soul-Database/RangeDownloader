# -*- coding: UTF-8 -*-
VERSION = 1.0
import zipfile
import requests
import webview
import base64
import subprocess
import json
import core
from contextlib import closing
import shutil
from threading import Thread

with subprocess.Popen("whoami",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as f:
    me = f.stdout.read().decode('utf-8').replace("\r\n","").split("\\")[1]
Download_path = "C:/Users/"+me+"/Downloads"

Parse = {}
Download_Threads = []
source = {
    "client": "https://livedb.asoulfan.com/rangeDownload/client.html",
    "ffmpeg_download": "https://livedb.asoulfan.com/rangeDownload/ffmpeg_download.html",
    "ffmpeg_assets":"https://ghproxy.com/https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n4.4-latest-win64-lgpl-4.4.zip",
    "version_check": "https://raw.githubusercontent.com//P-PPPP/RangeDownloader/main/version.json",
}

class Get_Request_Body:
    url:str

def single_download(strat_time:str,end_time:str):
    def to_second(a:str):
        if a.count(":") == 1:
            return int(a.split(":")[0])*60 + int(a.split(":")[1])
        elif a.count(":") == 2:
            return int(a.split(":")[0])*3600 + int(a.split(":")[1])*60 + int(a.split(":")[2])
        else:
            return int(a)
    start = to_second(strat_time.replace("：",":"))
    end = to_second(end_time.replace("：",":"))
    if end<start:
        return window.evaluate_js(f"alert('错误:结束时间不能小于开始时间')")
    
    if Parse["Download_Tool"] == "youtube-dl":
        pass
        '''
        options = {
            "external-downloader": "ffmpeg",
            "external-downloader-args": f"-ss {start} -to {end}",
            "f": "best",
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=dc7I-i7sPrg'])

        return window.evaluate_js(f"alert('下载完成')")
        '''
    else:
        cmd = f'ffmpeg {Parse["args"]} -ss {start} -i "{Parse["download_url"]}"  -to {end-start} -c copy -y "{Download_path}/{Parse["Save_Name"]}"' if start > 0 else f'ffmpeg {Parse["args"]} -i "{Parse["download_url"]}" -to {end} -c copy -y "{Download_path}/{Parse["Save_Name"]}"  2>&1'
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,universal_newlines=True)
    while p.poll() is None:
        Logger(p.stdout.readline())
        progress = to_second(p.stdout.readline().split("time=")[1].split(".")[0])/(end-start)*100 if "time=" in p.stdout.readline() else 0
        window.evaluate_js(f"progress('{str(progress)}')")
    window.evaluate_js(f"progress('{str(100)}')")

    window.evaluate_js(f"snackbar('下载完成 {Download_path}/{Parse['Save_Name']} ')")
    return True

def Logger(info):
    window.evaluate_js(f"logger('{str(base64.b64encode(str(info).encode('utf-8')),'utf-8')}')")

class Api():
    def download(self,strat_time:str,end_time:str):
        Download_Threads.append(Thread(target=single_download,args=(strat_time,end_time)).start())

    def parse(self,args):
        global Parse
        args = json.loads(args)
        info = Get_Request_Body
        info.url= args["url"]
        Parse = core.Parse(info)
        cmd = str(base64.b64encode(str(Parse["Play_Html"]+"\n"+Parse["Web_Title"]).encode('utf-8')),'utf-8')
        window.evaluate_js(f"get_parsed('{cmd}')")
        #把解析好的扔回去 因为包含单双引号,先base64一下

    def download_ffmpeg(self):
        window.evaluate_js(f"snackbar('正在下载ffmpeg')")
        with closing(requests.session().get(source["ffmpeg_assets"],stream=True)) as response:
            chunk_size = 1024*1024
            contentSize = int(response.headers['content-length'])
            dateCount = 0
            with open("ffmpeg.zip", "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    dateCount += len(data)
                    progress = round(dateCount / contentSize, 2) * 100
                    window.evaluate_js(f"update_progress('{progress}')")
        window.evaluate_js(f"snackbar('下载完成,正在解压')")
        for i in zipfile.ZipFile("./ffmpeg.zip").namelist():
            if i.split("/")[-1] == "ffmpeg.exe":
                zipfile.ZipFile("./ffmpeg.zip").extract(i,"./")
                shutil.move(i,"./ffmpeg.exe")
                break
        window.load_url(source["client"])

################################################### Components #####################################################
def detect_new_version():
    try:
        with closing(requests.session().get(source["version_check"])) as response:
            version =  json.loads(response.text)["version"]
    except:
        version = VERSION
    if version > VERSION:
        window.evaluate_js(f"snackbar(版本可以更新了!')")

def detect_ffmpeg():
    """
        没有ffmpeg的话就要下载
    """
    try:
        subprocess.Popen('ffmpeg -h',shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return True
    except:
        return False
####################################################### #####################################################

def set_html(window):
    if ffmpeg:
        window.load_url(source["client"])
    else:
        pass
        window.load_url(source["ffmpeg_download"])
if __name__ == "__main__":
    ffmpeg = detect_ffmpeg()
    api = Api()
    window = webview.create_window('Asdb media range downloader',html='Loading',js_api=api,width=960)
    webview.start(set_html,window)