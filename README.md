# Redditube

### STATUS:

*Finished developing.*

### DESCRIPTION:

Turn reddit posts into youtube videos.

When run, the script:
- Fetches a valid post from a chosen subreddit
- Searches the internet for a relevant stock video and downloads it
- Screenshots the reddit post's topic and a pre-determined number of comments
- Extracts the text from the topic and comments
- Runs the extracted text through a text-to-speech process
- Makes a video from the stock video, pictures, audio files, and some atmospheric background music
- Generates a thumbnail and then uploads the video to youtube via the Youtube Upload API 

### NOTES:

- I am aware that Reddit data can be accessed via API, but I wanted to do it this way for fun.