import base64
import os
from urllib.parse import quote, unquote

import requests
from flask import (Flask, Response, redirect, render_template, request,
                   send_file, send_from_directory, session,
                   stream_with_context, url_for)
from htmlmin.minify import html_minify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
app = Flask(__name__)
'''
photo = UploadSet('photo', IMAGES)
photos(app, IMAGES)
'''
app.secret_key = "yeah-k"


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'file' in request.files:
        a = request.files['file']
        mimetype = a.content_type
        data = base64.b64encode(a.read()).decode()
        DATA_URI = "data:"+mimetype+";base64,"+data
        return render_template("base64encodedimage.html", uri=DATA_URI)


def url_of_image(url):
    sess = requests.Session()
    c_len = ""
    ch_url = sess.head(url)
    try:
        c_len = ch_url.headers["content-length"]
        c_type = ch_url.headers['content-type']
        if int(c_len) >= 25000000:
            return "File too large!"
    except:
        return "unknown error"
    final_url = ch_url.url
    final_url = url
    data = base64.b64encode(requests.get(final_url).content).decode("ascii")
    DATA_URI = "data:"+c_type+";base64,"+data
    return DATA_URI


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/url-encodings")
def url_enc():
    return render_template("urldecode.html")


@app.route("/base64-text/")
def b64_main():
    return render_template("base64text.html")


@app.route("/base64-text-encoder", methods=["POST"])
def enc_text():
    to_encode = request.form["to_encode"]
    data = base64.b64encode(to_encode.encode("ascii")).decode("ascii")
    return data


@app.route("/base64-text-decoder", methods=["POST"])
def b64decode():
    to_decode = request.form["to_decode"]
    try:
        data = base64.b64decode(to_decode)
    except:
        try:
            data = base64.b64decode(to_decode+"=")
        except:
            return "incorrect padding on the string"
    return data


@app.route("/base64-image/")
def b64_img_main():
    return render_template("base64image.html")


@app.route("/base64-image-encoder", methods=["POST"])
def b64img():
    data = request.form["type"]
    if data == "url":
        b64_ = url_of_image(request.form["to_encode"])
        return b64_

    return "TODO:support for image uploads and url uploads"


@app.before_request
def https():
    if request.endpoint in app.view_functions and not request.is_secure and not "127.0.0.1" in request.url and not "localhost" in request.url and not "192.168." in request.url:
        if "herokuapp" in request.url:
            return redirect(request.url.replace("http://", "https://"), code=301)


@app.route("/base64-image-decoder", methods=["POST"])
def b64dec():
    b64data = request.form['b64text']
    headers = Headers()
    filen = "file."+request.form['usr_ext']
    headers.add("Content-Disposition", "attachment", filename=filen)
    try:
        data = b64data.split(";base64,")[1]
    except:
        # Support for uris in this type"data:[mimetype];base64,<stuff>
        data = b64data
    try:
        rtd = base64.b64decode(data)
    except:
        try:
            data = base64.b64decode(data+"=")
        except:
            return "incorrect padding on the string"
    return Response(rtd, headers=headers, content_type='application/octet-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
