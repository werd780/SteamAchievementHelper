import tkinter
import tkinter.messagebox
import tkinter.ttk
import customtkinter
import os
import getUserData
import getOwnedGameData
import getAchievementData
import GUISettings
import controls
import testAPI
import logFile
import csv
import ctypes
import time
from tkinter import filedialog
from howlongtobeatpy import HowLongToBeat
from CTkTable import *
from PIL import Image


customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue (standard)"

PROFILE_PIC_WIDTH = 100
PROFILE_PIC_HEIGHT = 100
PROFILE_PIC_PATH = ""
MASTERGAMEDICTIONARY = []
SORT_ORDER_MAIN = "Ascending"
SORT_ORDER_ACH = "Ascending"
RESET_FLAG = False


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        createProgramFolder()
        logFile.checkLogFile()
        
        global PROFILE_PIC_PATH
        PROFILE_PIC_PATH = "C:\\ProgramData\\AchievementHelper\\profile_pic.jpg"

        #settings list [window width, window height, appearance mode, UI Scaling, Steam ID, API Key]
        settings = GUISettings.getGUISettings()

        # configure window
        self.title("Steam Achievement Tracker")
        self.geometry(f"{settings[0]}x{settings[1]}")
        self.update()

        # configure grid layout (2x4)
        self.grid_columnconfigure((0), weight=0)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_rowconfigure((3,4), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Import Player ID to Begin -->", font=customtkinter.CTkFont(weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.checkbox_frame = customtkinter.CTkFrame(master=self.sidebar_frame)
        self.checkbox_frame.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.checkbox_label = customtkinter.CTkLabel(self.checkbox_frame, text="Include Games:", font=customtkinter.CTkFont(weight="bold"))
        self.checkbox_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.checkbox_not_started = customtkinter.CTkCheckBox(master=self.checkbox_frame, text = "Not Started", command = self.checkbox_not_started_event)
        self.checkbox_not_started.grid(row=1, column=0, pady=(10, 0), padx=10, sticky="w")
        self.checkbox_completed = customtkinter.CTkCheckBox(master=self.checkbox_frame, text = "Completed", command = self.checkbox_completed_event)
        self.checkbox_completed.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.achievement_filter_label = customtkinter.CTkLabel(self.sidebar_frame, text="Show Achievements:", anchor="w")
        self.achievement_filter_label.grid(row=3, column=0, padx=10, pady=(10, 0))
        self.achievement_filter_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["All","Locked","Unlocked"],
                                                               command=self.change_achievement_filter_event)
        self.achievement_filter_optionmenu.grid(row=4, column=0, padx=10, pady=(10, 0))

        self.export_table = customtkinter.CTkButton(self.sidebar_frame, border_width=2, height=50, text= "Export Table", command=self.export_table_button_event)
        self.export_table.grid(row=5, column=0, padx=10, pady=(30,0), sticky="nsew")

        self.export_achievements = customtkinter.CTkButton(self.sidebar_frame, border_width=2, height=50, text= "Export Achievements", command=self.export_achievements_button_event)
        self.export_achievements.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

        self.reset_settings = customtkinter.CTkButton(self.sidebar_frame, border_width=2, height=50, text= "Reset Settings (Upon Next Open)", command=self.reset_settings)
        self.reset_settings.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=10, column=0, padx=20, pady=(10, 0))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "100%", "120%", "140%","160%","180%","200%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=12, column=0, padx=20, pady=(10, 20))

        # create api entry and buttons
        self.frame_API = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame_API.grid(row=0, column=1, padx=(10,10), pady=(10,10), sticky="nsew")
        self.frame_API.grid_columnconfigure(0, weight=1)

        self.entry_API = customtkinter.CTkEntry(self.frame_API, placeholder_text="Enter your Steam API")
        self.entry_API.grid(row=0, column=0, padx=(10, 0), pady=(10,10), sticky="nsew")

        self.api_button_1 = customtkinter.CTkButton(master=self.frame_API, border_width=2, text= "Test & Submit", command=self.api_button_1_event)
        self.api_button_1.grid(row=0, column=1, padx=(10, 10), pady=(10,10), sticky="nsew")

        self.api_button_2 = customtkinter.CTkButton(master=self.frame_API, border_width=2, text= "How-To", command=self.api_button_2_event)
        self.api_button_2.grid(row=0, column=2, padx=(10, 10), pady=(10,10), sticky="nsew")

        # create main entry and button
        self.entry_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.entry_frame.grid(row=1, column=1, padx=(10,10), pady=(10,10), sticky="nsew")
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Steam ID (Steam -> Settings -> Account Details -> Near the top)")
        self.entry.grid(row=0, column=0, padx=(10, 0), pady=(10,10), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.entry_frame, border_width=2, text= "Submit", command=self.submit_button_event)
        self.main_button_1.grid(row=0, column=1, padx=(10, 10), pady=(10,10), sticky="nsew")

        # create admin data
        self.topbar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.topbar_frame.grid(row=2, column=1, padx=(10,10), sticky="nsew")
        self.topbar_frame.grid_columnconfigure((0,2,4,6,8), weight=1)

        self.profile_picture = customtkinter.CTkImage(light_image=Image.open(os.path.join(PROFILE_PIC_PATH)),size=(PROFILE_PIC_WIDTH,PROFILE_PIC_HEIGHT))
        self.profile_picture_label = customtkinter.CTkLabel(master=self.topbar_frame,image=self.profile_picture, text="")
        self.profile_picture_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.profile_name = customtkinter.CTkLabel(self.topbar_frame, text="Unknown Player Name", font=customtkinter.CTkFont(weight="bold"))
        self.profile_name.grid(row=0, column=2, padx=10, pady=(10, 10))

        self.number_games = customtkinter.CTkLabel(self.topbar_frame, text="# Games: Unknown", font=customtkinter.CTkFont(weight="bold"))
        self.number_games.grid(row=0, column=4, padx=10, pady=(10, 10))

        self.completed_games = customtkinter.CTkLabel(self.topbar_frame, text="# Completed: Unknown", font=customtkinter.CTkFont(weight="bold"))
        self.completed_games.grid(row=0, column=6, padx=10, pady=(10, 10))

        self.unstarted_games = customtkinter.CTkLabel(self.topbar_frame, text="# Unstarted: Unknown", font=customtkinter.CTkFont(weight="bold"))
        self.unstarted_games.grid(row=0, column=8, padx=10, pady=(10, 10))

        # create main table
        self.main_table_frame = customtkinter.CTkScrollableFrame(self, label_text="")
        self.main_table_frame.grid(row=3, column=1, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.main_table_frame.grid_columnconfigure(0, weight=1)
        
        main_value = [["Game ID","Name","Hrs Played","Total Achs","Achs Earned","HLTB Main","HLTB +Extras","HLTB All"]]
        self.main_table = CTkTable(master=self.main_table_frame,column=8,row=1,values=main_value,command=self.main_table_select)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=10)

        # create achieve bottom        
        self.achieve_table_frame = customtkinter.CTkScrollableFrame(self, label_text="Game Name")
        self.achieve_table_frame.grid(row=4, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.achieve_table_frame.grid_columnconfigure(0, weight=1)
        
        right_value = [["API Name","Name","Description","Achieved"]]
        self.achieve_table = CTkTable(master=self.achieve_table_frame,column=4,row=1,values=right_value,command=self.achieve_table_select)
        self.achieve_table.pack(expand=True, fill="both", padx=10, pady=10)

        # set default values
        customtkinter.set_appearance_mode(settings[2])
        self.appearance_mode_optionmenu.set(settings[2])

        self.scaling_optionmenu.set(settings[3])
        self.change_scaling_event(settings[3])

        if settings[4] != "Steam ID (Steam -> Settings -> Account Details -> Near the top)":
            self.entry.insert(0,settings[4])

        if controls.getAPI_Key() != "Enter your Steam API":
            self.entry_API.insert(0,controls.getAPI_Key())

        self.checkbox_not_started.select()
        self.checkbox_not_started.configure(state="disabled")
        self.checkbox_completed.select()
        self.checkbox_completed.configure(state="disabled")
        self.achievement_filter_optionmenu.set("All")
        self.achievement_filter_optionmenu.configure(state="disabled")
        self.export_table.configure(state="disabled")
        self.export_achievements.configure(state="disabled")
        self.entry.configure(state="disabled")
        self.main_button_1.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_achievement_filter_event(self, new_filter: str):
        self.update_achievement_table(game_name=self.achieve_table_frame._label_text,filter=new_filter)

    def submit_button_event(self):
        global MASTERGAMEDICTIONARY

        userID = self.entry.get()
        returnValues = getUserData.apiUserData(userID)
        if returnValues[0] == False:
            self.update_profile_name("ID NOT FOUND")
            return
        
        self.update_profile_picture(returnValues[1])
        self.update_profile_name(returnValues[2])

        gameReturnValues = getOwnedGameData.ownedGameData(userID,0)
        if gameReturnValues[0] == False:
            self.update_profile_name("ERROR PULLING GAMES")
            return

        self.update_number_games(gameReturnValues[1])

        MASTERGAMEDICTIONARY = gameReturnValues[2]

        #Create popup
        self.popup = tkinter.Toplevel()
        tkinter.Label(self.popup, text="Game Database Syncing").grid(row=0,column=0,sticky="w")
        self.gameNamePopup = tkinter.Label(self.popup, text="Name of Game: ")
        self.gameNamePopup.grid(row=1,column=0,sticky="w")
        self.countPopup = tkinter.Label(self.popup, text=f"0/{len(MASTERGAMEDICTIONARY)}")
        self.countPopup.grid(row=2,column=0,sticky="w")
        self.popup.pack_slaves()

        unplayedCount = 0
        completedCount = 0
        indexCounter = 0
        valuesToAdd = [["Game ID","Name","Hrs Played","Total Achs","Achs Earned","HLTB Main","HLTB +Extras","HLTB All"]]

        for game in MASTERGAMEDICTIONARY:
            #Update popup text
            self.gameNamePopup.config(text=f"Name of Game: {game['name']}")
            self.countPopup.config(text=f"{indexCounter+1}/{len(MASTERGAMEDICTIONARY)}")
            self.popup.update()

            #change playtime_forever to hours instead of minutes
            MASTERGAMEDICTIONARY[indexCounter]["playtime_forever"] = round(MASTERGAMEDICTIONARY[indexCounter]["playtime_forever"] / 60, 2)

            #returns [BOOL, Count of Achieves Total, Count of achieves Unlocked, List [Achievement Details]]
            achievementReturnValues = getAchievementData.playerAchievementData(userID, str(game['appid']), 0)

            #Adding achievement data to Game dictionary
            MASTERGAMEDICTIONARY[indexCounter]["total_achieves"] = achievementReturnValues[1]
            MASTERGAMEDICTIONARY[indexCounter]["unlocked_achieves"] = achievementReturnValues[2]
            MASTERGAMEDICTIONARY[indexCounter]["achievements"] = achievementReturnValues[3]
            
            #Getting counts for Top Bar
            if MASTERGAMEDICTIONARY[indexCounter]["playtime_forever"] == 0:
                unplayedCount = unplayedCount + 1
            if MASTERGAMEDICTIONARY[indexCounter]["unlocked_achieves"] == MASTERGAMEDICTIONARY[indexCounter]["total_achieves"]:
                completedCount = completedCount + 1

            #Getting HLTB data
            results = []
            try:
                results = HowLongToBeat().search(game["name"])
            except Exception as e:
                self.countPopup.config(text=f"Error: {e}")
                self.popup.update()
                logFile.writeToLog(f"Error in getting How Long to Beat data for {game['name']}: {e}")
                time.sleep(2)

            if results is not None and len(results) > 0:
                best_element = max(results, key=lambda element: element.similarity)
                MASTERGAMEDICTIONARY[indexCounter]["main_story"] = best_element.main_story
                MASTERGAMEDICTIONARY[indexCounter]["extras"] = best_element.main_extra
                MASTERGAMEDICTIONARY[indexCounter]["completionist"] = best_element.completionist

            else:
                MASTERGAMEDICTIONARY[indexCounter]["main_story"] = 0.0
                MASTERGAMEDICTIONARY[indexCounter]["extras"] = 0.0
                MASTERGAMEDICTIONARY[indexCounter]["completionist"] = 0.0            

            #Adding values to main table
            valuesToAdd.append([game['appid'],
                                game['name'], game['playtime_forever'],
                                game['total_achieves'], game['unlocked_achieves'],
                                MASTERGAMEDICTIONARY[indexCounter]["main_story"],
                                MASTERGAMEDICTIONARY[indexCounter]["extras"],
                                MASTERGAMEDICTIONARY[indexCounter]["completionist"]] )

            indexCounter = indexCounter + 1
        
        self.main_table.configure(rows=indexCounter+1)
        self.main_table.update_values(valuesToAdd)

        #Tear down popup
        self.popup.destroy()

        #Update top bar stats
        self.update_unstarted_games(str(unplayedCount))
        self.update_completed_games(str(completedCount))

        #Enable checkbox filters and export button
        self.checkbox_completed.configure(state="normal")
        self.checkbox_not_started.configure(state="normal")
        self.export_table.configure(state="normal")

    def export_table_button_event(self):
        self.export(table="Main")

    def export_achievements_button_event(self):
        self.export(table="Achievements")

    def checkbox_not_started_event(self):
        self.main_table_update()

    def checkbox_completed_event(self):
        self.main_table_update()

    def update_profile_picture(self, new_image_path: str):
        self.profile_picture.configure(light_image=Image.open(os.path.join(new_image_path)),size=(PROFILE_PIC_WIDTH,PROFILE_PIC_HEIGHT))
        self.profile_picture_label.configure(image=self.profile_picture)

    def update_profile_name(self, new_profile_name: str):
        self.profile_name.configure(text=new_profile_name)

    def update_number_games(self, new_number_games: str):
        self.number_games.configure(text=f"# Games: {new_number_games}")

    def update_completed_games(self, new_completed_games: str):
        self.completed_games.configure(text=f"# Completed: {new_completed_games}")

    def update_unstarted_games(self, new_unstarted_games: str):
        self.unstarted_games.configure(text=f"# Unstarted: {new_unstarted_games}")

    def main_table_update(self):
        #Create popup
        self.popup = tkinter.Toplevel()
        tkinter.Label(self.popup, text="Building Table").grid(row=0,column=0,sticky="w")
        self.gameNamePopup = tkinter.Label(self.popup, text="Name of Game: ")
        self.gameNamePopup.grid(row=1,column=0,sticky="w")
        self.countPopup = tkinter.Label(self.popup, text=f"0/{len(MASTERGAMEDICTIONARY)}")
        self.countPopup.grid(row=2,column=0,sticky="w")
        self.popup.pack_slaves()

        self.clear_table()

        #Generate Actions (00: Both removed, 01: Hide Not Started 10: Hide Completed, 11: Both)
        includeActions = [1,1]
        if self.checkbox_not_started.get() == 0:
            includeActions[0] = 0

        if self.checkbox_completed.get() == 0:
            includeActions[1] = 0

        indexCountDictionary = 0
        indexCountTable = 0
        valuesToAdd = [["Game ID","Name","Hrs Played","Total Achs","Achs Earned","HLTB Main","HLTB +Extras","HLTB All"]]

        for game in MASTERGAMEDICTIONARY:
            #Update Popup
            self.gameNamePopup.config(text=f"Name of Game: {game['name']}")
            self.countPopup.config(text=f"{indexCountDictionary+1}/{len(MASTERGAMEDICTIONARY)}")
            self.popup.update()

            if(includeActions[0] == 0 and includeActions[1] == 0):
                if game['playtime_forever'] != 0 and game['total_achieves'] != game['unlocked_achieves']:
                    valuesToAdd.append([game['appid'],
                                        game['name'], game['playtime_forever'],
                                        game['total_achieves'], game['unlocked_achieves'],
                                        game["main_story"], game["extras"], game["completionist"]])
                    indexCountTable = indexCountTable + 1

            elif (includeActions[0] == 0 and includeActions[1] == 1):
                if game['playtime_forever'] != 0:
                    valuesToAdd.append([game['appid'],
                                        game['name'], game['playtime_forever'],
                                        game['total_achieves'], game['unlocked_achieves'],
                                        game["main_story"], game["extras"], game["completionist"]])
                    indexCountTable = indexCountTable + 1

            elif (includeActions[0] == 1 and includeActions[1] == 0):
                if game['total_achieves'] != game['unlocked_achieves']:
                    valuesToAdd.append([game['appid'],
                                        game['name'], game['playtime_forever'],
                                        game['total_achieves'], game['unlocked_achieves'],
                                        game["main_story"], game["extras"], game["completionist"]])
                    indexCountTable = indexCountTable + 1

            else:
                valuesToAdd.append([game['appid'],
                                        game['name'], game['playtime_forever'],
                                        game['total_achieves'], game['unlocked_achieves'],
                                        game["main_story"], game["extras"], game["completionist"]])
                indexCountTable = indexCountTable + 1
        
            indexCountDictionary = indexCountDictionary + 1

        self.main_table.configure(rows=indexCountTable+1)
        self.main_table.update_values(valuesToAdd)

        self.popup.destroy()

    def achieve_table_select(self, cell):
        if cell["row"] == 0:
            self.sortTable(col=cell["column"], table="Ach")

    def main_table_select(self, cell):
        if cell["row"] == 0:
            self.sortTable(col=cell["column"], table="Main")
        else:
            self.achievement_filter_optionmenu.set("All")
            self.achieve_table_frame.configure(label_text=self.main_table.get(cell["row"], 1))
            self.update_achievement_table(game_name=self.achieve_table_frame._label_text, filter= "All")

    def sortTable(self, col: int, table: str):
        global SORT_ORDER_MAIN
        global SORT_ORDER_ACH

        if table == "Main":
            if(SORT_ORDER_MAIN == "Descending"):
                sortBool = True
                SORT_ORDER_MAIN = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_MAIN = "Descending"

            tableValues = self.main_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])

            self.main_table.update_values(tableValues)

        else:
            if(SORT_ORDER_ACH == "Descending"):
                sortBool = True
                SORT_ORDER_ACH = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ACH = "Descending"
                
            tableValues = self.achieve_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])

            self.achieve_table.update_values(tableValues)


    def update_achievement_table(self, game_name: str, filter: str):
        valuesToAdd = [["API Name","Name","Description","Achieved"]]
        for game in MASTERGAMEDICTIONARY:
            if game["name"] == game_name:
                achievements_raw = game["achievements"]

        for achievement in achievements_raw:
            if(filter == "Locked" and achievement['achieved'] == 0):
                valuesToAdd.append([achievement['apiname'],
                                    achievement['name'],
                                    achievement['description'],
                                    achievement['achieved']])
            elif(filter == "Unlocked" and achievement['achieved'] == 1):
                valuesToAdd.append([achievement['apiname'],
                                    achievement['name'],
                                    achievement['description'],
                                    achievement['achieved']])
            elif(filter == "All"):
                valuesToAdd.append([achievement['apiname'],
                                    achievement['name'],
                                    achievement['description'],
                                    achievement['achieved']])
        
        self.achieve_table.configure(rows=len(valuesToAdd))
        self.achieve_table.update_values(valuesToAdd)

        self.achievement_filter_optionmenu.configure(state="normal")
        self.export_achievements.configure(state="normal")
    
    def clear_table(self):
        main_value = []
        self.main_table.configure(column=8,row=1,values=main_value)

    def export(self, table: str):
        try:
            saveLocation = self.getSaveFolder()

            if table == "Main":
                valuesToAdd = self.main_table.get()
            else:
                valuesToAdd = self.achieve_table.get()

            with open(saveLocation, "w", newline='') as csv_file:
                writer=csv.writer(csv_file)
                writer.writerows(valuesToAdd)
        except Exception as e:
            logFile.writeToLog(f"Error in export on table: {table}: {e}")
    
    def getSaveFolder(self):
        defaultFileName = self.achieve_table_frame._label_text + ".csv"
        return(filedialog.asksaveasfilename(initialdir="/",
                                            title="Save As",
                                            initialfile=defaultFileName,
                                            filetypes = [("csv file(*.csv)","*.csv")], 
                                            defaultextension = [("csv file(*.csv)","*.csv")]))
    
    def reset_settings(self):
        global RESET_FLAG
        RESET_FLAG = True

    def api_button_1_event(self):
        works = testAPI.testAPI(self.entry_API.get())
        if works == True:
            self.entry.configure(state="normal")
            self.main_button_1.configure(state="normal")
            controls.setAPI_Key(self.entry_API.get())

        else:
            self.entry.configure(state="disabled")
            self.entry_API.delete(0,'end')
            self.entry_API.configure(placeholder_text="Invalid API. Please Try Again")

    def api_button_2_event(self):
        self.popup = tkinter.Toplevel()
        tkinter.Label(self.popup, text="How to get a Steam API",font=("Arial",16)).grid(row=0,column=0,sticky="nsew")
        self.api_description = tkinter.Label(self.popup, text="Visit this link (type 'localhost' for domain if you don't have one): ", font=("Arial",16))
        self.api_description.grid(row=1,column=0,sticky="nsew")
        self.api_link = tkinter.Label(self.popup, text="https://steamcommunity.com/dev/apikey",font=("Arial",16))
        self.api_link.grid(row=2,column=0,sticky="nsew")
        self.popup.pack_slaves()

