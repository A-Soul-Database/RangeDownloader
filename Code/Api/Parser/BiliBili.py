# _*_ coding:utf-8 _*_
import requests
import urllib.parse

class Parser():
    Args:str
    Download_Url:str
    Play_Html:str
    Web_Title:str
    Save_Name:str
    Video_Format:str
    Download_Tool:str

A = Parser()
A.Download_Tool = "ffmpeg"
A.Video_Format = "mp4"
A.Args =  ' -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -headers "Referer:https://www.bilibili.com/" '
def BiliBili(url:str="")->dict:
    bv,p = purify_URL(url)
    A.Download_Url = get_Info(bv,p)["data"]["durl"][0]["url"]
    A.Play_Html = f"<video class='mdui-video-fluid' src='{A.Download_Url}' controls></video>"
    A.Save_Name = bv if p=="1" else bv+"-"+p
    return A

def get_Info(bv,p)->dict:
    #通过bv号和p号获取视频信息
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Referer":"https://www.bilibili.com/",
    }
    Bili_Video_Info_Json = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()
    cid = Bili_Video_Info_Json["data"]["pages"][int(p)-1]["cid"]
    A.Web_Title = Bili_Video_Info_Json["data"]["title"]
    return requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={cid}&otype=json&&platform=html5&high_quality=1",headers=headers).json()

def purify_URL(url:str)->str:
    #提取bv号和p号
    bv = url.split("/")[-1].split("?")[0]
    try:
        p = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))["p"]
    except:
        p = "1"
    return (bv,p)