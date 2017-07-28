import logging

from flask import Flask, render_template, request, jsonify

import faces

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file_to_check = request.files['file']
        try:
            face_count = faces.detect_face(file_to_check.stream.read())
            print "upload: ok, faces: " + str(len(face_count))
            return jsonify(
                {
                "Upload/processing/success": True,
                 "Faces": len(face_count)
                 })
        except Exception as e:
            logging.exception(e)
            return jsonify({"Upload/processing/success": False})


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run()
