from . import BiliBili as BiliBili
from . import Naifen as Naifen


def Parse(url):
    if "bilibili.com" in url:
        return BiliBili.BiliBili(url)
    elif ("asoul-rec.com" in url) or ("knaifen.workers.dev" in url):
        return Naifen.Naifen(url)
    elif ("ddindexs.com" in url):
        return Naifen.DDindex(url)
    else:
        return None

def Save_BiliBili_Cookie(Cookie:str):
    return BiliBili.Save_BiliBili_Cookie(Cookie)

def Get_BiliBili_Cookie():
    return BiliBili.Get_BiliBili_Cookie()
