from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import seaborn as sns

#import yagmail

import sqlite3

import tkinter as tk
from tkinter import font as tkfont

global usernameCorrect
usernameCorrect = False
global previousMileage
previousMileage = True

import datetime

class myDatabase():
    def __init__(self):
        self.db = sqlite3.connect("D:\\Users\\Prabhjot\\Desktop\\CarDatabase.db") ## connection to database is made
        self.c = self.db.cursor() ## "cursor" object is made
        self.createDatabase() ## calls the next method to create the database
        self.populateJobTable() ## method to record the jobs in the "job" table is called

    def createDatabase(self):
        try:
            self.db.execute("PRAGMA foreign_keys = ON")
            self.c.execute("""CREATE TABLE IF NOT EXISTS userData(
            userID INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT)
            """)

            self.c.execute("""CREATE TABLE IF NOT EXISTS mileage(
            mileageID INTEGER PRIMARY KEY,
            mileage INTEGER,
            date TEXT)
            """)

            self.c.execute("""CREATE TABLE IF NOT EXISTS job(
            jobID INTEGER PRIMARY KEY,
            jobName TEXT,
            predictedCost REAL,
            maxMileage INTEGER,   
            weatherCheck TEXT,
            priority INTEGER)
            """)

            self.c.execute("""CREATE TABLE IF NOT EXISTS maintenanceRecords(
            mRecordID INTEGER PRIMARY KEY,
            jobID INTEGER,
            mileageID INTEGER,
            userID INTEGER,
            FOREIGN KEY (userID) REFERENCES userData(userID),
            FOREIGN KEY (mileageID) REFERENCES mileage(mileageID),
            FOREIGN KEY (jobID) REFERENCES job(jobID))
            """)

            self.db.commit()
            
        except:
            print("Database failed to create")

    def populateJobTable(self):
        try:
            self.c.execute("SELECT jobID FROM job WHERE jobID = ?", (1,))
            checkExistingRecords = self.c.fetchone()
            checkExistingRecords = checkExistingRecords[0]
            if checkExistingRecords == 1:
                pass
        except:
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "None", 0.00, 0, "False", 11))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Refuel", 1.20, 1000, "False", 10))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Oil change", 31.38, 2000, "False", 5))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Brake pads replacement", 23.58, 3000, "False", 1))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Lambda/Oxygen Sensor replacement", 60.23, 4000, "False", 6))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Air conditioning repair", 89.49, 5000, "hot weather", 8))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Radiator replacement", 112.31, 6000, "hot weather", 2))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Battery replacement", 85.20, 7000, "False", 7))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Heating repair", 129.80, 8000, "cold weather", 9))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Fuel filter replacement", 19.98, 9000, "False", 4))
            self.c.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?)", (None, "Headlight replacement", 238.29, 10000, "False", 3)) 
            self.db.commit()
            
    def getRecentEntries(self, username1, nameOfObject, flag2):
        continue1 = True
        self.c.execute("SELECT userID FROM userData WHERE username = ?", (username1,))
        checkUserID = self.c.fetchone()
        checkUserID = int(checkUserID[0])
        try:
            self.c.execute("SELECT mRecordID FROM maintenanceRecords where userID = ? LIMIT 1", (checkUserID,))
            mRecordExist = self.c.fetchone()
            if mRecordExist[0] != "":
                pass
        except:
            if flag2 == True:
                nameOfObject.updateRecentEntryLabel("No recent record found! Make a maintenance record by navigating to the 'Mileage Page'")
            continue1 = False
            global previousMileage
            previousMileage = False

        if continue1 == True:
            self.c.execute("SELECT * FROM maintenanceRecords WHERE userID = ? ORDER BY mRecordID DESC LIMIT 1", (checkUserID,))
            rEntry = self.c.fetchone()
            
            rMileageID = int(rEntry[2])
            rJobID = int(rEntry[1])

            self.c.execute("SELECT mileage, date FROM mileage WHERE mileageID = ? ORDER BY mileageID DESC LIMIT 1", (rMileageID,))
            rMileages = self.c.fetchone()
            rMileages1 = str(rMileages[0])
            rDate1 = str(rMileages[1])
            
            self.c.execute("SELECT jobName, predictedCost FROM job WHERE jobID = ? ORDER BY jobID DESC LIMIT 1", (rJobID,))
            rJobs = self.c.fetchone()
            rJobN1 = str(rJobs[0])
            rPCost1 = str(rJobs[1])

            rFinalText = ("Mileage:" + rMileages1 + " " + "Date:" + rDate1 + " " + "Job:" + rJobN1 + " " + "Predicted cost:" + "£" + rPCost1)
            if flag2 == True:
                nameOfObject.updateRecentEntryLabel(rFinalText)
            if flag2 == False and continue1 == True:
                nameOfObject.sendEmail(rFinalText, False)

        if flag2 == False and continue1 == False:
            nameOfObject.sendEmail("no records", True)
        

    def mileageAndJobAdd(self, mileage1, job1, date1, username1):
        self.c.execute("INSERT INTO mileage VALUES (?, ?, ?)", (None, mileage1, date1))
        self.db.commit()
        self.c.execute("SELECT mileageID FROM mileage WHERE mileage = ? AND date = ?", (mileage1, date1,))
        mileage1ID = self.c.fetchone()
        mileage1ID = int(mileage1ID[0])

        self.c.execute("SELECT jobID FROM job WHERE jobName = ?", (job1,))
        job1ID = self.c.fetchone()
        job1ID = int(job1ID[0])

        self.c.execute("SELECT userID FROM userData WHERE username = ?", (username1,))
        user1ID = self.c.fetchone()
        user1ID = int(user1ID[0])       
        
        self.c.execute("INSERT INTO maintenanceRecords VALUES (?, ?, ?, ?)", (None, job1ID, mileage1ID, user1ID))
        self.db.commit()
        
    def authUser(self, authUsername, authPassword, nameOfObject):
        global usernameCorrect
        isEmpty = False

        if authUsername == "":
            nameOfObject.updateLabel("Empty username field. Please enter your username.")
            isEmpty = True
            
        if authPassword == "" and usernameCorrect == True:
            nameOfObject.updateLabel("Empty password field. Please enter your password")
            isEmpty = True
        
        if usernameCorrect == True and isEmpty == False:
            self.c.execute("SELECT password FROM userData WHERE username = ?", (authUsername,))
            checkUser = self.c.fetchone()
            if checkUser[0] == authPassword:
                nameOfObject.updateLabel("Login details are correct. Successful login.")
                nameOfObject.successLogin(authUsername)
            else:
                nameOfObject.updateLabel("Password is incorrect")

        if usernameCorrect == False and isEmpty == False:
            try:
                self.c.execute("SELECT username FROM userData WHERE username = ?", (authUsername,))
                checkUser = self.c.fetchone()
                if checkUser[0] == authUsername:
                    nameOfObject.updateLabel("Username is correct")
                    nameOfObject.changeEntryStates("disabled", "normal")
                    usernameCorrect = True
            except:    
                nameOfObject.updateLabel("Username is incorrect")
            
    def addUser(self, addUsername, addPassword, nameOfObject):
        userExist = False
        isEmpty = False

        if addUsername == "" and addPassword == "":
            nameOfObject.updateLabel2("Empty username and password fields. Please enter your username and password")
            isEmpty = True
        elif addUsername == "":
            nameOfObject.updateLabel2("Empty username field. Please enter your username.")
            isEmpty = True
        elif addPassword == "":
            nameOfObject.updateLabel2("Empty password field. Please enter your password.")
            isEmpty = True

        if isEmpty == False:
            try:
                self.c.execute("SELECT username FROM userData WHERE username = ?", (addUsername,))
                checkUser = self.c.fetchone()
                if addUsername == checkUser[0]:
                    userExist = True
            except:
                userExist = False
            
            if userExist == False and isEmpty == False:
                self.c.execute("INSERT INTO userData VALUES (?,?,?)", (None, addUsername, addPassword))
                self.db.commit()
                nameOfObject.updateLabel2("User registration successful.")
            else:
                nameOfObject.updateLabel2("Username already taken. Please enter a different one.")

    def updateMileageValue(self, objectName, username1):
        if previousMileage == True:
            self.c.execute("SELECT userID FROM userData WHERE username = ?", (username1,))
            userID1 = self.c.fetchone()
            userID1 = int(userID1[0])
            self.c.execute("SELECT mileageID FROM maintenanceRecords WHERE userID = ? ORDER BY mileageID DESC LIMIT 1", (userID1,))
            mileageID1 = self.c.fetchone()
            mileageID1 = int(mileageID1[0])
            self.c.execute("SELECT mileage, date FROM mileage WHERE mileageID = ? ORDER BY mileageID DESC LIMIT 1", (mileageID1,))
            rMileageDetails = self.c.fetchone()
            rMileage = int(rMileageDetails[0])
            rDate = rMileageDetails[1]
            objectName.savePreviousMileageAndDate(rMileage, rDate)

    def checkJobTips(self, objectName, username):
        rMList = []
        rJobsDict = {}
        rJobNamesList = []
        if previousMileage == True: ## checks how many unique job types the user has e.g. has at least one record for jobs with jobID's 3 and 7
            self.c.execute("SELECT userID FROM userData WHERE username = ?", (username,))
            userID1 = self.c.fetchone()  
            userID1 = int(userID1[0])
            uniqueJobNum = 0
            counter = 2
            for i in range(10):
                self.c.execute("SELECT jobID FROM maintenanceRecords WHERE userID = ? AND jobID = ?", (userID1, counter))
                checking1 = self.c.fetchone()
                if checking1 == None:
                    pass
                else:
                    uniqueJobNum = uniqueJobNum + 1
                    rMList.append(checking1[0])
                counter = counter + 1
                
            for i in range(uniqueJobNum): ## retrieves job data from database for the most recent record for each recorded job type
                secondM = False
                jobIDs2 = rMList[i]
                jobIDs2 = int(jobIDs2)
                self.c.execute("SELECT jobName, maxMileage, weatherCheck, priority FROM job WHERE jobID = ?", (jobIDs2,))
                rJobDetails = self.c.fetchone()
                rJobName = str(rJobDetails[0])
                rJobNamesList.append(rJobName)
                rMaxMileage = int(rJobDetails[1])
                rWeatherCheck = str(rJobDetails[2])
                rPriority = int(rJobDetails[3])
                self.c.execute("SELECT mileageID FROM maintenanceRecords WHERE userID = ? AND jobID = ? ORDER BY mileageID DESC LIMIT 2", (userID1, jobIDs2))
                rCheckMileagesID2 = self.c.fetchall()
                mileageID1 = "".join(map(str, (rCheckMileagesID2[0])))
                mileageID1 = int(mileageID1)

                try: ## checks if the user has more than one mileage recorded for each unique job type recorded. The second most recent mileage will be saved under "secondMileage" and set "secondMW to True
                    mileageID2 = "".join(map(str, (rCheckMileagesID2[1])))
                    mileageID2 = int(mileageID2)
                    self.c.execute("SELECT mileage FROM mileage WHERE mileageID = ? ORDER BY mileage DESC LIMIT 1", (mileageID2,))
                    secondMileage = self.c.fetchone()
                    secondMileage = int(secondMileage[0])
                    secondM = True
                except:
                    pass
                
                self.c.execute("SELECT mileage, date FROM mileage WHERE mileageID = ?", (mileageID1,)) ## gets the most recent mileage for each unique job type recorded.
                rMileageAndDate = self.c.fetchone()
                rDate = str(rMileageAndDate[1])
                rDate.split("/")
                rMonth = rDate.split("/")[1]
                if "0" in rMonth[0]:
                    rMonth = rMonth[1]
                rMileage = int(rMileageAndDate[0])

                ## rJobsDict is a dictionary that records all the required information for every job type recorded by the user
                if secondM == True: ## if there are 2 or more mileages for this unique job type then the difference between the two mileages will be recorded in the dictionary as well
                    rMileageDiff = rMileage - secondMileage
                    rJobsDict[rJobName] = rMileage, rMileageDiff, rMonth, rMaxMileage, rWeatherCheck, rPriority
                else: ## if not then the mileage will just be recorded twice to overcome any errors in the "tipSystem" method
                    rJobsDict[rJobName] = rMileage, rMileage, rMonth, rMaxMileage, rWeatherCheck, rPriority 
                    
            objectName.tipSystem(rJobsDict, rJobNamesList, uniqueJobNum) ## "tipSystem" method will be called in the "mainPage" class with the jobs dictionary, a list of the job names
            ## and the number of unique job types being passed into the method.

        else:
            objectName.noMileage() ## if the global variable "previousMileage" is False then this method will tell the user that they need to make a record

    def getGraphValues(self, nameOfObject, username): ## get data for a graph with dates on y axis and mileages on x axis
        yList = []
        xList = []
        mileageIDs = []
        self.c.execute("SELECT userID FROM userData WHERE username = ?", (username,))
        userID1 = self.c.fetchone()
        userID1 = int(userID1[0])
        self.c.execute("SELECT mileageID FROM maintenanceRecords WHERE userID = ? LIMIT 10", (userID1,))
        mileageIDsNA = self.c.fetchall()

        mileageIDs = [i[0] for i in mileageIDsNA]

        for i in range(len(mileageIDs)):
            oneMileageID = mileageIDs[i]
            oneMileageID = int(oneMileageID)
            self.c.execute("SELECT mileage, date FROM mileage WHERE mileageID = ?", (oneMileageID,))
            dataFromMileageTable = self.c.fetchone()
            mileage1 = int(dataFromMileageTable[0])
            date1 = dataFromMileageTable[1]
            xList.append(mileage1)
            yList.append(date1)

        global previousMileage
        if previousMileage == False:
            nameOfObject.insufficientMileage("There are no mileages recorded!")
        elif len(xList) == 1:
            nameOfObject.insufficientMileage("There are insufficient mileages recorded!")
        elif previousMileage == True:
            nameOfObject.updateGraphValues(xList, yList)
            
    def endDatabase(self):
        self.db.close()

