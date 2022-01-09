from . import BiliBili as BiliBili
from . import Naifen as Naifen
from . import YouTube as YouTube
import os

def Extract(url):
    if "bilibili.com" in url:
        return BiliBili.BiliBili(url)
    elif "asoul-rec.com" in url:
        return Naifen.Naifen(url)
    elif "youtube.com" or "youtu.be" in url:
        return YouTube.YouTube(url)
    else:
        return None

def Get_Video_Info(url):
    if "bilibili.com" in url:
        return BiliBili.Get_Video_Info(url)
    elif "asoul-rec.com" in url:
        return Naifen.Get_Video_Info(url)
    else:
        return os.popen(f"ffmpeg -i '{url}'").read()