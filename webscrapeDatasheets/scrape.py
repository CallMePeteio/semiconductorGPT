
from databace import deleteRowsFromTable, insertIntoTable, getDataFromTable

from pynput.keyboard import Key, Controller
from bs4 import BeautifulSoup

import pyperclip
import pyautogui
import keyboard
import win32gui
import sqlite3
import logging
import shutil
import mouse
import time
import os



#manuName = "Infineon"
#pageItems = 20
#listItemHeight, startHeight = 30, 625
#scrapeImgPos, scrapeDatasheetPos = [50, startHeight], [280, startHeight]
#scrollPositions = []



def switchToApplication(appName='chrome', url=None):
    def callback(hwnd, extra):
        window_title = win32gui.GetWindowText(hwnd)
        if appName.lower() in window_title.lower():
            try:
                win32gui.SetForegroundWindow(hwnd)
            except:
                pyautogui.hotkey('alt', 'tab')
            extra['found'] = True

    extra = {'found': False}
    win32gui.EnumWindows(callback, extra)

    if not extra['found']:
        raise Exception(f"No {appName.capitalize()} window found!")

    if url != None and appName.lower() == 'chrome':
        pyautogui.hotkey('ctrl', 't')
        keyboard = Controller()
        keyboard.type(url)
        keyboard.press(Key.enter)
        time.sleep(9)


def getPageContent():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    return pyperclip.paste()

        
def getLabels(pageContent, startLabelWord, endLabelWord):
    startLabelIndex = pageContent.find(startLabelWord) + len(startLabelWord) + 1
    endLabelIndex = pageContent.find(endLabelWord) + len(endLabelWord) + 1

    labels = pageContent[startLabelIndex:endLabelIndex].split("\t") # SPLITS THE TEXT INTO DIFFRENT UNITS
    labels = [label.strip() for label in labels] # REMOVES ALL SPACES
    labels.insert(0, "Image Link")
    return labels


def formatComponentParameters(rawCompStr, datasheetLink, imageLink):    
    componentUnfiltered = rawCompStr.split("\t")
    componentParameters = []
    for i, parameter in enumerate(componentUnfiltered):

        if "\r" in parameter:
            parameter = parameter.replace("\r", "")

        if "\n" in parameter and i == 0: 
            firstParameters = parameter.split("\n")
            if len(firstParameters) == 6: 
                compName = firstParameters[0] + " " + firstParameters[1]
                componentParameters.append(compName)
                componentParameters.append(datasheetLink) # THIS IS THE LINK
                componentParameters.extend(firstParameters[4:6]) # ADDS THE USD AND NUM OF AUTH SELLERS
            else:
                return False   
        elif i == 3: 
            iHateMyLife = parameter.split("\n")[1:]
            componentParameters.extend(iHateMyLife)
        
        elif "\n" in parameter:
            componentParameters.extend(parameter.split("\n"))
        else: 
            componentParameters.append(parameter)

    componentParameters.insert(0, imageLink)

    lastItemIndex = len(componentParameters) -1
    if len(componentParameters[lastItemIndex]) == 0:
        componentParameters.pop(lastItemIndex)

    return componentParameters
    
def verifyComponentParameters(component): # NOT IN USE 
    patterns = [("w", 7), ("v", 10), ("a", 11), ("v", 12), ("v", 14), ("w", 15), ("f", 16), ("v", 22), ("v", 24), ("END FLAG", 0)] 

    patternCounter = 0
    for i, parameter in enumerate(component):
        if i == patterns[patternCounter][1]:
            if patterns[patternCounter][0] in parameter.lower() or len(parameter) == 0:
                patternCounter += 1

    print(patternCounter, len(patterns) -1)
    if patternCounter == len(patterns) -1:
        return True
    return False

def rightClickDropdown(listNum, duration=0.2):
    xOffset, zOffset, initZoffset = 100, 35, 15 
    mouse.click("right")
    mouse.move(xOffset, initZoffset + zOffset*listNum, absolute=False, duration=duration) # MOVES TO THE FIRST ITEM
    mouse.click()
    time.sleep(0.2)

