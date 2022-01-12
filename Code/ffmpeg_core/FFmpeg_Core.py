import os
import subprocess
from threading import Thread
import random
import time
import psutil


def Multi_Thread_Seeking(Start_Time:int,End_Time:int,Url:str,Seek_type:str="Input",Threads:int=4,args:str=""):
    """
        http://trac.ffmpeg.org/wiki/Seeking \n
        In the documentation, the following is the format of the seek command:
            Input\Output
    """
    # Make Commands
    
    Uniq_ID = str(random.randint(0,9999)) # To Prevent Overwrite
    Progress.update({Uniq_ID:{}})
    def test():
        Working_Threads = [] #Reset Working_Threads
        Each_Duration = (End_Time - Start_Time) / Threads
        Commands = []
        start_time = Start_Time
        for i in range(Threads):
            end_time = start_time + Each_Duration
            if Seek_type.lower()=="input":
                cmd =f'ffmpeg {args} -i "{Url}" -to {end_time} -c copy output{i}_{Uniq_ID}.mp4 -y 2>&1' if start_time==0 else f'ffmpeg {args} -ss {start_time} -i "{Url}" -to {end_time-start_time} -c copy output{i}_{Uniq_ID}.mp4 -y 2>&1'
            elif Seek_type.lower() == "output":
                cmd = f'ffmpeg {args} -i "{Url}" -to {end_time} -c copy output{i}_{Uniq_ID}.mp4 -y 2>&1' if start_time==0 else f'ffmpeg {args} -ss {start_time} -i "{Url}" -to {end_time} -c copy output{i}_{Uniq_ID}.mp4 -y 2>&1'
            Commands.append(cmd)
            start_time = end_time
        # Run Commands
        print(Commands)
        for i in range(Threads):
            Progress[Uniq_ID].update({i:{}}) 
            #Initialize Dictionary
            Progress[Uniq_ID][i]["Running"] = 1
            Working_Threads.append(Thread(target=evaule_command,args=(Commands[i],i,Uniq_ID,Each_Duration)))
        # Wait for all threads to finish
        for i in range(Threads):
            Working_Threads[i].start()
        for i in range(Threads):
            Working_Threads[i].join() 
        # Merge Files
        open(f"{Uniq_ID}.txt","w",encoding="utf-8").write("\n".join(["file 'output"+str(i)+f"_{Uniq_ID}.mp4'" for i in range(Threads)]))
        subprocess.call(f'ffmpeg -f concat -i {Uniq_ID}.txt -c copy {Uniq_ID}.mp4',shell=True)
        # Delete Files
        for i in range(Threads):
            os.remove(f"output{i}_{Uniq_ID}.mp4")
        os.remove(f"{Uniq_ID}.txt")
        return True

    Thread(target=test).start()
    return Uniq_ID


def evaule_command(Command:str,Instance_id:int,Uniq_ID:str,Duration:int):
    # Instance_id: Thread_Id
    p = subprocess.Popen(Command,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,universal_newlines=True,encoding="utf-8")
    while p.poll() is None:
        ###### Update Progress ######
        out = p.stdout.readline()
        Progress[Uniq_ID][Instance_id]["out"] = out
        if out.count("time="):
            Progress[Uniq_ID][Instance_id]["progress"] = to_seconds_time(out.split("time=")[1].split(".")[0])/Duration
        ####### thread operation#######
        if Progress[Uniq_ID][Instance_id]["Running"]==2:
            #restart thread when thread is running 
            p.kill()
            Progress[Uniq_ID][Instance_id]["Running"]=1
            return evaule_command(Command,Instance_id,Uniq_ID,Duration)
        if Progress[Uniq_ID][Instance_id]["Running"]==0:
            """
                Maybe you wanna suspend the thread for a while...
                If a thread is suspended, we provide two ways of operation
                    1. restart the thread
                    2. resume the thread
                But don't provide a way to stop the thread,Cause it will loop forever...
            """
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
        
        # oops,Maybe the thread is finished...
        Progress[Uniq_ID][Instance_id]["Running"]=3

Progress = {}
"""
{
  "3486": {  -> Uniq_ID
    "0": {
      "Running": 1, -> 0:Suspended 1:Running, 2:Restart(Temp,For siginal only), 3:Finished
      "out": "", -> Output of ffmpeg
      "progress": 1 -> Progress of the ffmpeg (e.g. : 0.03)
    },
    ...
}
"""
def Get_Progress(Uniq_ID:str):
    return Progress


def to_seconds_time(a:str)->int:
    if a.count(":")==1:
        return int(a.split(":")[0])*60+int(a.split(":")[1])
    if a.count(":")==2:
        return int(a.split(":")[0])*3600+int(a.split(":")[1])*60+int(a.split(":")[2])
    return int(a)

def thread_operation(Uniq_ID:str,Instance_id:int,Running:int):
    Progress[Uniq_ID][Instance_id]["Running"]=Running
    return True
