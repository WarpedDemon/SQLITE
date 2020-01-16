import json
import os
import sqlite3
import os
class MovieMaintainer():
    def __init__(self):
        self.CurrentData = []
        self.Additions = []
        self.Deletions = []
        self.CurrentFileName = ""
        self.saveName = self.GetDatabaseNameInput()
        self.MainLoop()

    def MainLoop(self):
        self.CreateLocalDatabase()
        self.CurrentData = self.ReadData(self.CurrentFileName)
        self.CurrentData.sort()
        self.Active = True
        while self.Active:

            #Display Current Data
            index = -1
            #for i in self.CurrentData:
                #print("DEBUG: Current Data Being Displayed: " + i)

            if len(self.CurrentData) > 0:
                for i in self.CurrentData:
                    index += 1
                    print(str(index + 1) + ": " + i)
            else:
                print("-- no items are in the list --")

            #Ask options...
            if len(self.CurrentData) > 0:
                print("[A]dd [D]elete [S]ave [Q]uit")
            else:
                print("[A]dd [Q]uit")

            userInput = input("Please enter an option: ")
            userInput = userInput.lower()
            if userInput == "a":
                self.Add()
            elif(userInput == "d"):
                self.Delete()
            elif(userInput == "s"):
                self.Save()
            elif(userInput == "q"):
                self.Quit()
            else:
                print("ERROR: invalid choice--enter one of 'AaDdSsQq'")
                os.system("pause")

    """Tool Box Bellow"""

    def CreateLocalDatabase(self):
        # Init db
        self.connection = sqlite3.connect(self.saveName + ".db")
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(
                """CREATE TABLE movies ( Id INT, title VARCHAR(25), PRIMARY KEY (Id) )""")
        except:
            # print("Database Exists")
            pass
        # Open a connection to sql

    def Delete(self):
        deletion = input("Please enter a number to delete: ")
        if(deletion.isdigit()):
            self.Deletions.append(self.CurrentData[int(deletion)-1])
            self.CurrentData.remove(self.CurrentData[int(deletion)-1])
            self.CurrentData.sort()
        else:
            print("Invalid Input.")
        return

    def Quit(self):
        if self.CurrentData == self.ReadData(self.CurrentFileName):
            pass
        else:
            user = input("unsaved changes (y/n): ")
            if user.lower() == "y":
                self.exit = True
                self.Save()

        self.Active = False

    def Save(self):
        #print("DEBUG: Saving to SQLite Database '" + self.saveName + "'")

        self.databaseData = []
        self.cursor.execute("""SELECT * FROM movies""")

        sqlCommand = ""

        #Sync Saves
        for newItem in self.Additions:
            sqlCommand = """INSERT INTO movies (title) VALUES('""" + newItem + """')"""

            self.executeSQL(sqlCommand)

        #Sync Deletions
        for newItem in self.Deletions:
            sqlCommand = """DELETE FROM movies WHERE title='""" + newItem + """'"""

            self.executeSQL(sqlCommand)

        self.Additions = []
        self.Deletions = []
        self.CurrentData = self.ReadData(self.CurrentFileName)
        self.CurrentData.sort()

        #print("DEBUG: Saved to SQLite Database '" + self.saveName + "'")

    def executeSQL(self, sqlCommand):
        #print(sqlCommand)
        self.cursor.execute(sqlCommand)
        self.connection.commit()

    def Add(self):
        addition = input("Please enter a new entry: ")
        if(addition != ""):
            self.Additions.append(addition)
            self.CurrentData.append(addition)
            self.CurrentData.sort()
        else:
            print("Invalid Input")
        return

    def GetFiles(self):
        val = ""
        listfiles = os.listdir(".")
        for file in listfiles:
            if file[-3:] == ".db":
                val += file + " "

        print("Database Files: " + val)

    def GetDatabaseNameInput(self):
        self.GetFiles()
        return input("Choose database name: ")

    def ReadData(self, dbname):
        self.executeSQL("""SELECT * FROM movies""")
        databaseResults = self.cursor.fetchall()

        #print("DEBUG: Current Program Data: " + str(self.CurrentData))
        #print("DEBUG: Database Data: " + str(databaseResults))

        results = []
        for row in databaseResults:
            #print("DEBUG: DataBase Row Info: " + row[1])
            results.append(row[1])

        return results

Start = MovieMaintainer()