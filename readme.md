# RangeDownloader 视频片段下载器

RangeDownloader 通过组合 `ffmpeg` 命令让用户可以**只下载某个片段**而不是下载全部文件.

<details>
<summary> 为什么需要<code>RangeDownloader</code> </summary>
场景分析: 当我们在进行视频创作时,也许<b>只需要其中一小段素材</b>.  </br>
一般来说,创作者可能会选择两种方法: </br>
- 直接下载该文件,之后在本地裁剪</br>
    - 问题: 耗费大量时间</br>
- 录屏 </br>
    - 问题: 画质严重损失 </br>
- Range: seconds</br>
    - 问题: 需要服务器支持,且<b>大多数服务器不支持</b></br>

</details>

由于`Ffmpeg.wasm`限制跨域且有内存限制,故现在仅支持命令行输出

## Api
### `Get /api/v1/parse/{info:path}`
info templates:
```info
{
    "url":"https://www.bilibili.com/BV123",
    "start":"00:00",
    "end":"03:51"
}
```
return
```returns
{
  "args": " -user_agent \"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36\" -headers \"Referer:https://www.bilibili.com/\"",
  "url": "https://****.bilivideo.com/up.....",
  "name": "BV1Mr4y1S79q_1.mp4",
  "cmd": "ffmpeg  -user_agent \"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36\" -headers \"Referer:https://www.bilibili.com/\" -i 'https://****.bilivideo.com/up.....' -ss 00:00 -to 05:00 -c copy -y 'BV1Mr4y1S79q_1.mp4'"
}
```
*在执行时请注意把`\`去除*

## 已经测试支持的网站
- BiliBili (默认清晰度为1080P)
- `asoul-rec.com`

## 贡献
`Extract/`文件夹已经包含了两个网站的实现方式,按照`Extract/AddWeb.md`进行规范开发即可.