def getImgAndDatasheet():



   

    compImgDataLink, scrollOverItemAmounts = [], [4, 10]
    scrollWheelHeight = startHeight/2


    for scrollOverItemAmount in scrollOverItemAmounts:
        mouse.drag(1915, scrollWheelHeight, 1915, scrollWheelHeight + listItemHeight * scrollOverItemAmount, duration=0.5)
        scrollWheelHeight += listItemHeight * scrollOverItemAmount


        for i in range(len(scrollOverItemAmounts)):

            mouse.move(scrapeImgPos[0], scrapeImgPos[1], duration=2)   
            rightClickDropdown(2)
            imgLink = pyperclip.paste()

            mouse.move(scrapeDatasheetPos[0], scrapeDatasheetPos[1], duration=2)
            rightClickDropdown(3, duration=2)
            datasheetLink = pyperclip.paste()


            compImgDataLink.append((imgLink, datasheetLink))

            scrapeImgPos[1] += 85
            scrapeDatasheetPos[1] += 85
            
            print(scrapeImgPos[0], scrapeDatasheetPos[0])


            time.sleep(3)

        #break
        

def copyHTML(copyHtmlPos = (1433, 162)):
    pyautogui.hotkey('ctrl', 'shift', "i")
    time.sleep(2)
    mouse.move(1465, 120)
    mouse.click()

    mouse.move(copyHtmlPos[0], copyHtmlPos[1], duration=1)
    mouse.click("right")

    mouse.move(93, 172, absolute=False, duration=1)
    mouse.click()
    mouse.move(175, 0, absolute=False, duration=1)
    mouse.click()
    time.sleep(0.5)

def saveHTML(htmlPath, htmlName, checkTimes=40, delay=0.5):
    fullHtmlPath = htmlPath + "/" + htmlName + ".html"        
    if not os.path.exists(fullHtmlPath):
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1.3)

        mouse.move(1580, 350, duration=0.5)
        mouse.click()
        pyautogui.hotkey('ctrl', 'a')
        keyboard.type(htmlPath)
        keyboard.press(Key.enter)

        mouse.move(0, 380, absolute=False, duration=0.5)
        mouse.click()
        pyautogui.hotkey("ctrl", "a")
        keyboard.type(htmlName)
        time.sleep(0.8)
        keyboard.press(Key.enter)

        filePath = htmlPath + "/" + htmlName
        extraFilePath = filePath + "_files"
        for i in range(checkTimes): # TRIES FOR 20 SECDONS (WAITING FOR FILE DOWNLOAD)

            if os.path.exists(extraFilePath) and os.path.exists(filePath): # CHECKS IF THE EXTRA FILES EXIST

                time.sleep(4)
                filesInDir = os.listdir(extraFilePath)
                for files in filesInDir:
                    if not ".jpg" in files or not ".png" in files:
                        os.remove(extraFilePath + "/" + files)
                return fullHtmlPath


            elif os.path.exists(fullHtmlPath): # IF THE FILE EXISTS BUT THE EXTRA FILE DOSENT
                logging.error(f"Extra files wasnt created for file: {htmlName}")
                return fullHtmlPath

            time.sleep(delay)
        return False

    else:
        logging.error(f"Skipping {htmlName}, Because file already exists!")
        return fullHtmlPath



    #mouse.move(140, 70, absolute=False, duration=2)
    #mouse.click()
    #time.sleep(0.5)





logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                              '%m-%d-%Y %H:%M:%S')

databasePath = "D:/Coding/Projects/SemiConductorGPT/website/instance/database.db"
conn = sqlite3.connect(databasePath)
cursor = conn.cursor()


fullhtmlPath = "D:/Coding/Projects/SemiConductorGPT/webscrapeDatasheets/htmlScraped"
endNum = 980
startPlace = 0  # THERE IS 20 COMPNENTS FOR EATCH PAGE, SO IF startPlace=20, THEN IT WILL START ON THE SECOND PAGE
keyboard = Controller()

componentType = "mosfet"
scrapeDirName = "htmlScraped"
scriptPath = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") # GETS THE PATH FOR THE CURRENT SCRIPT
components = [] # KEEPS TRACK OVER ALL OF THE DIFFRENT COMPONETNS, WITH LABELS

