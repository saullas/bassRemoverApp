from __future__ import unicode_literals

import glob
import os
from threading import Timer
from youtube_dl import YoutubeDL

MAX_DURATION = 20 * 60

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'prefer_ffmpeg': True,
    'outtmpl': 'static/audiofiles/downloaded/' + '%(title)s.%(ext)s'
}


def delete_all_audiofiles():
    files = glob.glob('static/audiofiles/processed/*')
    for f in files:
        os.remove(f)

    files = glob.glob('static/audiofiles/downloaded/*')
    for f in files:
        os.remove(f)


def allowed_file(filename):
    a = '.' in filename and filename.rsplit('.', 1)[1].lower() in {"mp3", "wav"}
    return a


def download_audio_from_youtube_url(url):
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if info["duration"] > MAX_DURATION:
                return "too long"

            title = info["title"]
            ydl.download([url])
            return title + '.mp3'
    except:
        return "error"
