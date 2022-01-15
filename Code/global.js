var A_Cao = false;

function dialog(operation,html){
    /*
        show/hide a dialog
            operation int 
                1: open
                0: close
    */
   document.getElementById('global_dialog').innerHTML = html;
    operation ===1 ? global_dialog.open() : global_dialog.close()
}

function snackbar(message){
    mdui.snackbar({
        message: message,
        position: 'left-bottom',
    });
}
function Install_FFmpeg(){
    fetch(`${Config.ffmpeg_api}/Install_FFmpeg`)
    let progress = setInterval(function(){
        fetch(`${Config.ffmpeg_api}/Install_Progress`)
        .then(responese=>{
            responese.json().then(function(data){
                if(data){
                    console.log(data)
                    document.getElementById('progress_bar').style.width = data.Download_Progress + "%";
                    if (data.Install_Stage===2){
                        clearInterval(progress);
                        document.getElementById("ffmpeg-page").style.display = "none";
                        document.getElementById("main-page").style.display = "block";
                        snackbar("FFmpeg 安装完成");
                    }
                }
            });
        })
    },1000)
}
async function Advanced_Fetch(url){
    ms=1000;
    let controller = new AbortController();
    let signal = controller.signal;
    let timeout_Promise = (timeout)=>{
        return new Promise((resolve,reject)=>{
            setTimeout(()=>{
                resolve(new Response(false,{status:408}));
                controller.abort();
            },timeout)
        })
    }
    let request_Promise = (target) => {
        return fetch(target,{
            signal:signal
        });
    };
    const response = await Promise.race([timeout_Promise(ms),request_Promise(url)])
    return response.ok;
}

async function init(){
    snackbar("尝试链接本地服务...");
    var status = await heartbeat();
    if(!status){
        snackbar("本地服务连接失败，请检查服务是否正常启动或是否正确配置");
        Setting();
        return false;
    }
    
    //Check ffmpeg Install Status
    fetch (Config.ffmpeg_api+"/Detect").then(function(response){
        //Get Bool Json
        response.json().then(function(data){
            if(data===false){
                snackbar("FFmpeg 没有安装");
                document.getElementById("main-page").style.display = "none";
                document.getElementById("ffmpeg-page").style.display = "block";
                Install_FFmpeg();
            }
        });
    });
    snackbar("服务正常");
    //read config from cookie
    if(getCookie("Config")){Config = JSON.parse(getCookie("Config"))}
    get_bilibili_cookie();
}

async function heartbeat(){
    const ffmpeg = await Advanced_Fetch(Config.ffmpeg_api+"/ping");
    const parse = await Advanced_Fetch(Config.Parse_api+"/ping");
    return (ffmpeg && parse);
}

function combine_download_item(Uniq_Id){
    This_Item = Download_Progress[Uniq_Id];
    Thread_Num = This_Item.Threads
    title = This_Item.Save_Name;
    var Progress_Html="";
    var Activity_bar = "";
    var Status,progress;
    var Finished = 0;
    for(var n=0;n<Thread_Num;n++){
        progress = This_Item[n].progress*100;
        running = This_Item[n].Running;
        width =100/Thread_Num;
        switch(running){
            case 0:// hang
                Status = "mdui-progress-determinate mdui-color-grey";
                Activity_bar= `<i class="mdui-list-item-icon mdui-icon material-icons mdui-ripple" mdui-tooltip="{content: '继续'}" onclick="Download_Actions(${Uniq_Id},1,${Thread_Num})">play_arrow</i><i class="mdui-list-item-icon mdui-icon material-icons mdui-ripple" mdui-tooltip="{content: '删除任务'}"  onclick="Download_Actions(${Uniq_Id},4,${Thread_Num})">clear</i>`;
                break;
            case 1:// Normally run
                Status = "mdui-progress-determinate mdui-color-blue";
                Activity_bar= `<i class="mdui-list-item-icon mdui-icon material-icons mdui-ripple" mdui-tooltip="{content: '暂停'}" onclick="Download_Actions(${Uniq_Id},0,${Thread_Num})">pause</i><i class="mdui-list-item-icon mdui-icon material-icons mdui-ripple" mdui-tooltip="{content: '删除任务'}" onclick="Download_Actions(${Uniq_Id},4,${Thread_Num})">clear</i>`;
                break;
            case 3:// Finished
                Finished+=1
                Status = "mdui-progress-determinate mdui-color-green";
                if (Finished === Thread_Num){
                    if(Finished_List.indexOf(Uniq_Id)===-1){snackbar(`${title} 下载完成`);Finished_List.push(Uniq_Id);}
                    Activity_bar= `<i class="mdui-list-item-icon mdui-icon material-icons mdui-ripple" mdui-tooltip="{content: '打开保存位置'}" onclick="open_folder()">folder</i>`;
                }
                break;
            case 4://Terminated
                Status = "mdui-progress-determinate mdui-color-red";
                Activity_bar="";
                break;
        }
        var Progress_Html_Temp = `<div class="mdui-progress" style="width: ${width}%;float: left;"><div class="${Status}" style="width: ${progress}%;"></div></div>`;
        Progress_Html+=Progress_Html_Temp;
    }
    var Download_Template = `
    <li class="mdui-list-item mdui-ripple">
        <div class="mdui-list-item-content">
        <div class="mdui-list-item-title">${title}</div>
        ${Progress_Html}
        </div>
        ${Activity_bar}
    </li>
    `
    return Download_Template;
}
function Download_Actions(Uniq_Id,Signal,Thread_Num){
    for(var n=0;n<Thread_Num;n++){
        fetch(`${Config.ffmpeg_api}/thread_operation?Uniq_ID=${Uniq_Id}&Running=${Signal}&Instance_id=${n}`)
    }
}
function open_folder(){
    fetch(`${Config.ffmpeg_api}/Open_Folder`)
}
function Setcookie (name, value){ 
    var expdate = new Date();
    expdate.setTime(expdate.getTime() + 1296000 * 1000);
    document.cookie = name+"="+value+";expires="+expdate.toGMTString()+";path=/";
}
function getCookie(c_name){
    if (document.cookie.length>0){
      c_start=document.cookie.indexOf(c_name + "=")
      if (c_start!=-1){ 
        c_start=c_start + c_name.length+1 
        c_end=document.cookie.indexOf(";",c_start)
        if (c_end==-1) c_end=document.cookie.length
        return decodeURI(document.cookie.substring(c_start,c_end))
        } 
      }
    return ""
}
function apply_parse(){
    dialog(1,'<div class="mdui-dialog-title" id="dialog_title">正在解析</div><div class="mdui-dialog-content"><div class="mdui-progress"><div class="mdui-progress-indeterminate"></div></div></div>');
    var url = encodeURI(document.getElementById("url").value);
    if(url.indexOf("bilibili")>0){snackbar("Tips:如果你是大会员,可以设置Cookie以获得4K视频支持捏")}
    fetch(`${Config.Parse_api}/Parse`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "url": url
        })
    }).then(function(response){
        response.json().then(function(data){
            get_parsed(data);
        });
    });
    
}

