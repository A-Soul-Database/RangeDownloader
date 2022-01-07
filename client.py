# -*- coding: UTF-8 -*-
import webview
import core
import subprocess
import json
import os

me = os.popen("whoami").read().replace("\n","").split("\\")[1]
Download_path = "C:/Users/"+me+"/Downloads"

class Get_Request_Body:
    url:str
    start:str
    end:str
    save_path:str=""

class Api():
    def excute(self,args):
        args = json.loads(args)
        info = Get_Request_Body
        info.url,info.start,info.end,info.save_path = args["url"],args["start"],args["end"],Download_path
        cmd = core.Parse(info)["cmd"]
        window.evaluate_js("update_status('已解析,开始下载')")
        subprocess.Popen(cmd,shell=True).wait()
        window.evaluate_js("update_status('下载完成')")


api = Api()
window = webview.create_window('Mp4 range downloader', './index.html',js_api=api)
webview.start()