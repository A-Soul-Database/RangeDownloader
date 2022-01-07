from urllib.parse import quote, urlparse, unquote
import Extract
Extracts = [
    "www.bilibili.com","ali.asoul-rec.com","nf.asoul-rec.com" #It should obey the RFC 1808 rule.
]
class Get_Request_Body():
    url:str
    start:str
    end:str
    save_path:str=""

def Parse(args:Get_Request_Body):
    def to_second(a:str):
        if a.count(":") == 1:
            return int(a.split(":")[0])*60 + int(a.split(":")[1])
        elif a.count(":") == 3:
            return int(a.split(":")[0])*3600 + int(a.split(":")[1])*60 + int(a.split(":")[2])
        else:
            return int(a)
    url = args.url

    start = to_second(args.start.replace('：',":"))
    end = to_second(args.end.replace('：',":"))
    
    if urlparse(url).hostname in Extracts:
        Parser = Extract.Extract(url)
    else:
        Parser = {
            "args":"",
            "url":url,
            "name":url.split("/")[-1].split("?")[0].replace(" ","")
        }


    Parser["url"] = unquote(Parser["url"])
    Parser["name"] = unquote(Parser["name"])
    cmd = f'ffmpeg {Parser["args"]} -ss {start} -i "{Parser["url"]}"  -to {end-start} -c copy -y "{args.save_path}/{Parser["name"]}"' if start>0 else f'ffmpeg {Parser["args"]} -i "{Parser["url"]}" -to {end} -c copy -y "{args.save_path}/{Parser["name"]}"'
    #判定开始时间是否为0 否则B站会影响
    Parser["cmd"] = cmd
    return Parser