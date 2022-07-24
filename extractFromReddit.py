from better_profanity import profanity
from cleantext import clean
from cv2 import imread
from datetime import date
from getComment import getComments
from getStockFootage import getStockFootage
from gtts import gTTS
from makeVideos import makeVideo
from moviepy.editor import *
from os import chdir, walk, remove, scandir
from re import sub, finditer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from textblob import TextBlob
from webdriver_manager.chrome import ChromeDriverManager

#MAIN VARIABLES
AMOUNT_OF_VIDEOS = 1
AMOUNT_OF_COMMENTS = 15
MIN_COMMENT_LENGTH = 0
MAX_COMMENT_LENGTH = 300
STOCK_FOOTAGE_TOPIC_LIST = ['women','woman']
SUBREDDIT = '' #Input subreddit to search
TOP_OF_TIME_UNIT = 'year' #Input time unit you'd like to search the top posts of. Options: 'all', 'year', 'month', 'week', 'day', 'hour'

#MAIN PATHS
PICTURE_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Topic and Comments Pictures'       #Where the screenshots will be sent to and acquired from
AUDIO_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Topic and Comments Audio'            #Where the tts audio will be sent to and acquired from
STOCK_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Reddit Video\Stock Footage'          #Where the stock footage will be downloaded to and acquired from
MUSIC_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Permanent Clips\Atmosphere'          #Where the background music/atmosphere will be acquired from
OUTPUT_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Reddit Video\Final Videos'          #Where the final video will be sent to and acquired from
THUMBNAIL_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Reddit Video\Thumbnails'         #Where the youtube thumbnail will be sent to and acquired from
PERMANENT_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Permanent Clips\Dead Topics'     #Where the text file with used topics is located
EMPTY_FILES_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Permanent Clips\Empty Files'   #Where the three empty files are located (empty mp3, empty mp4, and empty image (image isn't empty but can be set to 0 opacity))
UPLOAD_TO_YOUTUBE_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Upload to Youtube'       #Where the files used to upload to youtube are located
SECRET_CLIENT_PATH_FILE = r'C:\Users\samlb\Documents\client\client_secret.json'

