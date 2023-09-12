import requests
import controls

def testAPI(apiKey: str):
    steamPath = "ISteamWebAPIUtil/GetSupportedAPIList/v0001/"
    url = f"{controls.steamAPIURL}{steamPath}"
    extraFields = {"key":apiKey}
    response = requests.get(url,params=extraFields)
    if(response.status_code == 200):
        return True
    else:
        return False