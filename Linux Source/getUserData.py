import requests
import controls
import shutil
import time

def apiUserData(userID: str):
    #quicker check if ID exists
    if(len(userID) != 17):
        return [False,"",""]

    steamPath = "ISteamUser/GetPlayerSummaries/v0002/"
    url = f"{controls.steamAPIURL}{steamPath}/"
    extraFields = {"key":controls.getAPI_Key(), "steamids":{userID}}
    try:
        response = requests.get(url,params=extraFields)
        if(response.status_code == 200):
            jdata = response.json()

            #Check if User Exists
            try:
                personalData = jdata["response"]["players"][0]
            
            except IndexError:
                return [False,"",""]
            
            #download picture
            url = personalData["avatarmedium"]
            response=requests.get(url,stream=True)
            with open("resources/profile_pic.jpg","wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            return [True,"resources/profile_pic.jpg",personalData["personaname"]]

        else:
            return [False,"",""]
    except:
        time.sleep(5)
        apiUserData(userID)
    