def killTopic(mainTopicText):
    with open(PERMANENT_PATH+'\\'+"deadTopics.txt", "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        file_object.write(mainTopicText)

#Set webdriver configurations
p1 = {"download.default_directory": STOCK_PATH, "profile.default_content_setting_values.notifications": 2 }
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option("detach", True)
option.add_experimental_option("prefs", p1)
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

#Set options and begin
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
driver.get('https://www.google.com/') #Placeholder
action = ActionChains(driver)

#Clean stockfootage, video, and thumbnail directory. Deleted here (and not before program runs) so I have access to the files between runs.
for file1 in scandir(STOCK_PATH):
    remove(file1.path)
for file2 in scandir(OUTPUT_PATH):
    remove(file2.path)
for file3 in scandir(THUMBNAIL_PATH):
    remove(file3.path)

#Get the stock video
getStockFootage(driver, STOCK_FOOTAGE_TOPIC_LIST, AMOUNT_OF_VIDEOS, STOCK_PATH)

#Counter variables
verifiedVideos = 1
elementCounter = 2
topics = []
alreadyDid = False

while(verifiedVideos <= AMOUNT_OF_VIDEOS):
    
    try:
        #Clean directories every run
        for file2 in scandir(PICTURE_PATH):
            remove(file2.path)
        for file3 in scandir(AUDIO_PATH):
            remove(file3.path)
    except PermissionError:
        pass #The file will get replaced anyway

    #Go to website
    if alreadyDid == False:
        driver.get("https://www.reddit.com/r/"+str(SUBREDDIT)+"/top/?t="+str(TOP_OF_TIME_UNIT))
    else:
        pass

    #Get the topic
    try:
        topic = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[4]/div[1]/div[4]/div['+str(elementCounter)+']')))
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', topic)
    except TimeoutException:
        print("Reddit page didn't load properly (Find Topic). Reloading.")
        continue

    #Check if topic has already been done
    mainTopicText = WebDriverWait(topic, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_eYtD2XCVieq6emjKBH3m'))).text
    alreadyDone = open(PERMANENT_PATH+'\\'+"deadTopics.txt").readlines()
    for counter in range(len(alreadyDone)-1):
        string = alreadyDone[counter]
        alreadyDone[counter] = string[:-1]
    if mainTopicText in alreadyDone:
        print("Topic #"+str(elementCounter-1)+" has already been done.")
        elementCounter = elementCounter + 1
        alreadyDid = True
        continue
    alreadyDid = False

    #Check if topic is an ad
    topicData = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[4]/div[1]/div[4]/div['+str(elementCounter)+']/div/div/div[3]/div[1]/div')))
    if ('ago' not in topicData.text) and ('Promoted' in topicData.text) and ('Posted by' not in topicData.text):
        print("Topic #"+str(elementCounter-1)+" is an advertisement.")
        killTopic(mainTopicText)
        elementCounter = elementCounter+1
        continue
    
    #Check if topic is about a video (this program doesn't do that)
    try:
        topic.find_element(By.CLASS_NAME, "_3UEq__yL-82zX4EyuluREz")
        print("Topic #"+str(elementCounter-1)+" is about a video.")
        killTopic(mainTopicText)
        elementCounter = elementCounter+1
        continue
    except NoSuchElementException:
        pass
    
    #Check if topic is about an embedded video (this program doesn't do that)
    try:
        topic.find_element(By.TAG_NAME, "iframe")
        print("Topic #"+str(elementCounter-1)+" is about a embedded video.")
        killTopic(mainTopicText)
        elementCounter = elementCounter+1
        continue
    except NoSuchElementException:
        pass
    
    #Check if topic is about a slideshow (this program doesn't do that)
    try:
        topic.find_element(By.CLASS_NAME, "kcerW9lbT-se3SXd-wp2i")
        print("Topic #"+str(elementCounter-1)+" is about a slideshow.")
        killTopic(mainTopicText)
        elementCounter = elementCounter+1
        continue
    except NoSuchElementException:
        topic.find_element(By.CLASS_NAME, '_eYtD2XCVieq6emjKBH3m').click()

    #Check if reddit page loaded correctly
    try:
        topicText = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/h1'))).text
        topicPicture = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div')))
    except TimeoutException:
        print("Reddit page didn't load properly (Get Topic Text). Reloading.")
        continue
        
    #If program reaches here, video can be made
    print("Topic #"+str(elementCounter-1)+" is valid.")

    #Fix topic text if need be
    try:
        topicDescription = topicPicture.find_elements(By.CLASS_NAME, '_1qeIAgB0cPwnLhDF9XSiJM')
        fullTopic = topicText
        for counter56 in range(len(topicDescription)):
            fullTopic = str(fullTopic) + '. '+ str(topicDescription[counter56].text)
    except NoSuchElementException:
        pass
    
    #Screenshot the topic (along with any images or description)
    chdir(PICTURE_PATH)
    topicPicture.screenshot('aTopic.png')
    topicSize = imread('aTopic.png')
    topicSize = topicSize.shape
    if (topicSize[0] > 900) or (topicSize[1] > 1740):
        print('Topic #'+str(elementCounter-1)+' screenshot is too large')
        elementCounter = elementCounter+1
        continue

    #Find all the parent comments
    print("\nTOPIC: "+str(topicText)+"\n")
    commentText = getComments(driver, MIN_COMMENT_LENGTH, MAX_COMMENT_LENGTH, AMOUNT_OF_COMMENTS, PICTURE_PATH)

    #Check if video is in "Context Mode"
    if commentText == False:
        elementCounter = elementCounter + 1
        print("The post is in 'Context Mode'")
        continue

    #Get the text-to-speech for all of the comments and topics
    chdir(AUDIO_PATH)
    fullTopic = TextBlob(fullTopic)
    fullTopic = fullTopic.string
    fullTopic = clean(fullTopic, no_emoji=True)
    tts = gTTS(text=(profanity.censor(fullTopic, ' ')), lang='en', slow=False)
    tts.save('aTopic.mp3')
    for voiceCounter in range(len(commentText)):
        tts = gTTS(text=commentText[voiceCounter], lang='en',slow=False)
        tts.save('comment'+str(voiceCounter+1)+'.mp3')

    #Make the video
    makeVideo(verifiedVideos, PICTURE_PATH, AUDIO_PATH, STOCK_PATH, MUSIC_PATH, OUTPUT_PATH, EMPTY_FILES_PATH)

    #Clean text for youtube
    chdir(THUMBNAIL_PATH)
    topicText = sub('\\s+', ' ', topicText)
    cleanTopicText = profanity.censor(topicText, '*')
    cleanTopicText = cleanTopicText.capitalize()
    thumbnailTopic = cleanTopicText.split(' ')
    for counter456 in range(len(thumbnailTopic)):
        thumbnailTopic[counter456] = thumbnailTopic[counter456].strip()
    
    #Make youtube title
    youtubeTitle = ''
    for counter685 in range(len(thumbnailTopic)):
        if counter685 == 0:
            youtubeTitle = str(thumbnailTopic[counter685])
        else:
            youtubeTitle = youtubeTitle + ' ' + str(thumbnailTopic[counter685])
    youtubeTitle = youtubeTitle.capitalize()

    #Make thumbnail
    if len(thumbnailTopic) < 5:
        wordCount = len(thumbnailTopic)
    else:
        wordCount = 5
    thumbnailTopicString = ''
    for counter685 in range(wordCount):
        if counter685 == 0:
            thumbnailTopicString = str(thumbnailTopic[counter685])
        else:
            thumbnailTopicString = thumbnailTopicString + ' ' + str(thumbnailTopic[counter685])
    thumbnailTopicString = thumbnailTopicString.capitalize()
    thumbnailTopicString = thumbnailTopicString + '....'
    thumbnail = TextClip(txt=thumbnailTopicString, method='caption', align='center', kerning=-10 ,size=(1920, 1080), font="Garamond-Bold", color="white", bg_color="black")
    thumbnail.save_frame('#'+str(verifiedVideos)+' thumbnail.png')

    #Store the topic and inform user of status
    topics.append(cleanTopicText)
    print('\nFinished video #'+str(verifiedVideos))
    if verifiedVideos == (AMOUNT_OF_VIDEOS):
        print("\nAll "+str(verifiedVideos)+" videos have been rendered.\nBeginning process to upload them to Youtube.\n")
    else:
        print("\nStarting process to create video #"+str(verifiedVideos+1)+"\n")

    #Add the topic to a text file so it's never used again
    killTopic(mainTopicText)

    elementCounter = elementCounter+1
    verifiedVideos = verifiedVideos+1

#Import function to upload to Youtube
sys.path.insert(1, UPLOAD_TO_YOUTUBE_PATH)
from uploadToYoutube import uploadToYoutube

#Get files and description
videosToUpload = next(walk(OUTPUT_PATH), (None, None, []))[2]
thumbnailsToUpload = next(walk(THUMBNAIL_PATH), (None, None, []))[2]
chdir(UPLOAD_TO_YOUTUBE_PATH)
with open('description.txt', encoding='utf8') as f:
    defaultDescription = f.read()

#Upload all the videos
for counter in range(len(videosToUpload)):
    video = videosToUpload[counter]
    thumbnail = thumbnailsToUpload[counter]
    tags = [SUBREDDIT]
    title = topics[counter]
    title = title.capitalize()
    title = title.strip()
    title = title+' | r/'+SUBREDDIT+' '+str(date.today().year)
    if len(title) > 100:
        addOn = ' | r/'+SUBREDDIT+' '+str(date.today().year)
        instance = 100-len(addOn)
        title = topics[counter]
        title = title[:instance-4]
        try:
            instance = [m.start() for m in finditer(' ', title)]
            title = title[:instance[-1]]
        except Exception:
            pass
        title = title.strip()
        title = title+'... '
        title = title+' | r/'+SUBREDDIT+' '+str(date.today().year)
    description = defaultDescription
    uploadToYoutube(str(title), str(description), tags, str(video), str(thumbnail), counter, SECRET_CLIENT_PATH_FILE, OUTPUT_PATH, THUMBNAIL_PATH)