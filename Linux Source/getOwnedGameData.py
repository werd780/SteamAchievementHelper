import requests
import controls
import time


def ownedGameData(userID: str):
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
            return [False,"",[]]
    except:
        time.sleep(5)
        ownedGameData(userID)  