function get_parsed(info){
    Parse = info;
    document.getElementById("left-outer-player").innerHTML = info.Play_Html;
    document.getElementById('video_title').innerHTML = info.Web_Title;
    document.getElementById("step2-container").style.display = "block";
    dialog(0);
}
function to_second_time(time){
    time.replace(/：/g, ":");
    let a = time.split(":");
    switch(a.length-1){
        case 0:
            return parseInt(time);
        case 1:
            return parseInt(a[0])*60 + parseInt(a[1]);
        case 2:
            return parseInt(a[0])*3600 + parseInt(a[1])*60 + parseInt(a[2]);
    }
}
function apply_download(){
    console.log(Parse)
    start_time = to_second_time(document.getElementById("start-time").value);
    end_time = to_second_time(document.getElementById("end-time").value);
    fetch(`${Config.ffmpeg_api}/Seek`,{
        method : "POST",
        headers :{
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({
            "Url": Parse.Download_Url,
            "Start_Time": start_time,
            "End_Time": end_time,
            "Save_Name": `${Parse.Save_Name}_${start_time}_${end_time}`,
            "Threads":Config.Thread_Num,
            "Args":Parse.Args,
            "Seek_type":"Input"
        })
    })
    snackbar('已添加至下载队列中');
}

function get_video_player_current_time(){
    var this_time = document.getElementsByTagName("video")[0].currentTime;
    navigator.clipboard.writeText(parseInt(this_time))
    snackbar("已经复制到剪贴板")
}
function logger(info){
    document.getElementById("logs").innerHTML = info;
}
function progress(intt){
    document.getElementById("download_progress").style.width = intt+"%";
}
function save_setting_param(){
    if(!Config.Multi_Thread_Switch){
        Config.Thread_Num = 1; //如果关闭了多线程,则线程数设置为1
    }else{
        Config.Thread_Num = document.getElementById("Thread_Num").value;
    }
    Config.ffmpeg_api = document.getElementById("ffmpeg_api").value;
    Config.Parse_api = document.getElementById("Parse_api").value;
    Config.BiliBili_Cookie = document.getElementById("BiliBili_Cookie").value;
    Config.Multi_Thread_Switch = document.getElementById("Multi_Thread_Switch").checked;
    //Save to cookie
    document.cookie = Setcookie("Config",JSON.stringify(Config));
    save_bilibili_cookie(Config.BiliBili_Cookie);
    snackbar("已保存");
}

function save_bilibili_cookie(cookie){
    fetch(`${Config.Parse_api}/Save_BiliBili_Cookie?Cookie=${cookie}`)
}
function get_bilibili_cookie(){
    fetch(`${Config.Parse_api}/Get_BiliBili_Cookie`)
    .then(responese=>responese.json())
    .then(function(data){
        if(data!=""){
            Config.BiliBili_Cookie = data;
            document.getElementById("BiliBili_Cookie").value = data;
        }
    })
}

function Setting(){
    document.getElementById('ffmpeg_api').value = Config.ffmpeg_api;
    document.getElementById('Parse_api').value = Config.Parse_api;
    document.getElementById('Thread_Num').value = Config.Thread_Num;
    document.getElementById('BiliBili_Cookie').value = Config.BiliBili_Cookie;

    document.getElementById('Multi_Thread_Switch').checked = Config.Multi_Thread_Switch;
    Setting_Dialog.open();
}

function get_download_info(){
    var Download_List_Html = "";
    fetch(`${Config.ffmpeg_api}/Progress`).then(function(response){
        response.json().then(function(data){
            //遍历json对象
            Download_Progress = data;
            for(var i in data){
                Download_List_Html+=combine_download_item(i);
            }
            document.getElementById('Download-List-Content').innerHTML = Download_List_Html;
        })
    })
}

function Acao_Mode(){
    const acao = new mdui.Dialog("#A_cao_dialog");
    acao.open()
}