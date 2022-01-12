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
