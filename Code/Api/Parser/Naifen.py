from urllib.parse import quote, unquote

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
    url = url.replace("http://","").replace("https://","")
    
    url = unquote(unquote(url))
    title = url.split('?')[0].split('/')[-1].replace(" ","")
    url ="https://"+ quote(url.split("?")[0]) + "?raw"

    name = url.split("/")[-1].split("?")[0].replace(" ","")

    A.Download_Url = url
    A.Play_Html=f"<video class='mdui-video-fluid' src='{url}' controls></video>"
    A.Web_Title = title
    A.Save_Name = name
    
    return A