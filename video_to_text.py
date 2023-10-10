# Transform an audio from a YouTube video to text script with language detection.


# Description: This script will ask the user for a YouTube video URL, download the audio from the video, transform it to text, detect the language of the file and save it to a txt file.


# import required modules
import os
import re
import whisper
from langdetect import detect
from pytube import YouTube
from pathlib import Path


# Function to open a file
def startfile(fn):
    os.system('open %s' % fn)


# Function to create and open a txt file
def create_and_open_txt(text, filename):
    # Create and write the text to a txt file
    with open(filename, "w") as file:
        file.write(text)
    #startfile(filename)
    


def sanitize_filename(filename):
    # Replace invalid characters with underscores
    sanitized_filename = re.sub(r'[\/:*?"<>|]', '_', filename)
    return sanitized_filename


# Ask user for the YouTube video URL
url = "https://www.youtube.com/watch?v=aywZrzNaKjs"

# Create a YouTube object from the URL
yt = YouTube(url)
title = sanitize_filename(yt.title)
# Get the audio stream
audio_stream = yt.streams.filter(only_audio=True).first()

# Download the audio stream
output_path = f"YoutubeVideoTranscribeQAData/{title}"
filename = "audio.mp3"
print(filename)

audio_stream.download(output_path=output_path, filename=filename)


audio_path = f"{output_path}/{filename}"
model = whisper.load_model("base")

result = model.transcribe(audio_path)
transcribed_text = result["text"]



language = detect(transcribed_text)
print(f"Detected language: {language}")


create_and_open_txt(transcribed_text, f"{output_path}/transcribe.txt")