import os
import utils
import time
import sys

from flask import Flask, render_template, request, send_from_directory, jsonify, after_this_request
from werkzeug.utils import secure_filename
from bassRemover import remove_bass

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

UPLOAD_FOLDER = os.path.dirname(__file__) + '/static/audiofiles/uploaded/'
PROCESSED_FOLDER = os.path.dirname(__file__) + '/static/audiofiles/processed/'
DOWNLOAD_FOLDER = os.path.dirname(__file__) + '/static/audiofiles/downloaded/'

# delete all saved files when app starts and every n minutes
utils.delete_all_audiofiles()


@app.route("/", methods=["GET"])
def homePage():
    return render_template("upload_audio.html")


@app.route("/uploadUrl", methods=["POST"])
def upload_url():
    url = request.form["youtube-url"]
    fileName = utils.download_audio_from_youtube_url(url)

    if fileName == "too long":
        return jsonify({
            "error": "Requested video is too long (max 20 minutes).",
            "status": 400
        })
    elif fileName == "error":
        return jsonify({
            "error": "An error occured during downloading audio from youtube. Check if url you submitted is valid.",
            "status": 500
        })
    else:
        try:
            audiofile_processed = remove_bass(filePath=DOWNLOAD_FOLDER + fileName)

            # remove downloaded audio, we dont need it anymore
            os.remove(DOWNLOAD_FOLDER + fileName)

            currtime = time.strftime("%Y%m%d-%H%M%S")
            unique_filename = secure_filename(fileName) + currtime + ".wav"
            audiofile_processed.export(PROCESSED_FOLDER + unique_filename, format="wav")

            return jsonify({
                "filename": unique_filename,
                "status": 200
            })
        except Exception as e:
            return jsonify({
                "error": "An error occured during processing. Please try again.",
                "status": 500
            })


@app.route("/uploadAudio", methods=["POST"])
def upload_audio():
    if request.files:
        audiofile = request.files["audiofile"]
        # filename = audiofile.filename

        if not utils.allowed_file(audiofile.filename):
            return jsonify({
                "error": "Unsupported format.",
                "status": 400
            })

        # audiofile.save(UPLOAD_FOLDER + filename)
        # fileSize = os.stat(UPLOAD_FOLDER + filename).st_size
        # os.remove(UPLOAD_FOLDER + filename)
        #
        # if fileSize > MAX_UPLOAD_LIMIT:
        #     return jsonify({
        #         "error": "File is too large.",
        #         "status": 400
        #     })

        try:
            currtime = time.strftime("%Y%m%d-%H%M%S")
            unique_filename = os.path.splitext(secure_filename(audiofile.filename))[0] + currtime + ".wav"

            audiofile_processed = remove_bass(audiofile=audiofile)
            audiofile_processed.export(PROCESSED_FOLDER + unique_filename, format="wav")

            return jsonify({
                "filename": unique_filename,
                "status": 200
            })

        except Exception as e:
            print(e)
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
            try:
                os.remove(PROCESSED_FOLDER + filename)
                return response
            except:
                return response

        return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)
    except:
        return jsonify({
            "error": "There was an error fetching your file.",
            "status": 500
        })


# if __name__ == '__main__':
#    app.run()
