import requests
import controls
import shutil
import logFile

def apiUserData(userID: str):
    #quicker check if ID exists
    if(len(userID) != 17):
        logFile.writeToLog(f"User ID inputted was too short or long: {userID} length {len(userID)}")
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
                logFile.writeToLog(f"User ID does not exist {userID}")
                return [False,"",""]
            
            #download picture
            url = personalData["avatarmedium"]
            response=requests.get(url,stream=True)
            with open("C:\\ProgramData\\AchievementHelper\\profile_pic.jpg","wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            return [True,"C:\\ProgramData\\AchievementHelper\\profile_pic.jpg",personalData["personaname"]]

        else:
            logFile.writeToLog(f"Returned HTTP response for User Data request: {response.status_code} userID: {userID}")
            return [False,"",""]
        
    except Exception as e:
        logFile.writeToLog(f"Error in owned Game Data: {e} userID: {userID}")
    