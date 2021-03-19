import glob
import os
from threading import Timer


def delete_all_audiofiles():
    files = glob.glob('static/audiofiles/processed/*')
    for f in files:
        os.remove(f)


def delete_uploads_timer():
    Timer(60.0, delete_uploads_timer).start()  # called every minute
    print("Delete files")


def allowed_file(filename):
    a = '.' in filename and filename.rsplit('.', 1)[1].lower() in {"mp3", "wav"}
    return a
