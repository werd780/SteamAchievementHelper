import requests
import controls
import time
import logFile

def playerAchievementData(userID: str,appID: str, attempt: int):
    if (attempt == 4):
        logFile.writeToLog(f"Reached max attempts getting achievement data for userID: {userID} and gameID: {appID}")
        return ([False,0,0,[]])
    
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

            try:
                for achievement in jdata["playerstats"]['achievements']:
                    totalAchieveCount = totalAchieveCount + 1 
                    if achievement['achieved'] == 1:
                        unlockedAchieveCount = unlockedAchieveCount + 1

                #return [BOOL, Count of Achieves Total, Count of achieves Unlocked, List [Achievement Details]
                return [True, totalAchieveCount,unlockedAchieveCount,jdata["playerstats"]['achievements']]
            
            except Exception as e:
                logFile.writeToLog(f"INFO: This game {appID} has an odd return from Steam: {e}")
                return [False,0,0,[]]

        else:
            logFile.writeToLog(f"Returned HTTP response for getting achievement data: {response.status_code} for userID: {userID} and gameID: {appID}")
            return [False,0,0,[]]
    
    except Exception as e:
        logFile.writeToLog(f"Error in owned get achievement data: {e} on attempt {attempt} for userID: {userID} and gameID: {appID}")
        time.sleep(attempt + 1)
        return(playerAchievementData(userID, appID, attempt + 1))