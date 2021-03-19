from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["ALLOWED_EXTENSIONS"] = {"mp3", "wav", "flac"}
app.config["UPLOAD_FOLDER"] = os.path.dirname(__file__) + '/static/audiofiles/uploads/'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/uploadAudio", methods=["GET", "POST"])
def upload_audio():

    if request.method == "POST":
        if request.files:
            audiofile = request.files["audiofile"]

            if not allowed_file(audiofile.filename):
                return render_template("public/upload_audio.html")

            new_filename = secure_filename(audiofile.filename)
            audiofile.save(os.path.join(app.config["UPLOAD_FOLDER"]), new_filename)
            print("image saved")
            return render_template("public/upload_audio.html")

    return render_template("public/upload_audio.html")


def allowed_file(filename):
    a = '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    return a


if __name__ == '__main__':
    app.run()
