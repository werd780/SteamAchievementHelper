import requests
import json
import controls

def getHelp():
    steamPath = "ISteamWebAPIUtil/GetSupportedAPIList/v0001/"
    url = f"{controls.steamAPIURL}{steamPath}"
    extraFields = {"key":controls.getAPI_Key()}
    response = requests.get(url,params=extraFields)
    if(response.status_code == 200):
        with open("steamAPIDocs.txt","w") as f:
            json.dump(response.json(),f,indent=4)
    else:
        print(f"{response.status_code} failed")