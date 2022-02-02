from . import BiliBili as BiliBili
from . import Naifen as Naifen
from . import YouTube as YouTube


def Parse(url):
    if "bilibili.com" in url:
        return BiliBili.BiliBili(url)
    elif "asoul-rec.com" in url:
        return Naifen.Naifen(url)
    elif "youtube.com" or "youtu.be" in url:
        return YouTube.YouTube(url)
    else:
        return None

def Save_BiliBili_Cookie(Cookie:str):
    return BiliBili.Save_BiliBili_Cookie(Cookie)

def Get_BiliBili_Cookie():
    return BiliBili.Get_BiliBili_Cookie()