from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import utils
from bassRemover import remove_bass

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.dirname(__file__) + '/static/audiofiles/uploads/'
app.config["PROCESSED_FOLDER"] = os.path.dirname(__file__) + '/static/audiofiles/processed/'

# delete all uploaded files when app starts
utils.delete_all_audiofiles()

# timer function to delete files
utils.delete_uploads_timer()


@app.route("/", methods=["GET", "POST"])
def upload_audio():

    if request.method == "POST":
        if request.files:
            audiofile = request.files["audiofile"]

            if not utils.allowed_file(audiofile.filename):
                return render_template("upload_audio.html")

            new_filename = os.path.splitext(secure_filename(audiofile.filename))[0] + ".wav"

            audiofile_processed = remove_bass(audiofile)
            audiofile_processed.export(app.config["PROCESSED_FOLDER"] + new_filename, format="wav")

            return render_template("download_audio.html", filename=new_filename)
    else:
        return render_template("upload_audio.html")


@app.route("/downloadAudio/<filename>", methods=["GET"])
def download_audio(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
