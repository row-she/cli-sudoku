import json
import sys
import signal,sys

def exitGame():
    print("\n\n*************************")
    print("***** OK, BYE THEN. *****")
    print("*************************\n")
    sys.exit(0)

def catch_ctrl_C(sig,frame):
    exitGame()

signal.signal(signal.SIGINT, catch_ctrl_C)

solution = []
currentBoard = []
currentStage = 1
currentLevel = ""
userData = {}

def enterMenu():
    global currentLevel
    print("\n****************")
    print("***** MENU *****")
    print("****************\n")
    print("What do you want to do?")
    while True:
        try:
            command = raw_input("\nQuit game (Q), Change Level (L), Resume Game (R): ")
            if command.upper() == "Q":
                exitGame()
            elif command.upper() == "L":
                if not currentLevel:
                    print("\nYour didn't select your level yet.")
                else:
                    print("\nYour current level is: " + currentLevel.upper())
                while True:
                    try:
                        userLevel = str(raw_input("\nSelect level (easy/medium/hard): "))
                        if userLevel == "menu":
                            enterMenu()
                        levelOptions = {
                            "easy": 1,
                            "medium": 2,
                            "hard": 3
                            }
                        if levelOptions[userLevel]:
                            currentLevel = userLevel
                            return True
                    except ValueError:
                        pass
                    except KeyError:
                        pass
                    print("Please enter \'easy\', \'medium\' or \'hard\'.")
            elif command.upper() == "R":
                print("")
                return True
        except ValueError:
            pass
        except KeyError:
            pass
        print("Please enter 'Q', 'L' or 'R'")


def greeting():
    print("\n******************************")
    print("*** WELCOME TO CLI SUDOKU! ***")
    print("******************************")
    print("\nType 'menu' at any prompt to enter menu.\n")
    print("Press 'ctrl-c' to quit at any time.")

greeting()

def getUserStage(level):
    global currentStage
    global userData
    data = json.loads(open("userdata.json", mode='r').read())
    userData = data
    stage = data["progress"][level]
    currentStage = stage
    return stage

def setUserStage():
    global currentLevel
    global currentStage
    global userData
    userData["progress"][currentLevel] = currentStage
    userFile = open("userdata.json", mode='w')
    userFile.write(json.dumps(userData))

def updateBoard(board, userInput):
    rowNum = userInput[1]-1
    colNum = userInput[2]-1
    value = userInput[3]
    goalValue = solution[rowNum][colNum]
    if board[rowNum][colNum] == 1:
        print(("That slot is already filled, dummy!\n").upper())
    else:
        if value != goalValue:
            print("Wrong Answer! Game Over!")
            while True:
                try:
                    retry = str(raw_input("\nTry again? (y/n) "))
                    if retry == "menu":
                        menuAction = enterMenu()
                        if menuAction:
                            newStage = getUserStage(currentLevel)
                            print("Current Stage: " + currentLevel.upper() + "-" + str(newStage))
                            getBoardData(currentLevel, newStage)
                    if retry == "y":
                        global currentBoard
                        greeting()
                        runBoard(currentBoard)
                    elif retry == "n":
                        print("\n************************")
                        print("*** ALRIGHT, SEE YA! ***")
                        print("************************\n")
                        sys.exit(0)
                except ValueError:
                    pass
                print("Please enter \'y\' or \'n\'.")
            sys.exit(0)
        else:
            print("Correct!\n")
            board[rowNum][colNum] = 1
            currentBoard = board

def boardIsComplete():
    for row in currentBoard:
        for col in row:
            if col == False:
                return False
    return True

