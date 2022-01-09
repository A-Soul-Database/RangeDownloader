import urllib.parse
def YouTube(url:str):
    return {
        "args":"",
        "download_url":"",
        "Play_Html":f'<iframe id="ytplayer" type="text/html" src="https://www.youtube.com/embed/{dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))["v"]}"frameborder="0"></iframe>',
        "Web_Title":"",
        "Save_Name":dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))["v"]+".mp4",
        "Download_Tool":"youtube-dl"
    }