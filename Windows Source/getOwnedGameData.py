import requests
import controls
import time
import logFile


def ownedGameData(userID: str, attempt: int):
    if attempt == 4:
        logFile.writeToLog(f"Reached max attempts getting owned game data for userID {userID}")
        return [False,"",[]]
    steamPath = "IPlayerService/GetOwnedGames/v0001/"
    url = f"{controls.steamAPIURL}{steamPath}/"
    extraFields = {"key":controls.getAPI_Key(), "steamid":userID,
                   "include_appinfo":"true","include_played_free_games":"true"}
    try:
        response = requests.get(url,params=extraFields)
        if(response.status_code == 200):
            jdata = response.json()

            return [True, str(jdata['response']['game_count']),jdata['response']['games']]

        else:
            logFile.writeToLog(f"Returned HTTP response for get owned game data: {response.status_code} userID: {userID}")
            return [False,"",[]]
        
    except Exception as e:
        logFile.writeToLog(f"Error in owned Game Data: {e} on attempt {attempt} userID: {userID}")
        time.sleep(attempt + 1)
        return(ownedGameData(userID,attempt + 1))