def runBoard(board):
    #print board
    print("\nHere's your board:\n")
    for rowNum, row in enumerate(solution):
        if rowNum == 0:
            rowDisp = "A"
            print("   1   2   3     4   5   6")
        elif rowNum == 1:
            rowDisp = "B"
        elif rowNum == 2:
            rowDisp = "C"
            print("  ------------+------------")
        elif rowNum == 3:
            rowDisp = "D"
        elif rowNum == 4:
            rowDisp = "E"
            print("  ------------+------------")
        elif rowNum == 5:
            rowDisp = "F"
        rowArray = []
        for colNum, col in enumerate(row):
            if board[rowNum][colNum]:
                rowArray.append("[" + str(col) + "]")
            else:
                rowArray.append("[ ]")
            if colNum==2:
                rowArray.append(":")
        joinedRow = " ".join(rowArray)
        print(rowDisp + " " + joinedRow)
    print("")
    #get user input
    userInput = []
    #get user row
    while True:
        try:
            userRow = str(raw_input("Enter a row (A-F): "))
            if userRow == "menu":
                menuAction = enterMenu()
                if menuAction:
                    newStage = getUserStage(currentLevel)
                    print("Current Stage: " + currentLevel.upper() + "-" + str(newStage))
                    getBoardData(currentLevel, newStage)
            else:
                userRow = userRow.upper()
            rowOptions = {
                "A":1, "B": 2, "C": 3, "D": 4, "E": 5, "F":6
                }
            if rowOptions[userRow]:
                userInput.append(userRow)
                userInput.append(rowOptions[userRow])
                break
        except KeyError:
            pass
        print("Please enter a letter from A to F: ")
    #get user column
    while True:
        try:
            userCol = str(raw_input("Enter a column (1-6): "))
            if userCol == "menu":
                menuAction = enterMenu()
                if menuAction:
                    newStage = getUserStage(currentLevel)
                    print("Current Stage: " + currentLevel.upper() + "-" + str(newStage))
                    getBoardData(currentLevel, newStage)
            else:
                userCol = int(userCol)
            if userCol > 0 and userCol < 7:
                userInput.append(userCol)
                break
        except ValueError:
            pass
        print("Please enter a number between 1 and 6: ")
    #get user value
    while True:
        try:
            userVal = str(raw_input("Enter a value (1-6): "))
            if userVal == "menu":
                menuAction = enterMenu()
                if menuAction:
                    newStage = getUserStage(currentLevel)
                    print("Current Stage: " + currentLevel.upper() + "-" + str(newStage))
                    getBoardData(currentLevel, newStage)
            else:
                userVal = int(userVal)
            if userVal > 0 and userVal < 7:
                userInput.append(userVal)
                print("\nYou've entered the value " + str(userVal) + " for " + \
                      str(userInput[0]) + "-" + str(userInput[2]) + ".")
                while True:
                    try:
                        submit = str(raw_input("Do you want to submit this? (y/n) "))
                        if submit == "menu":
                            menuAction = enterMenu()
                            if menuAction:
                                newStage = getUserStage(currentLevel)
                                print("Current Stage: " + currentLevel.upper() + "-" + str(newStage))
                                getBoardData(currentLevel, newStage)
                        if submit == "y":
                            print("")
                            updateBoard(currentBoard, userInput)
                            print("---------------------------")
                            if boardIsComplete() == False:
                                runBoard(currentBoard)
                            else:
                                print("\n*************************************")
                                print("***** CONGRATULATIONS! YOU WON! *****")
                                print("*************************************\n")
                                global currentStage
                                currentStage = currentStage+1
                                print("Next Stage: " + currentLevel.upper() + "-" + str(currentStage))
                                setUserStage()
                                getBoardData(currentLevel, currentStage)
                        elif submit == "n":
                            runBoard(currentBoard)
                    except ValueError:
                        pass
                    print("Please enter y or n")
                break
        except ValueError:
            pass
        print("Please enter a value between 1 and 6: ")

def getBoardData(level, stage):
    global solution
    global currentBoard
    filepath = "sudokus/6x6/" + str(level) + "/board" + str(stage) + ".json"
    data = json.loads(open(filepath, "r").read())
    solution = data["board"]
    currentBoard = data["show"]
    runBoard(currentBoard)

def selectLevel():
    global currentLevel
    while True:
        try:
            userLevel = str(raw_input("\nSelect level (easy/medium/hard): "))
            if userLevel == "menu":
                menuAction = enterMenu()
                if menuAction:
                    newStage = getUserStage(currentLevel)
                    print("Current Stage: " + currentLevel.upper() + "-" + str(newStage))
                    getBoardData(currentLevel, newStage)
            levelOptions = {
                "easy": 1,
                "medium": 2,
                "hard": 3
                }
            if levelOptions[userLevel]:
                currentLevel = userLevel
                stage = getUserStage(userLevel)
                print("Current Stage: " + currentLevel.upper() + "-" + str(stage))
                getBoardData(userLevel, stage)
        except ValueError:
            pass
        except KeyError:
            pass
        print("Please enter \'easy\', \'medium\' or \'hard\'.")

selectLevel()