newDb = myDatabase()
        

class mainWindow(tk.Tk):
    ## This class isn't a page itself. It is used to create the other pages.
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        
        self.titleFont1 = tkfont.Font(family = "Arial", size = 30, weight = "bold")
        self.buttonFont1 = tkfont.Font(family = "Arial", size = 15)
        self.labelFont1 = tkfont.Font(family = "Arial", size = 15)
        self.labelFont2 = tkfont.Font(family = "Arial", size = 10)
        self.labelFont3 = tkfont.Font(family = "Arial", size = 9, weight = "bold")
        self.labelFont4 = tkfont.Font(family = "Arial", size = 15, weight = "bold")
        container = tk.Frame(self) ## creating a frame called container
        container.pack(side = "top", fill = "both", expand = True) ## when window is expanded frames moves with it. 
        container.grid_rowconfigure(0, weight = 1) ## helps with the proper alignement of widgets
        container.grid_columnconfigure(0, weight = 1) ## helps with the proper alignement of widgets

        self.frames = {} ## empty dictionary is created

        self.menuBar = tk.Menu() 
        self.pagesMenu = tk.Menu()
        self.menuBar.add_cascade(label="Pages", menu=self.pagesMenu)

        self.changeMenuState("disabled")

        self.pagesMenu.add_command(label = "Main Page", command = lambda: self.showFrame("mainPage")) 
        self.pagesMenu.add_command(label = "Mileage Page", command = lambda: self.showFrame("mileagePage"))
        self.pagesMenu.add_command(label = "Results Page", command = lambda: self.showFrame("resultsPage"))
        self.pagesMenu.add_command(label = "Email Page", command = lambda: self.showFrame("emailPage"))
        self.pagesMenu.add_command(label = "Help Page", command = lambda: self.showFrame("helpPage"))
        self.pagesMenu.add_command(label = "Exit/Logout Page", command = lambda: self.showFrame("endPage"))
        self.configure(menu = self.menuBar) 

        for p in (startPage, loginPage, registerUserPage, mainPage, helpPage, mileagePage, emailPage, resultsPage, endPage): ## The names of the different classes for each of the pages
            pageName = p.__name__ 
            frame = p(parent = container, controller = self)
            self.frames[pageName] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.showFrame("startPage")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

    def getPage(self, nameOfPage):
        return self.frames[nameOfPage.__name__]

    def changeMenuState(self, state1):
        self.menuBar.entryconfig("Pages", state = state1)


class startPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        titleLabel = tk.Label(self, text = "Welcome to the Start Page", font = controller.titleFont1).grid(row = 0, column = 1)
        loginPageButton = tk.Button(self, text = "Login with already registered account", font = controller.buttonFont1,
                            command = lambda: controller.showFrame("loginPage")).grid(row = 1, column = 1)
        registerUserPageButton = tk.Button(self, text = "Register as a new user", font = controller.buttonFont1,
                            command = lambda: controller.showFrame("registerUserPage")).grid(row = 2, column = 1)

        self.grid_rowconfigure([0, 1, 2], weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        
class loginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        titleLabel = tk.Label(self, text = "Login Page", font = controller.titleFont1).grid(row = 0, column = 1)
        usernameEntryLabel = tk.Label(self, text = "Username", font = controller.labelFont1).grid(row = 1, column = 0)
        passwordEntryLabel = tk.Label(self, text = "Password", font = controller.labelFont1).grid(row = 2, column = 0)
        self.checkLabel = tk.Label(self, text = "", font = controller.labelFont2)
        self.useMenuLabel = tk.Label(self, text = "", font = controller.labelFont2)
        
        self.usernameEntry = tk.Entry(self)
        self.passwordEntry = tk.Entry(self, state = "disabled", show = "*")
        
        self.loginButton = tk.Button(self, text = "Login", font = controller.buttonFont1, command = self.checkUserDetails)
        self.startPageButton = tk.Button(self, text = "Go to Start Page", font = controller.buttonFont1, command = lambda: controller.showFrame("startPage"))
        self.resetButton = tk.Button(self, text = "Reset", font = controller.buttonFont1, command = self.resetLoginPage)     
        
        self.loginButton.grid(row = 3, column = 1)
        self.startPageButton.grid(row = 0, column = 0, sticky = "nw")
        self.resetButton.grid(row = 0, column = 2, sticky = "nw")   
        self.checkLabel.grid(row = 4, column = 1, sticky = "s")
        self.useMenuLabel.grid(row = 5, column = 1, sticky = "s")
        self.usernameEntry.grid(row = 1, column = 1)
        self.passwordEntry.grid(row = 2, column = 1)

        self.grid_rowconfigure([0, 1, 2], weight = 1)
        self.grid_columnconfigure(1, weight = 1)

    def resetLoginPage(self):
        self.usernameEntry.configure(state = "normal")
        self.usernameEntry.delete(0, "end")
        self.passwordEntry.delete(0, "end")
        self.passwordEntry.configure(state = "disabled")
        
        global usernameCorrect
        usernameCorrect = False
        self.checkLabel.configure(text = "")

    def changeEntryStates(self, state1, state2):
        self.usernameEntry.configure(state = state1) ## "disabled" or "normal"  
        self.passwordEntry.configure(state = state2)
        
    def updateLabel(self, textInput):
        self.checkLabel.configure(text = textInput)
        
    def checkUserDetails(self):
        username1 = self.usernameEntry.get()
        password1 = self.passwordEntry.get()
        objectName = self.controller.getPage(loginPage)
        newDb.authUser(username1, password1, objectName)

    def successLogin(self, username1):
        self.loginButton.configure(state = "disabled")
        self.startPageButton.configure(state = "disabled")
        self.resetButton.configure(state = "disabled")
        self.passwordEntry.configure(state = "disabled")
        self.useMenuLabel.configure(text = "Now you can use the menu in the top left hand corner to navigate to the other pages.")
        self.controller.changeMenuState("normal")
        
        objectName = self.controller.getPage(helpPage) 
        objectName.updateUsernameLabel(username1) 
        
        objectName = self.controller.getPage(mainPage) 
        objectName.updateUsernameLabel(username1) 

        objectName = self.controller.getPage(mileagePage) 
        objectName.updateUsernameLabel(username1)

        objectName = self.controller.getPage(emailPage)
        objectName.updateUsernameLabel(username1)

        objectName = self.controller.getPage(resultsPage)
        newDb.getGraphValues(objectName, username1)

        objectName = self.controller.getPage(endPage)
        objectName.updateUsernameLabel(username1)

class registerUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        titleLabel = tk.Label(self, text = "This is the user registration page", font = controller.titleFont1).grid(row = 0, column = 1)
        usernameEnterLabel = tk.Label(self, text = "Username", font = controller.labelFont1).grid(row = 1, column = 0)
        passwordEnterLabel = tk.Label(self, text = "Password", font = controller.labelFont1).grid(row = 2, column = 0)
        self.usernameLabel = tk.Label(self, text = "", font = controller.labelFont2)
        
        self.usernameEntry = tk.Entry(self)
        self.passwordEntry = tk.Entry(self, show = "*")
        
        rUserButton = tk.Button(self, text = "Register User", font = controller.buttonFont1, command = self.registerUserDetails).grid(row = 3, column = 1)
        startPageButton = tk.Button(self, text = "Go to Start Page", font = controller.buttonFont1, command = lambda: controller.showFrame("startPage")).grid(row = 0, column = 0, sticky = "nw")
        
        self.usernameLabel.grid(row = 4, column = 1, sticky = "s")
        self.usernameEntry.grid(row = 1, column = 1)
        self.passwordEntry.grid(row = 2, column = 1)

        self.grid_rowconfigure([0, 1, 2], weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        
    def updateLabel2(self, textInput):
        self.usernameLabel.configure(text = textInput)
    
    def registerUserDetails(self):
        username2 = self.usernameEntry.get()
        password2 = self.passwordEntry.get()
        objectName = self.controller.getPage(registerUserPage)
        newDb.addUser(username2, password2, objectName)
        
class mainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleLabel = tk.Label(self, text = "Main Page", font = controller.titleFont1).grid(row = 0, column = 0, sticky = "e")
        self.recEntryLabel = tk.Label(self, text = "Your most recent entry was: ", font = controller.labelFont4)
        self.top3RecLabel = tk.Label(self, text = "Your top 3 recommendations are shown below: ", font = controller.labelFont4)
        self.usernameLabel = tk.Label(self, text = "", font = controller.labelFont3)
        self.updateRecEntryLabel = tk.Label(self, text = "", font = controller.labelFont2)
        self.updateRTipLabel1 = tk.Label(self, text = "", font = controller.labelFont2) 
        self.updateRTipLabel2 = tk.Label(self, text = "", font = controller.labelFont2) 
        self.updateRTipLabel3 = tk.Label(self, text = "", font = controller.labelFont2) 
        
        self.recEntryLabel.grid(row = 1, column = 0, sticky = "w")
        self.top3RecLabel.grid(row = 3, column = 0, sticky = "w")
        self.usernameLabel.grid(row = 0, column = 2, sticky = "ne")
        self.updateRecEntryLabel.grid(row = 2, column = 0, sticky = "w")
        self.updateRTipLabel1.grid(row = 4, column = 0, sticky = "w") 
        self.updateRTipLabel2.grid(row = 5, column = 0, sticky = "w") 
        self.updateRTipLabel3.grid(row = 6, column = 0, sticky = "w") 

        self.grid_rowconfigure([0, 1], weight = 1)
        self.grid_columnconfigure([0, 1, 2], weight = 1)

    def updateUsernameLabel(self, username1):
        self.usernameLabel.configure(text = "User: " + username1)
        objectName = self.controller.getPage(mainPage)
        newDb.getRecentEntries(username1, objectName, True)
        newDb.checkJobTips(objectName, username1)

    def updateRecentEntryLabel(self, text1):
        self.updateRecEntryLabel.configure(text = text1)

    def noMileage(self): 
        self.updateRTipLabel1.config(text = "No recent record found! Make a maintenance record by navigating to the 'Mileage Page'")

    def tipSystem(self, jobDict, jobNames, jobsNum):
        
        ## codes used: HW - hot weather, CW - cold weather, MMLP - max mileage limit passed, CTMML - close to max mileage limit, EATML - exactly at the mileage limit
        ## jobDict contains: rMileage, rMileageDiff, rMonth, rMaxMileage, rWeatherCheck, rPriority
        
        currentTipList = []
        sortedTipsList = []
        jobs2DArray = [[0 for x in range(3)] for y in range(11)]
        counter = 0
        internalCounter = -1
        tipsArePresent = False
        
        for i in range (jobsNum):
            jobDetails = jobDict[jobNames[i]]
            tipsList = []
            hasTips = False
            if jobDetails[4] != "False":
                if jobDetails[4] == "hot weather":
                    if int(jobDetails[2]) >= 3 and int(jobDetails[2]) <= 8:
                        tipsList.append("HW")
                        hasTips = True
                elif jobDetails[4] == "cold weather":
                    if int(jobDetails[2]) <= 2:
                        tipsList.append("CW") 
                        hasTips = True
                    elif int(jobDetails[2]) >= 9 and int(jobDetails[2]) <= 12:
                        tipsList.append("CW") 
                        hasTips = True
                        
            if jobDetails[1] > jobDetails[3]:
                tipsList.append("MMLP")
                hasTips = True
            elif ((int(jobDetails[3]))-100) < jobDetails[1] < (int(jobDetails[3])):
                tipsList.append("CTMML")
                hasTips = True
            elif jobDetails[1] == jobDetails[3]:
                tipsList.append("EATML")
                hasTips = True

            if hasTips == True:
                internalCounter = internalCounter + 1
                jobs2DArray[internalCounter][0] = jobNames[internalCounter]
                jobs2DArray[internalCounter][1] = jobDetails[5]
                jobs2DArray[internalCounter][2] = tipsList[0]
                counter = counter + 1
                tipsArePresent = True
                
        if tipsArePresent == True:
            for x in range(counter):
                sortedTipsList.append(jobs2DArray[x][1])

            sortedTipsList.sort(reverse=False)

            if counter > 0:
                for y in range(counter):
                    if jobs2DArray[y][1] == sortedTipsList[0]:
                        currentTipList.append(jobs2DArray[y])
                        
                jobDetailsTip1 = jobDict[currentTipList[0][0]]
                tip1Name = currentTipList[0][0]
                tip1Name.replace('{', '')
                tip1Name.replace('}', '')

                if currentTipList[0][2] == "HW":
                    self.updateRTipLabel1.config(text = ("A " + tip1Name + " is suggested as you made this recording during months of normally hot weather"))
                elif currentTipList[0][2] == "CW":
                    self.updateRTipLabel1.config(text = ("A " + tip1Name + " is suggested as you made this recording during months of normally cold weather"))
                elif currentTipList[0][2] == "MMLP":
                    self.updateRTipLabel1.config(text = ("A " + tip1Name + " is suggested as you made this recording with a mileage that is over the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is:" + str(jobDetailsTip1[3]) + " and your mileage was:" + str(jobDetailsTip1[1])))
                elif currentTipList[0][2] == "CTMML":
                    self.updateRTipLabel1.config(text = ("A " + tip1Name + " is suggested as you made this recording with a mileage that is close to the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is: " + str(jobDetailsTip1[3]) + " and your mileage was: " + str(jobDetailsTip1[1])))
                elif currentTipList[0][2] == "EATML":
                    self.updateRTipLabel1.config(text = ("A " + tip1Name + " is suggested as you made this recording with a mileage that is exactly the same as the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is:" + str(jobDetailsTip1[3]) + " and your mileage was:" + str(jobDetailsTip1[1])))

                if counter > 0:
                    sortedTipsList.remove(sortedTipsList[0])

            if counter > 1:
                for y in range(counter):
                    if jobs2DArray[y][1] == sortedTipsList[0]:
                        currentTipList.append(jobs2DArray[y])

                jobDetailsTip2 = jobDict[currentTipList[1][0]]
                tip2Name = currentTipList[1][0]
                tip2Name.replace('{', '')
                tip2Name.replace('}', '')

                if currentTipList[0][2] == "HW":
                    self.updateRTipLabel2.config(text = ("A " + tip2Name + " is suggested as you made this recording during months of normally hot weather"))
                elif currentTipList[0][2] == "CW":
                    self.updateRTipLabel2.config(text = ("A " + tip2Name + " is suggested as you made this recording during months of normally cold weather"))
                elif currentTipList[0][2] == "MMLP":
                    self.updateRTipLabel2.config(text = ("A " + tip2Name + " is suggested as you made this recording with a mileage that is over the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is:" + str(jobDetailsTip2[3]) + " and your mileage was:" + str(jobDetailsTip2[1])))
                elif currentTipList[0][2] == "CTMML":
                    self.updateRTipLabel2.config(text = ("A " + tip2Name + " is suggested as you made this recording with a mileage that is close to the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is: " + str(jobDetailsTip2[3]) + " and your mileage was: " + str(jobDetailsTip2[1])))
                elif currentTipList[0][2] == "EATML":
                    self.updateRTipLabel2.config(text = ("A " + tip2Name + " is suggested as you made this recording with a mileage that is exactly the same as the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is:" + str(jobDetailsTip2[3]) + " and your mileage was:" + str(jobDetailsTip2[1])))
                if counter > 1:
                    sortedTipsList.remove(sortedTipsList[0])

            if counter > 2:
                for y in range(counter):
                    if jobs2DArray[y][1] == sortedTipsList[0]:
                        currentTipList.append(jobs2DArray[y])

                jobDetailsTip3 = jobDict[currentTipList[2][0]]
                tip3Name = currentTipList[2][0]
                tip3Name.replace('{', '')
                tip3Name.replace('}', '')
                
                if currentTipList[0][2] == "HW":
                    self.updateRTipLabel3.config(text = ("A " + tip3Name + " is suggested as you made this recording during months of normally hot weather"))
                elif currentTipList[0][2] == "CW":
                    self.updateRTipLabel3.config(text = ("A " + tip3Name + " is suggested as you made this recording during months of normally cold weather"))
                elif currentTipList[0][2] == "MMLP":
                    self.updateRTipLabel3.config(text = ("A " + tip3Name + " is suggested as you made this recording with a mileage that is over the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is:" + str(jobDetailsTip3[3]) + " and your mileage was:" + str(jobDetailsTip3[1])))
                elif currentTipList[0][2] == "CTMML":
                    self.updateRTipLabel3.config(text = ("A " + tip3Name + " is suggested as you made this recording with a mileage that is close to the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is: " + str(jobDetailsTip3[3]) + " and your mileage was: " + str(jobDetailsTip3[1])))
                elif currentTipList[0][2] == "EATML":
                    self.updateRTipLabel3.config(text = ("A " + tip3Name + " is suggested as you made this recording with a mileage that is exactly the same as the recommended mileage limit for this part"
                                                         + "\n" + "The recommended mileage limit is:" + str(jobDetailsTip3[3]) + " and your mileage was:" + str(jobDetailsTip3[1])))
                 
        else:
            self.updateRTipLabel1.config(text = "There are no recommendations")

class helpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleLabel = tk.Label(self, text = "Help Page", font = controller.titleFont1).grid(row = 0, column = 1)
        welcomeLabel = tk.Label(self, text = "Welcome to the main page of this application. From here you can access the various other parts of this application.",
                          font = controller.labelFont2).grid(row = 1, column = 1)
        menuHelpLabel = tk.Label(self, text = "The menu bar in the top left corner will let you access any page. However the login, register and start pages are excluded",
                          font = controller.labelFont2).grid(row = 2, column = 1)
        usernameHelpLabel = tk.Label(self, text = "For most pages your account's username is displayed in the top right corner. To log out at any time please navigate to the 'Exit/Logout Page'",
                          font = controller.labelFont2).grid(row = 3, column = 1)
        logoutHelpLabel = tk.Label(self, text = "Once you are logged out you cannot access any pages except the login, register and start pages",
                          font = controller.labelFont2).grid(row = 4, column = 1)
        emailHelpLabel = tk.Label(self, text = "The email system only works for gmail accounts. The 'unauthorised apps' needs to be enabled in your account for the email to be sent",
                                  font = controller.labelFont2).grid(row = 5, column = 1)
        self.usernameLabel = tk.Label(self, text = "", font = controller.labelFont3)

        self.usernameLabel.grid(row = 0, column = 2, sticky = "ne")
        
        self.grid_rowconfigure([0, 1, 2, 3, 4], weight = 1)
        self.grid_columnconfigure([1, 2], weight = 1)

    def updateUsernameLabel(self, username1):
        self.usernameLabel.configure(text = "User: " + username1)

class mileagePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.objectName = None
        self.flag1 = False
        
        titleLabel = tk.Label(self, text = "Mileage Page", font = controller.titleFont1).grid(row = 0, column = 1)
        mileageLabel = tk.Label(self, text = "Enter Mileage:", font = controller.labelFont1).grid(row = 1, column = 0)
        jobLabel = tk.Label(self, text = "Choose job/function:", font = controller.labelFont1).grid(row = 2, column = 0)
        dateLabel = tk.Label(self, text = "Enter current date (DD/MM/YYYY):", font = controller.labelFont1).grid(row = 3, column = 0)
        self.usernameLabel = tk.Label(self, text = "", font = controller.labelFont3)
        self.infoLabel = tk.Label(self, text = "", font = controller.labelFont2)

        self.previousCheckVar = tk.BooleanVar(self)
        previousCheckBox = tk.Checkbutton(self, text = "Use same mileage and date as last record", onvalue=True, offvalue=False, variable = self.previousCheckVar).grid(row = 4, column = 0)

        self.usernameLabel.grid(row = 0, column = 2, sticky = "ne")
        self.infoLabel.grid(row = 5, column = 1)
        
        self.username = ""
        
        self.mileageEntry = tk.Entry(self)
        self.dateEntry = tk.Entry(self)

        self.mileageEntry.grid(row = 1, column = 1)
        self.dateEntry.grid(row = 3, column = 1)

        saveDetailsButton = tk.Button(self, text = "Save details", font = controller.buttonFont1,
                                      command = lambda: [newDb.updateMileageValue(self.objectName, self.username), self.usePrevMileageCheck(self.previousCheckVar.get()), self.saveJobRecord(self.username)]).grid(row = 4, column = 1)

        self.jobOptionsVariable = tk.StringVar(self)
        self.jobOptionsVariable.set("None")

        self.jobOptionsList = tk.OptionMenu(self, self.jobOptionsVariable, "None", "Refuel", "Oil change",
                                            "Brake pads replacement", "Lambda/Oxygen Sensor replacement",
                                            "Air conditioning repair", "Radiator replacement", "Battery replacement",
                                            "Heating repair", "Fuel filter replacement", "Headlight replacement")
        self.jobOptionsList.grid(row = 2, column = 1)

        self.grid_rowconfigure([0, 1], weight = 1)
        self.grid_columnconfigure([0, 1], weight = 1)

        self.previousMileageVariable = 0
        self.previousDateVariable = "" 
                                      
    def savePreviousMileageAndDate(self, value1, value2):
        self.previousMileageVariable = value1
        self.previousDateVariable = value2
        
    def validateMileage(self, mileage):
        global previousMileage
        if mileage.isdigit() and mileage != "":
            if "-" not in mileage:
                check1 = True
        else:
            check1 = False

        if check1 == True:
            mileage = int(mileage)
            if previousMileage == True:
                if mileage > self.previousMileageVariable:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def validateDate(self, date):
        flag = False
        if date != "":
            try:
                date.split("/")
                day1 = date.split("/")[0]
                month1 = date.split("/")[1]
                year1 = date.split("/")[2]
            except:
                return False
            
            if len(day1) is 2:
                pass
            else:
                flag = True
                
            if len(month1) is 2:
                pass
            else:
                flag = True
                
            if len(year1) is 4:
                pass
            else:
                flag = True

            if flag == True:
                return False
            else:
                try:
                    day1 = int(day1)
                    month1 = int(month1)
                    year1 = int(year1)
                    dateCheck = datetime.datetime(day = day1, month = month1, year = year1)
                    return True
                except:
                    return False
        
    def updateUsernameLabel(self, username1): 
        self.usernameLabel.configure(text = "User: " + username1)
        self.username = username1
        self.objectName = self.controller.getPage(mileagePage)
        
        
    def saveJobRecord(self, username1):
        if self.flag1 == False:
            mileage1 = self.mileageEntry.get()
            date1 = self.dateEntry.get()
            if self.validateMileage(mileage1) is True and self.validateDate(date1) is True:
                jobOption1 = self.jobOptionsVariable.get()
                newDb.mileageAndJobAdd(mileage1, jobOption1, date1, username1)
                self.infoLabel.configure(text = "Record saved successfully")
            else:
                self.infoLabel.configure(text = "Incorrect details. Try again")
        else:
            jobOption2 = self.jobOptionsVariable.get()
            mileage2 = self.previousMileageVariable
            date2 = self.previousDateVariable
            newDb.mileageAndJobAdd(mileage2, jobOption2, date2, username1)
            self.infoLabel.configure(text = "Record saved successfully")

    def usePrevMileageCheck(self, checkBoxValue):
        global previousMileage
        if checkBoxValue == True and previousMileage == True:
            self.mileageEntry.configure(state = "disabled")
            self.dateEntry.configure(state = "disabled")
            self.flag1 = True

class emailPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        titleLabel = tk.Label(self, text = "Email Page", font = controller.titleFont1).grid(row = 0, column = 1)
        emailALabel = tk.Label(self, text = "Enter your email address:", font = controller.labelFont3).grid(row = 1, column = 0)
        passwordLabel = tk.Label(self, text = "Enter your password:", font = controller.labelFont3).grid(row = 2, column = 0)
        recipientLabel = tk.Label(self, text = "Enter the recipeint email address:", font = controller.labelFont3).grid(row = 3, column = 0)
        subjectLabel = tk.Label(self, text = "Enter your subject:", font = controller.labelFont3).grid(row = 4, column = 0)
        self.usernameLabel = tk.Label(self, text = "", font = controller.labelFont3)
        messageLabel = tk.Label(self, text = "Enter your message:", font = controller.labelFont3).grid(row = 5, column = 0)
        self.username = ""
        self.objectName = ""
        self.infoLabel = tk.Label(self, text = "", font = controller.labelFont2)
        
        
        self.emailAEntry = tk.Entry(self)
        self.passwordEntry = tk.Entry(self)
        self.recipientEntry = tk.Entry(self)
        self.subjectEntry = tk.Entry(self)
        self.message = tk.Text(self, width = 25, height = 5)

        self.emailAEntry.grid(row = 1, column = 1)
        self.passwordEntry.grid(row = 2, column = 1)
        self.recipientEntry.grid(row = 3, column = 1)
        self.subjectEntry.grid(row = 4, column = 1)
        self.message.grid(row = 5, column = 1)
        self.usernameLabel.grid(row = 0, column = 2, sticky = "ne")
        self.infoLabel.grid(row = 7, column = 1)

        self.grid_rowconfigure([0, 1, 2, 3, 4], weight = 1)
        self.grid_columnconfigure([0, 1], weight = 1)

        saveDetailsButton = tk.Button(self, text = "Send Email with Previous Record", command = lambda: newDb.getRecentEntries(self.username, self.objectName, False))
        saveDetailsButton.grid(row = 6, column = 1)

    def updateUsernameLabel(self, username1): 
        self.usernameLabel.configure(text = "User: " + username1)
        self.username = username1
        self.objectName = self.controller.getPage(emailPage)

    def sendEmail(self, rRecord, flag1):
        if flag1 == False:
            inputsValid = True
            messageExist = True
            if self.emailAEntry.get() == "" or self.passwordEntry.get() == "" or self.recipientEntry.get() == "":
                inputsValid = False
            if self.message.get("1.0", "end-1c") == "":
                messageExist = False

            if inputsValid == False:
                self.infoLabel.configure(text = "Incorrect details")
            
            if inputsValid == True:
                try:
                    if messageExist == True:
                        finalMessage = self.message.get("1.0", "end-1c") + "\n" + rRecord
                    else:
                        finalMessage = rRecord
                    #yag = yagmail.SMTP(self.emailAEntry.get(), self.passwordEntry.get())
                    contents = [finalMessage]
                    #yag.send(self.recipientEntry.get(), self.subjectEntry.get(), contents)
                    self.infoLabel.configure(text = "Email sent successfully")
                except:
                    self.infoLabel.configure(text = "Error. Email could not be sent.")
        elif flag1 == True:
            self.infoLabel.configure(text = "No previous records found!")
            
class resultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
    def updateGraphValues(self, yValuesList, xValuesList):
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)

        df=pd.DataFrame({"theXValues": xValuesList, "theYValues": yValuesList }) ## using the pandas module
        ax1 = fig.add_subplot(111)
        df.plot( "theXValues", "theYValues", linestyle='-', marker='o', ax = ax1, legend = None) ## plots graph

        ax1.set_title("A graph to show the mileages and dates of up to 10 records") ## sets title
        ax1.set_xlabel("Dates") ## sets x axis name
        ax1.set_ylabel("Mileages") ## sets y axis name

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) ## creates the widget in Tkinter to allow for the graph and packs it

        toolbar = NavigationToolbar2Tk(canvas, self) ## creates the toolbar used with the graph
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)


        canvas.mpl_connect("key_press_event", on_key_press)

    def insufficientMileage(self, text1):
        insufficientMileageLabel = tk.Label(self, text = text1).grid(row = 0, column = 0)

class endPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        titleLabel = tk.Label(self, text = "Logout/Exit Page", font = controller.titleFont1).grid(row = 0, column = 1)
        self.usernameLabel = tk.Label(self, text = "", font = controller.labelFont3)
        self.usernameLabel.grid(row = 0, column = 2, sticky = "ne")
        exitButton = tk.Button(self, text = "Exit the application", font = controller.buttonFont1,
                               command = lambda: [newDb.endDatabase(), app.destroy()]).grid(row = 1, column = 1)
        self.grid_rowconfigure([0, 1, 2], weight = 1)
        self.grid_columnconfigure([0, 1], weight = 1)

    def updateUsernameLabel(self, username1):
        self.usernameLabel.configure(text = "User: " + username1)
        
if __name__ == "__main__":
    app = mainWindow()
    app.mainloop()



