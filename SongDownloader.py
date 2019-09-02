#SongDownloader.py by Joshua Fung
#Last edit: August 18, 2019
#In order for this to work with  kpop songs, song names in file should be written in the order of "group name" + "song name"

#Kinda works, if theres more than one song, it may not fully download the last song in the list

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import sys, time, os


#Check python version
print("Python Version: "+ sys.version)

def downloadSong(songs):


    repeat = 1
    counter = 0
    #Will hold the filename of the song that will be download
    songNames = []

    #Website stuff
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", "C:\\Songs")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ".mp3 audio/mpeg")
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)
    profile.set_preference("general.warnOnAboutConfig", False)
    profile.update_preferences()

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://www.mp3juices.cc/")
    mainWindow = driver.current_window_handle

    while repeat == 1:

        #Finds the input and enteres in the name of the song
        input = driver.find_element_by_id("query")
        #Gets rid of text in the input box
        input.clear()
        input.send_keys(songs[counter])

        #If the button doesn't load in time, keep clicking lol
        passed = False
        while passed == False:
            try:
                #Finds the button and clicks it
                button = driver.find_element_by_id("button")
                button.click()
                passed = True
            except:
                passed == False
                print("Reran code to click first download button")
                time.sleep(1)

        #Wait for the restults to load
        time.sleep(1.5)

        passed = False
        while passed == False:
            try:
                #Finds the name of the youtube video
                name = driver.find_elements_by_class_name("name")
                songNames.append(name[0].text)

                #Gets the first result
                downloadButtonShower = driver.find_elements_by_class_name("options")
                downloadButtonShower[0].click()
                passed = True
            except:
                passed == False
                print("Reran code to click second download button")
                time.sleep(1)

        #Wait for the restults to load
        time.sleep(2)

        #Finds the actual download button and presses it
        passed = False
        while passed == False:
            try:
                downloadButton = driver.find_elements_by_class_name("url")
                downloadButton[0].click()
                passed = True
            except:
                passed = False
                print("Reran code to actually download the song")
                time.sleep(1)

        #Goes to the next song
        counter+=1

        #This section will close the pop up windows
        handles = driver.window_handles
        for x in range(len(handles)):
            if handles[x] != mainWindow:
                driver.switch_to_window(handles[x])
                driver.close
                x = len(handles)

        #print(songNames)
        #print(len(songs))
        print(len(os.listdir("C:\\Songs")), counter, "yaaa")
        #Checks if there are any more songs to download
        if counter == len(songs):
                #Exit loop and prepare to close
            repeat = 0
            #3.5 seconds to download a song until moving onto the next one
            #time.sleep(3.5)
        #Not all songs have been downloaded
        else:
            passed = False
            #If they all are not finished downloading
            while passed == False:
                #Everything is finished, exit loop
                if len(os.listdir("C:\\Songs")) == counter:
                    print("Finished downloading "+songs[counter-1])
                    passed = True
                #Keep waiting
                else:
                    print("Downloading "+songs[counter-1])
                    time.sleep(1)
    #Close web browser
    print("Download(s) Complete")
    driver.close()

    counter = 0

    #Hold the file paths
    paths = []


#This whole section is for renaming the files, except i couldnt get it to work becaues python wont
#recognize korean chaacters (i think) so i kinda just gave up lol
    #Loop through all files in the Songs folder and rename them
    #for fileName in os.listdir("C:\\Songs"):
    #    paths.append(str(fileName))
#
    #print(paths)
#
    #for fileName in paths:
    #    dst = songs[counter]+".mp3"
    #    os.rename(paths[counter],dst)
    #    counter+=1


def readFile():
    #Gets the file with the songs in them
    file = open("songs.txt","r")

    #Checks to see if the file is readable
    if file.mode == "r":
        content = file.readlines()

    #Initializes array
    songs = []

    #Puts songs into array
    for x in content:
        songs.append(x.strip()+" lyrics") #strip removes extra white space

    #Shows songs that will be downloaded
    print("Songs that will be downloaded:")
    for x in songs:
        print(x)
    #Empty space for formatting
    print("")

    # define the name of the directory to be created
    path = "C:\\Songs"

    #Makes the songs folder that will it will download to
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed. File either already exists or another error has occured" % path)
    else:
        print ("Successfully created the directory %s " % path)

    #Downloads songs
    downloadSong(songs)

#Runs the program
readFile()