manufacturerNameId = [("infineon", 196), ("onsemi", 278), ("vishay", 30), ("stmicroelectronics", 355), ("international_rectifier", 202), ("toshiba", 375)]

for manufacturerName, manufacturerId in manufacturerNameId:

    componentManufacturer = manufacturerName
    category = componentType + "_" + componentManufacturer


    hasManufacturer = getDataFromTable("manufacturer", ["manufacturerName"], [componentManufacturer], cursor)

    
    #input(f"{componentManufacturer} {category}")

    if len(hasManufacturer) == 0: 
        insertIntoTable("manufacturer", [(componentManufacturer,)],["manufacturerName"], cursor, conn)


    input("inserted")
    for itemNum in range(startPlace, endNum, 20):

        htmlPath = fullhtmlPath + "/" + category + str(itemNum) + ".html"        
        if not os.path.exists(htmlPath):
            url = f"https://octopart.com/search?q=&category_id=4229&manufacturer_id={manufacturerId}&start={itemNum}"
            switchToApplication(url=url) # SWITCHES TO CHROME, AND OPENS A NEW TAB WITH THE INPUTTED URL
            htmlPath = saveHTML(fullhtmlPath, category + str(itemNum)) # SAVES THE HTML
            pyautogui.hotkey("ctrl", "w") # CLOSES THE PAGE
            switchToApplication("Code")

        logging.info(f"Starting components: ({itemNum}/{endNum})")

        #htmlPath = "D:/Coding/Projects/SemiConductorGPT/webscrapeDatasheets/htmlScraped/Mosfet_Infineon_180.html"

        if htmlPath != False:
            with open(htmlPath, "r", encoding="utf-8") as htmlFile:
                html = htmlFile.read()


            soup = BeautifulSoup(html, 'html.parser')


            labels = [] # KEEPS TRACK OVER ALL OF THE DIFFRENT LABELS
            labelsTable = soup.find_all('tr', class_=['jsx-1894495442', 'columns']) # FINDS THE MAIN LABEL BOX
            for i, label in enumerate(labelsTable[1].find_all("th")): # LOOPS OVER ALL OF THE LABELS

                if i == 0: # THE IMAGES DOSENT HAVE A 
                    labels.append("imagepath")
                elif i == 2:
                    labels.append("datasheetlink")
                    labels.append("cadmodellink")
                else:
                    labelStr = label.text.strip().lower()


                    if " " in labelStr:
                        labels.append(labelStr.replace(" ", ""))
                    else:
                        labels.append(labelStr) # APPENDS THE TEXT (LABELS) TO THE LIST


            allParameters = []
            items = soup.find(id="__next") # FINDS THE MAIN DIV BOX
            items = items.find('tbody', class_='jsx-1894495442')

            for item in items.find_all("tr", class_="jsx-1313607631"): # LOOPS OVER ALL OF THE DIFFRENT ITEMS (COMPONENTS)
                parameters = [] # KEEPS TRACK OVER THE COMPONENTS PARAMETERS
                imagePath = scriptPath + "/htmlScraped/" + item.find("img")["src"][2:] # GETS THE FULL PATH TO THE LOCALLY STORED IMAGE
                compName = item.find("img").get('alt', '').replace(" : ", " ") # GETS THE COMPONENT NAME 
                datasheetAndModelSoup = item.find_all("td")[0] # MAKES THE SOUP FROM THE TD TAG (FIRST) THAT CONTAINS TWO DIFFRENT HREFS CONTAINING THE MODEL LINK AND DATASHEET LINK

                datasheetLink, dModelLink = "", "" # INITIALIZES THE VARIABLES, IF THERE ISNT ANY 3D MODEL, THEN KEEP THE LINK EMPTY
                for i, data in enumerate(datasheetAndModelSoup.find_all("a")): # LOOPS OVER ALL OF THE ANCOR TAGS
                    if i == 0: 
                        datasheetLink = data.get("href")
                    if i == 1: 
                        dModelLink = data.get("href")
                        break


                parameters.extend([imagePath, compName, datasheetLink, dModelLink]) # ADDS THE INFORMATION GATHERED TO THE PARAMETERS LIST

                for parameter in item.find_all("td")[1:]: # LOOPS OVER ALL OF THE OTHER PARAMETERS
                    parameters.append(parameter.text.strip()) # ADDS THE PARAMETER TO THE PARAMETERS LIST
                allParameters.append(parameters) # APPENDS THE LIST OF PARAMETERS TO ANOTHERLIST (ALL PARAMETERS): allParameters = [[PARAMETER COMP1], [PARAMETER COMP2], [PARAMETER COMP3], ETC]


            for component in allParameters:
                component = list(zip(labels, component)) # ADDS THE LABELS
                if len(labels) == len(component):
                    compTypeId = getDataFromTable("componentType", ["componentType"], [componentType], cursor)[0][0]
                    manuId = getDataFromTable("manufacturer", ["manufacturerName"], [componentManufacturer], cursor)[0][0]

                    compName = component[1][1].replace(componentManufacturer.title() + " ", "")
                    insertIntoTable("component", [(compTypeId, manuId, compName)],["componentTypeID", "manufacturerID", "componentName"], cursor, conn)
                    compId = getDataFromTable("component", ["componentTypeID", "manufacturerID", "componentName"], (compTypeId, manuId, compName), cursor)[0][0]
                    component.pop(1)

                    for parameter in component:

                        if parameter[1] != "":
                            insertIntoTable("componentSpecifications", [(compId, parameter[0].lower(), parameter[1].lower())], ["componentID", "specName", "specValue"], cursor)

        conn.commit()


