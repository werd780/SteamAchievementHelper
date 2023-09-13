import datetime
import os

FILENAME = 'C:\\ProgramData\\AchievementHelper\\log_file.txt'

def writeToLog(msg):
    with open(FILENAME,'a') as f:
        f.write(f"{datetime.datetime.now()}: {msg}\n")

def checkLogFile():
    try:
        if os.path.getsize(FILENAME) > 1048576:
            with open(FILENAME,'w') as f:
                f.write(f"Cleared and restarted log at: {datetime.datetime.now()}\n")
    except:
        writeToLog("Failed to clear and create new log file, must be manually deleted to reduce space as needed\n")