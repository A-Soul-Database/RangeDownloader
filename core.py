from urllib.parse import urlparse, unquote
import Extract
Extracts = [
    "www.bilibili.com","ali.asoul-rec.com","nf.asoul-rec.com" #It should obey the RFC 1808 rule.
]
class Get_Request_Body():
    url:str

def Parse(args:Get_Request_Body):
    def to_second(a:str):
        if a.count(":") == 1:
            return int(a.split(":")[0])*60 + int(a.split(":")[1])
        elif a.count(":") == 3:
            return int(a.split(":")[0])*3600 + int(a.split(":")[1])*60 + int(a.split(":")[2])
        else:
            return int(a)
    
    url = args.url

    
    if urlparse(url).hostname in Extracts:
        Parser = Extract.Extract(url)
    else:
        Parser = {
            "args":"",
            "download_url":url,
            "Play_Html":f"<video src='{url}' controls></video>",
            "Web_Title":url.split("/")[-1].replace("?","").replace(" ",""),
            "Save_Name":url.split("/")[-1].replace("?","").replace(" ","")
        }


    Parser["download_url"] = unquote(Parser["download_url"])
    Parser["Play_Html"] = unquote(Parser["Play_Html"])
    Parser["Save_Name"] = unquote(Parser["Save_Name"])
    #cmd = f'ffmpeg {Parser["args"]} -ss {start} -i "{Parser["download_url"]}"  -to {end-start} -c copy -y "{args.save_path}/{Parser["Save_Name"]}"' if start>0 else f'ffmpeg {Parser["args"]} -i "{Parser["download_url"]}" -to {end} -c copy -y "{args.save_path}/{Parser["Save_Name"]}"'
    #判定开始时间是否为0 否则B站会影响
    #Parser["cmd"] = cmd
    return Parser