#pageContent = getPageContent() # GETS ALL OF THE CONTENT IN THE WEB PAGE, THIS IS IN STRING FORM. JUST CTR + A AND CTRL + C


#getImgAndDatasheet()

 
#
#startLabelWord, endLabelWord = "Compliance", "RoHS" # THERE IS LUCKLY A PATTERN FOR THE FIRST AND LAST WORD, ENCLOSING THE LABELS
#labels = getLabels(pageContent, startLabelWord, endLabelWord) # GETS ALL OF THE LABELS, RETURNS A LIST
#
#startCompWord, endCompWord = "RoHS", "…" # THERE IS LUCKLY A PATTERN FOR THE FIRST LAND LAST WORDS, ENCLOSING THE LABELS
#startCompIndex = pageContent.find(startCompWord) + len(startCompWord) + 1 # FINDS THE FIRST INDEX OF WHERE THE WORD OCCURS, THIS IS THE START OF THE COMPONENTS
#endCompIndex = pageContent.find(endCompWord) + len(endCompWord) + 1 # FINDS THE LAST INDEX OF WHERE THE WORD OCCURS, THIS IS THE END OF THE COMPONENTS
#
#x = 0
#rawCompStrings = pageContent[startCompIndex:endCompIndex].split(manuName) # RETURNS A LIST CONTAINING ALL OF THE COMPONENTS, ON THE PAGE IN STRING FORM
#for i, rawCompStr in enumerate(rawCompStrings): # LOOPS OVER ALL OF THE COMPONETNS
#    rawCompStr = manuName + rawCompStr # ADDS THE MANUFACTURER NAME BACK, BECAUSE IT IS USED FOR SPLITTING IN THE CODE ABOVE
#
#    component = formatComponentParameters(rawCompStr, "DATASHEET LINK", "IMAGE LINK") # RETURNS A LIST OF ALL THE DIFFRENT PARAMETERS FOR THE COMPONENT. 
#
#    if component != False: # IF THERE WASNT AN ERROR CONVERTING THE RAW STRING INTO A LIST
#        if len(component) == len(labels): # CHECKS IF THERE IS PARAMETERS FOR EATCH LABEL
#            print(list(zip(labels, component)))
#            x+=1
#        else:
#            print(component)
#    else:
#        print(component)
#
#        
#
#    #verification = verifyComponentParameters(component)
#    
#
    




#mouse.move(scrapeLeftPos[0], scrapeLeftPos[1], duration=1)
#mouse.click()
#mouse.wheel(-9)
#time.sleep(8)   
#
#mouse.wheel(-7)