def createProgramFolder():
    directoryCheck = "C:\\ProgramData\\AchievementHelper"
    if not os.path.isdir(directoryCheck):
       os.mkdir(directoryCheck)
    if not os.path.isfile(directoryCheck + "\\API_Key.pk"):
        open(directoryCheck + "\\API_Key.pk","w").close()
        controls.setAPI_Key("Enter your Steam API")
    if not os.path.isfile(directoryCheck + "\\GUI_Settings.pk"):
        open(directoryCheck + "\\GUI_Settings.pk","w").close()
        GUISettings.revertGUISettings()
    if not os.path.isfile(directoryCheck + "\\log_file.txt"):
        open(directoryCheck + "\\log_file.txt","w").close()
    img = Image.new('RGB', (64,64))
    img.save(directoryCheck + "\\profile_pic.jpg")
    
def on_closing():
    if RESET_FLAG == True:
        GUISettings.revertGUISettings()
        controls.setAPI_Key("Enter your Steam API")

    else:
        if(app.entry.get() == ""):
            entryField = "Steam ID (Steam -> Settings -> Account Details -> Near the top)"
        else:
            entryField = app.entry.get()

        if(app.entry_API.get() == ""):
            apiEntryField = "Enter your Steam API"
        else:
            apiEntryField = app.entry_API.get()

        #settings list [window width, window height, appearance mode, UI Scaling, Steam ID]
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        app_width = int(app.winfo_width() / scale_factor)
        app_height = int(app.winfo_height() / scale_factor)
        GUISettings.setGUISettings([app_width, app_height,
                                app.appearance_mode_optionmenu.get(),
                                app.scaling_optionmenu.get(),
                                entryField])
        controls.setAPI_Key(apiEntryField)
    app.destroy()

if __name__ == "__main__":
    app = GUI()
    app.protocol("WM_DELETE_WINDOW",on_closing)
    app.mainloop()


