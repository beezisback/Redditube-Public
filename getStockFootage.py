from os import chdir, walk
from random import randint as rand
from selenium.webdriver.common.by import By
from time import sleep

def getStockFootage(driver, topic, amountOfFootages, stockPath):

    #Open new tab with stock footage related to the topic
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    #Some variables for process
    stockVideos = []
    forbidden = []
    stockTopic = rand(0,len(topic)-1)
    counter56 = 0

    #Go to stock video page
    driver.get("https://www.pexels.com/search/videos/"+str(topic[stockTopic])+"/?orientation=landscape")

    while(counter56 < amountOfFootages):

        #Get stock video
        while(1):
            col = rand(2,50)
            row = rand(1,3)
            nowIllegal = str(col)+' '+str(row)
            if nowIllegal in forbidden:
                pass
            else:
                try:
                    stockVideo = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[6]/div[1]/div[3]/div['+str(row)+']/div['+str(col)+']/article/a/img')
                except Exception:
                    pass
                else:
                    forbidden.append(nowIllegal)
                    break

        #Turn src link into the download link (and then click it)
        stockVideoSRC = stockVideo.get_attribute("src")
        stockVideoSRC = stockVideoSRC[33:]
        instance = stockVideoSRC.find('/')
        stockVideoSRC = stockVideoSRC[:instance]
        stockVideos.append(str(stockVideoSRC))
        
        counter56 = counter56+1

    #Download the videos
    for counter258 in range(len(stockVideos)):
        driver.get('https://www.pexels.com/video/'+str(stockVideos[counter258])+'/download/')
        sleep(1)

    #Make sure we download a valid video file
    chdir(stockPath)
    myCurrentFootage = next(walk(stockPath), (None, None, []))[2]
    for counter56 in range(len(myCurrentFootage)):
        while(1):
            sleep(1)
            myCurrentFootage = next(walk(stockPath), (None, None, []))[2]
            try:
                if ('.tmp' or '.crdownload') in myCurrentFootage[counter56]:
                    pass
                else:
                    break
            except Exception:
                pass

    #Close this tab and go back to reddit
    print("\nDownloaded "+str(amountOfFootages)+" stock videos from the internet.\n")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])