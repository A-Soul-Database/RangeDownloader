from urllib.parse import quote, unquote
import requests

header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0 AsdbRangeDownloaderv1'
class Parser():
    Url:str
    Args:str = f' -user_agent "User-Agent: {header}" '
    Download_Url:str
    Play_Html:str
    Web_Title:str
    Save_Name:str
    Video_Format:str
    Download_Tool:str

A = Parser()
A.Video_Format = "mp4"
A.Download_Tool = "ffmpeg"
A.Args = ""
def Naifen(url)->dict:
    """
        奶粉罐录播站的解析
            整体分为Ali和nf,两个子域名
            Ali:不存在代理
            Nf: Cloudflare的代理为流传输,不支持
            有中文存在需要url编解码
    """
    try:
        url = url.replace("http://","").replace("https://","").split("?")[0]
    except:
        url = url.replace("http://","").replace("https://","")
        
    url = unquote(unquote(url))
    r = requests.get("https://"+url+"?preview",headers={'User-Agent':header}).text
    title = url.split('?')[0].split('/')[-1].replace(" ","")
    url ="https://"+ quote(url.split("?")[0]) + "?raw"

    name = url.split("/")[-1].split("?")[0].replace(" ","")

    try:
        A.Download_Url = r.split('data-url="')[1].split('"')[0].replace("#38;","")
    except:
        A.Download_Url = r.split('<a class="download-button" href="')[1].split('"')[0]


    A.Play_Html=f"<video class='mdui-video-fluid' src='{quote(url)}' controls></video>"
    A.Web_Title = title
    A.Save_Name = title
    return A

def DDindex(url)->dict:
    try:
        url = url.replace("https://","").replace("http://","").replace('&download=1','')
    except:
        url = url.replace("https://","").replace("http://","")
    
    url = unquote(unquote(url))
    r = requests.get(f"https://{url}",headers={"User-Agent":header})
    r.encoding = 'utf-8'
    pas = "一百八一杯"
    path = url.split("ddindexs.com")[1]
    info = requests.post("https://alist.ddindexs.com/api/fs/get",data={"password":pas,"path":path},headers={"User-Agent":header}).json()
    title = info["data"]["name"]
    A.Save_Name , A.Web_Title = title, title
    Real_Url = info["data"]["raw_url"]
    A.Play_Html=f"<video class='mdui-video-fluid' src='{Real_Url}' controls></video>"
    A.Download_Url = Real_Url
    return A
