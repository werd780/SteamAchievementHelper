import pickle
from resourcePathFix import resource_path

FILENAME = 'C:\\ProgramData\\AchievementHelper\\resources\\GUI_Settings.pk'

def getGUISettings():
    with open(FILENAME,'rb') as fi:
        settings = pickle.load(fi)
    return (settings)

def setGUISettings(settings: list):
    with open(FILENAME,'wb') as fi:
        pickle.dump(settings, fi)

def revertGUISettings():
    #settings list [window width, window height, appearance mode, UI Scaling, Steam ID]
    settings_list=[1700, 720, "Dark", "100%", "Steam ID (Steam -> Settings -> Account Details -> Near the top)"]

    with open(FILENAME,'wb') as fi:
        pickle.dump(settings_list, fi)