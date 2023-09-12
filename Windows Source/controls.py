import pickle
from resourcePathFix import resource_path

steamAPIURL =  "http://api.steampowered.com/"
formatType = "format=json"

FILENAME = 'C:\\ProgramData\\AchievementHelper\\resources\\API_Key.pk'

def getAPI_Key():
    with open(FILENAME,'rb') as fi:
        apiKey = pickle.load(fi)
    return (apiKey)

def setAPI_Key(apiKey: str):
    with open(FILENAME,'wb') as fi:
        pickle.dump(apiKey, fi)
