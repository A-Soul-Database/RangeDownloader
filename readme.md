# RangeDownloader 视频片段下载器

RangeDownloader 通过组合 `ffmpeg` 命令让用户可以**只下载某个片段**而不是下载全部文件.

<details>
<summary> 为什么需要<code>RangeDownloader</code> </summary>
场景分析: 当我们在进行视频创作时,也许<b>只需要其中一小段素材</b>.  </br>
一般来说,创作者可能会选择两种方法: </br>
- 直接下载该文件,之后在本地裁剪</br>
<PRE>&#9</PRE>- 问题: 耗费大量时间</br>
- 录屏 </br>
<PRE>&#9</PRE>- 问题: 画质严重损失 </br>
- Range: seconds</br>
<PRE>&#9</PRE>- 问题: 需要服务器支持,且<b>大多数服务器不支持</b></br>

</details>

## 已经测试支持的网站
- BiliBili (默认清晰度为1080P)
- `asoul-rec.com`

## 贡献
`Extract/`文件夹已经包含了两个网站的实现方式,按照`Extract/AddWeb.md`进行规范开发即可.

## todo
- m3u8 Segment
- You-Tube Support
- Update Check
- Srt Cut

## License & Libs
[ffmpeg]()  
[pywebview]()  