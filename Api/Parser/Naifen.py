from urllib.parse import quote, unquote
import requests
class Parser():
    Url:str
    Args:str
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
    r = requests.get("https://"+url+"?preview",headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}).text
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