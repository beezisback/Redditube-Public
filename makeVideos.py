from moviepy.editor import *
from os import walk
from random import randint as rand

def makeVideo(videoCounter, picturePath, audioPath, stockPath, musicPath, outputPath, emptyPath):

    #Get files
    myAudioFiles = next(walk(audioPath), (None, None, []))[2]
    myImageFiles = next(walk(picturePath), (None, None, []))[2]

    #Make audio file (without music)
    audio = []
    emptyAudio = AudioFileClip(emptyPath+'\\'+'emptyAudio.mp3')
    for counter1 in range(len(myAudioFiles)):
        theAudio = AudioFileClip(audioPath+'\\'+str(myAudioFiles[counter1]))
        theAudio = theAudio.subclip(0,-0.1)
        audio.append(theAudio)
        audio.append(emptyAudio)
    audioFiles = concatenate_audioclips(audio)
    audioFiles = audioFiles.set_fps(44100)
    audioFiles = audioFiles.volumex(2)

    #Make comment video
    images = []
    emptyImage = ImageClip(emptyPath+'\\'+'emptyImage.png', duration=0.5)
    emptyImage = emptyImage.set_opacity(0)
    for counter2 in range(len(myImageFiles)):
        theImage = ImageClip(picturePath+'\\'+str(myImageFiles[counter2])).set_duration(audio[counter2*2].duration)
        theImage = theImage.resize(2)
        images.append(theImage)
        images.append(emptyImage)
    theImages = concatenate_videoclips(images, method='compose')
    theImages = theImages.set_position(("center"))
    theImages = theImages.set_fps(10)

    #Get stock video
    myStock = next(walk(stockPath), (None, None, []))[2]
    stockFile = VideoFileClip(stockPath+'\\'+str(myStock[0]), target_resolution=(1080, 1920), audio=False)
    stockFile = stockFile.subclip(0.5,-0.5)
    stockFile = stockFile.loop(duration = theImages.duration)
    stockFile = stockFile.set_fps(30)

    #Get background music
    myMusic = next(walk(musicPath), (None, None, []))[2]

    #Make final audio and final video
    with AudioFileClip(musicPath+'\\'+str(myMusic[rand(0,len(myMusic)-1)]), fps=44100) as musicFile:
        musicFile = afx.audio_loop(musicFile, duration=theImages.duration)
        finalAudio = CompositeAudioClip([musicFile, audioFiles])
        finalAudio = finalAudio.set_fps(44100)
        finalVideo = CompositeVideoClip([stockFile, theImages])
        finalVideo = finalVideo.set_audio(finalAudio)
        finalVideo.write_videofile(outputPath+'\\'+'finalVideo #'+str(videoCounter)+'.mp4')

# For testing
# PICTURE_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Topic and Comments Pictures'    
# AUDIO_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Topic and Comments Audio'         
# STOCK_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Reddit Video\Stock Footage'       
# MUSIC_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Permanent Clips\Atmosphere'       
# OUTPUT_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Reddit Video\Final Videos'       
# THUMBNAIL_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Reddit Video\Thumbnails'      
# PERMANENT_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Permanent Clips\Dead Topics'  
# EMPTY_FILES_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Permanent Clips\Empty Files'
# UPLOAD_TO_YOUTUBE_PATH = r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM_PUBLIC\Upload to Youtube'     

# makeVideo(1, PICTURE_PATH, AUDIO_PATH, STOCK_PATH, MUSIC_PATH, OUTPUT_PATH, EMPTY_FILES_PATH)