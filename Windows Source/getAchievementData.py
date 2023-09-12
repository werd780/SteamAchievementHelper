import requests
import controls
import time

def playerAchievementData(userID: str,appID: str):
    steamPath = "ISteamUserStats/GetPlayerAchievements/v0001"
    url = f"{controls.steamAPIURL}{steamPath}/"
    extraFields = {"key":controls.getAPI_Key(), "steamid":userID, "appid":appID, "l":"english"}

    try:
        response = requests.get(url,params=extraFields)
        if(response.status_code == 200):
            jdata = response.json()

            totalAchieveCount = 0
            unlockedAchieveCount = 0

            if jdata["playerstats"]["success"] == "false":
                return [True, totalAchieveCount,unlockedAchieveCount,[]]

            for achievement in jdata["playerstats"]['achievements']:
                totalAchieveCount = totalAchieveCount + 1 
                if achievement['achieved'] == 1:
                    unlockedAchieveCount = unlockedAchieveCount + 1

            #return [BOOL, Count of Achieves Total, Count of achieves Unlocked, List [Achievement Details]
            return [True, totalAchieveCount,unlockedAchieveCount,jdata["playerstats"]['achievements']]

        else:
            return [False,0,0,[]]
    except:
        time.sleep(5)
        playerAchievementData(userID, appID)