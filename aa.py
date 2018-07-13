import base64
from urllib.parse import quote, unquote
from flask import (Flask, Response, redirect, render_template, request,
                   send_file, session, stream_with_context, url_for)
from htmlmin.minify import html_minify
app=Flask(__name__)

@app.route("/")
def index():
	a="k"
	return a

@app.route("/url-encodings")
def url_enc():
	return render_template("urldecode.html")

@app.route("/base64-test",methods=["POST"])
def try_():
	print(request.form["ye"])
	return "ok"

@app.route("/base64-text-encoder",methods=["POST"])
def enc_text():
	to_encode=request.form["to_encode"]
	data=base64.b64encode(to_encode.encode("ascii")).decode("ascii")
	return data

@app.route("/base64-text-decoder",methods=["POST"])
def b64decode():
	to_decode=request.form["to_decode"]
	data=base64.b64decode(to_decode).decode("ascii")
	return data
	return "TODO:support for image uploads and url uploads"
if __name__=="__main__":
	app.run()