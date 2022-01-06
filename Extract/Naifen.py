def Naifen(url)->dict:
    proxied = True if "proxied" in url else False
    url = url.split("?")[0]+"?raw&proxied" if proxied else url.split("?")[0]+"?raw"
    name = url.split("/")[-1].split("?")[0].replace(" ","")
    return {"args":"","url":url,"name":name}

'''
def Get_Video_Info(url):
    command = f'ffmpeg -i "{Naifen(url)["url"]}" '
    #[1].split(",")[0]
    print(command)
    return os.popen(command).read().split("Duration:")
'''