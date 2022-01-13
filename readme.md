# RangeDownloader 视频片段下载器

RangeDownloader 通过组合 `ffmpeg` 命令让用户可以**只下载某个片段**而不是下载全部文件.

<details>
<summary> 为什么需要<code>RangeDownloader</code> </summary>
场景分析: 当我们在进行视频创作时,也许<b>只需要其中一小段素材</b>.  </br>
一般来说,创作者可能会选择两种方法: </br>
方法1: 直接下载该文件,之后在本地裁剪</br>
问题: 耗费大量时间</br>
方法2: 录屏 </br>
问题: 画质严重损失 </br>
方法3: Range: seconds</br>
问题: 需要服务器支持,且<b>大多数服务器不支持</b></br>

</details>

## 已知问题
由于mp4 的 track问题,ffmpeg在分割前几秒有几率发生**花屏**现象导致素材不可用
解决方法
1. 调整设置中的 *多线程下载阈值* 大于你所需要下载的时间
2. 提前并推后2~3秒的时长

## 已经测试支持的网站
- BiliBili (账号所能达到的最高清晰度)
- `asoul-rec.com`

## 编译/源码使用


## 贡献
`Extract/`文件夹已经包含了两个网站的实现方式,按照`Extract/AddWeb.md`进行规范开发即可.

## todo
- m3u8 Segment
- You-Tube Support
- Update Check
- Srt Cut
- Local File

- BiliBili cookie bind
- setting interface
- use card item

## License & Libs
[GPL V3.0 License]()  
[ffmpeg]()  
[pywebview]()  
[mdui]()  