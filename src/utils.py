from datetime import datetime
import os

def get_current_time() -> str:
    now = datetime.now()
    now = now.ctime()
    now = now.split(" ")
    time = now[4]
    time = time.split(":")
    time = time[0] + ":" + time[1]
    return time

def get_current_date():
    now = datetime.now()
    date = datetime.date(now)
    date = str(date)
    return date

def get_project_dir() -> str:
    cwd = os.getcwd()
    cwd = cwd.split("/")
    cwd = "/".join(cwd[:-1])
    if not "/ZoomJoiner" in cwd: # this is only needed from the IDE, when running the script th .sh is at the same level as the config file
        cwd = cwd + "/ZoomJoiner"
    return cwd
