# FFmpeg_Core
# Author: @PPPPP, For all video creators :)
import os
import subprocess
from threading import Thread
import time
import psutil
import sys


def Multi_Thread_Seeking(Start_Time:int,End_Time:int,Url:str,Save_Name:str,Seek_type:str="Input",Threads:int=4,Args:str=""):
    #   http://trac.ffmpeg.org/wiki/Seeking \n
    #   In the documentation, the following is the format of the seek command:
    #       Input\Output

    Uniq_ID = str(hash(Url)) # Generate a id ,To Prevent File Overwrite
    Progress.update({Uniq_ID:{}})
    Progress[Uniq_ID]["Save_Name"] = Save_Name
    def test():
        Working_Threads = [] #Reset Working_Threads
        Each_Duration = (End_Time - Start_Time) / Threads
        Commands = []
        start_time = Start_Time
        for i in range(Threads):
            end_time = start_time + Each_Duration
            if Seek_type.lower()=="input":
                cmd =f'ffmpeg  {Args} -i "{Url}" -to {end_time} -avoid_negative_ts 1 -c copy "{i}_{Uniq_ID}.mp4" -y 2>&1' if start_time==0 else f'ffmpeg  {Args} -ss {start_time} -i "{Url}" -to {end_time-start_time} -avoid_negative_ts 1 -c copy "{i}_{Uniq_ID}.mp4" -y 2>&1'
            elif Seek_type.lower() == "output":
                cmd = f'ffmpeg  {Args} -i "{Url}" -to {end_time} -avoid_negative_ts 1 -c copy "{i}_{Uniq_ID}.mp4" -y 2>&1' if start_time==0 else f'ffmpeg  {Args} -ss {start_time} -i "{Url}" -to {end_time} -avoid_negative_ts 1 -c copy "{i}_{Uniq_ID}.mp4" -y 2>&1'
            Commands.append(cmd)
            start_time = end_time
        # Run Commands
        for i in range(Threads):
            Progress[Uniq_ID].update({i:{}}) 
            #Initialize Dictionary
            Progress[Uniq_ID][i]["Running"] = 1
            Working_Threads.append(Thread(target=evaule_command,args=(Commands[i],i,Uniq_ID,Each_Duration)))
        Progress[Uniq_ID]["Threads"] = Threads
        # Wait for all threads to finish
        for i in range(Threads):
            Working_Threads[i].start()
        for i in range(Threads):
            Working_Threads[i].join() 
        # Merge Files
        if Threads>1:
            #One thread dont need this
            if Progress[Uniq_ID][0]["Running"]!=4:
                open(f"{Uniq_ID}.txt","w",encoding="utf-8").write("\n".join([f"file '{i}_{Uniq_ID}.mp4'" for i in range(Threads)]))
                subprocess.call(f'ffmpeg -f concat -i {Uniq_ID}.txt -c copy "{Save_Name}.mp4"',shell=True)
                os.remove(f"{Uniq_ID}.txt")
            # Delete Files
            for i in range(Threads):
                pass
                os.remove(f"{i}_{Uniq_ID}.mp4")
        elif Threads ==1 :
            os.rename(f"0_{Uniq_ID}.mp4",f"{Save_Name}.mp4")
        return True

    Thread(target=test).start()
    return Uniq_ID


def evaule_command(Command:str,Instance_id:int,Uniq_ID:str,Duration:int):
    # Instance_id: Thread_Id
    Progress[Uniq_ID][Instance_id]["progress"]=0
    p = subprocess.Popen(Command,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,bufsize=1,universal_newlines=True,encoding="utf-8")
    while p.poll() is None:
        time.sleep(0.1)
        ###### Update Progress ######
        out = p.stdout.readline()
        p.stdout.flush()
        Progress[Uniq_ID][Instance_id]["out"] = out
        if out.count("time="):
            Progress[Uniq_ID][Instance_id]["progress"] = to_seconds_time(out.split("time=")[1].split(".")[0])/Duration
        ####### thread operation#######
        if Progress[Uniq_ID][Instance_id]["Running"]==4:
            Kill_FFmpeg(p.pid)
            return False
        if Progress[Uniq_ID][Instance_id]["Running"]==2:
            #restart thread when thread is running 
            Kill_FFmpeg(p.pid)
            Progress[Uniq_ID][Instance_id]["progress"] = 0
            Progress[Uniq_ID][Instance_id]["Running"]=1
            return evaule_command(Command,Instance_id,Uniq_ID,Duration)
        if Progress[Uniq_ID][Instance_id]["Running"]==0:
            #   Maybe you wanna suspend the thread for a while...
            #       0. Stop The Thread
            #       1. restart the thread
            #       2. resume the thread
            #       3. Thread has finished
            #       4. Thread has been killed
            psutil.Process(p.pid).suspend()
            while Progress[Uniq_ID][Instance_id]["Running"]==0:
                time.sleep(1)
                if Progress[Uniq_ID][Instance_id]["Running"]==1:
                    #resume thread
                    psutil.Process(p.pid).resume()
                if Progress[Uniq_ID][Instance_id]["Running"]==2:
                    #restart thread
                    p.kill()
                    Progress[Uniq_ID][Instance_id]["Running"]=1
                    return evaule_command(Command,Instance_id,Uniq_ID,Duration)
    #Maybe the thread is finished...without any risk...
    Progress[Uniq_ID][Instance_id]["progress"] = 1
    Progress[Uniq_ID][Instance_id]["Running"]=3

Progress = {}
#
#{
#  "3486": {  -> Uniq_ID
#    "0": {
#      "Running": 1, -> 0:Suspended 1:Running, 2:Restart(Temp,For siginal only), 3:Finished, 4:Terminate a task
#      "out": "", -> Output of ffmpeg
#      "progress": 1 -> Progress of the ffmpeg (e.g. : 0.03)
#    },
#    ...
#}

def Get_Progress():
    return Progress

def Kill_FFmpeg(pid):
    # Exit Thread
    # It is because we started a new thread using 'shel=True' this will open up a individual ffmpeg process
    # Cause p.kill() and p.termate() cannot stop immediately
    # for more reason and solution please :
    # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
    #
    if sys.platform == "win32":
        subprocess.call(f'TASKKILL /F /PID {pid} /T')
    else:
        import signal,os
        os.killpg(os.getpgid(pid), signal.SIGTERM)

def to_seconds_time(a:str)->int:
    if a.count(":")==1:
        return int(a.split(":")[0])*60+int(a.split(":")[1])
    if a.count(":")==2:
        return int(a.split(":")[0])*3600+int(a.split(":")[1])*60+int(a.split(":")[2])
    return int(a)

def thread_operation(Uniq_ID:str,Instance_id:int,Running:int):
    Progress[Uniq_ID][Instance_id]["Running"]=Running
    return True
