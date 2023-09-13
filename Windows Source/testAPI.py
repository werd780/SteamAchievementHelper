import requests
import controls
import logFile

def testAPI(apiKey: str):
    steamPath = "ISteamWebAPIUtil/GetSupportedAPIList/v0001/"
    url = f"{controls.steamAPIURL}{steamPath}"
    extraFields = {"key":apiKey}
    response = requests.get(url,params=extraFields)
    if(response.status_code == 200):
        return True
    else:
        logFile.writeToLog(f"Returned HTTP response for API validation: {response.status_code}")
        return False