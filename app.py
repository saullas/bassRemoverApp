from flask import Flask, render_template, request, send_from_directory, jsonify, after_this_request
from werkzeug.utils import secure_filename
import os
import utils
from bassRemover import remove_bass
import time

app = Flask(__name__)

app.config["PROCESSED_FOLDER"] = os.path.dirname(__file__) + '/static/audiofiles/processed/'

# delete all uploaded files when app starts
utils.delete_all_audiofiles()

# timer function to delete files
utils.delete_uploads_timer()


@app.route("/", methods=["GET"])
def homePage():
    return render_template("upload_audio.html")


@app.route("/uploadUrl", methods=["POST"])
def upload_url():
    return None


@app.route("/uploadAudio", methods=["POST"])
def upload_audio():
    if request.files:
        audiofile = request.files["audiofile"]

        if not utils.allowed_file(audiofile.filename):
            return jsonify({
                "error": "Unsupported format.",
                "status": 400
            })

        try:
            currtime = time.strftime("%Y%m%d-%H%M%S")
            unique_filename = os.path.splitext(secure_filename(audiofile.filename))[0] + currtime + ".wav"

            audiofile_processed = remove_bass(audiofile)
            audiofile_processed.export(app.config["PROCESSED_FOLDER"] + unique_filename, format="wav")

            return jsonify({
                "filename": unique_filename,
                "status": 200
            })
        except:
            return jsonify({
                "error": "An error occured during processing. Please try again.",
                "status": 500
            })
    else:
        return jsonify({
            "error": "No files attached.",
            "status": 400
        })


@app.route("/downloadAudio/<filename>", methods=["GET"])
def download_audio(filename):
    try:
        @after_this_request
        def remove_file(response):
            os.remove(app.config["PROCESSED_FOLDER"] + filename)
            return response

        return send_from_directory(app.config["PROCESSED_FOLDER"], filename, as_attachment=True)
    except:
        return jsonify({
            "error": "There was an error fetching your file.",
            "status": 500
        })


if __name__ == '__main__':
    app.run()
