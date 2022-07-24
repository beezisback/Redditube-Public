from changeDate import changeDate
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from os import chdir
from socket import setdefaulttimeout
import datetime

def uploadToYoutube(title, description, tags, videoFilename, thumbnailFilename, number, secretClient, outputPath, thumbnailPath):

    setdefaulttimeout(99999)

    CLIENT_SECRET_FILE = secretClient
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    date = changeDate('changeDate.txt', 10+4, 19+4) #Youtube API works in UTC, but I'm in EST (hence the addition)

    upload_date_time = datetime.datetime(date[0], date[1], date[2], date[3], 0, 0).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryI': 23,
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': False
    }

    chdir(outputPath)
    mediaFile = MediaFileUpload(videoFilename)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    chdir(thumbnailPath)
    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload(thumbnailFilename)
    ).execute()

    print(str(number+1)+" video(s) have been uploaded\n")