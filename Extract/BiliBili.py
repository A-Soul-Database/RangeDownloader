# _*_ coding:utf-8 _*_
import os
import requests
import urllib.parse


def BiliBili(url:str="")->dict:
    bv,p = purify_URL(url)
    return {"args":' -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -headers "Referer:https://www.bilibili.com/" ',
        "download_url":get_Info(bv,p)["data"]["durl"][0]["url"],
        "Play_Html":f"<iframe src='http://player.bilibili.com/player.html?bvid={bv}&p={p}' scrolling='no' frameborder='no' width='100%'></iframe>",
        "Web_Title":"",
        "Save_Name":bv+".mp4" if p=="1" else bv+"-"+p+".mp4"
        }

def get_Info(bv,p)->dict:
    #通过bv号和p号获取视频信息
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Referer":"https://www.bilibili.com/",
    }
    Bili_Video_Info_Api = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    Bili_Video_Info_Json = requests.get(Bili_Video_Info_Api,headers=headers).json()
    cid = Bili_Video_Info_Json["data"]["pages"][int(p)-1]["cid"]
    qualities = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={cid}&otype=json",headers=headers).json()
    qn = qualities["data"]["support_formats"][0]["quality"]
    return requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={cid}&qn={qn}&otype=json",headers=headers).json()

def purify_URL(url:str)->str:
    #提取bv号和p号
    bv = url.split("/")[-1].split("?")[0]
    try:
        p = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))["p"]
    except:
        p = "1"
    return (bv,p)
    
'''
def Get_Video_Info(url:str):
    bv,p = Purify_URL(url)
    return Get_Info(bv,p)["data"]["timelength"]
'''

