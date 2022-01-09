import requests

def Naifen(url)->dict:
    title = requests.get(url).text.split('<a href="?preview">')[1].split("</a>")[0]
    proxied = True if "proxied" in url else False
    url = url.split("?")[0]+"?raw" if proxied else url.split("?")[0]+"?raw"
    name = url.split("/")[-1].split("?")[0].replace(" ","")
    return {
    "args":"",
    "download_url":url,
    "Play_Html":f"<video class='mdui-video-fluid' src='{url}' controls></video>",
    "Web_Title":title,
    "Save_Name":name,
    "Download_Tool":"ffmpeg"
    }

'''
def Get_Video_Info(url):
    command = f'ffmpeg -i "{Naifen(url)["url"]}" '
    #[1].split(",")[0]
    print(command)
    return os.popen(command).read().split("Duration:")
'''