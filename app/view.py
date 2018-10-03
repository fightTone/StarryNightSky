from flask import Flask, render_template, request
from controller import *
from model import *

import sqlite3 as sql

app = Flask(__name__, static_url_path = "", static_folder = "tmp")


@app.route('/', methods = ['POST', 'GET'])
def encode():
	if (request.method == "GET"):
		return render_template("incode_input.html")
	elif(request.method == "POST"):
		nputs,silwet = ncode_nputs()
		
		ncode(nputs,silwet)
		whole_reps = []
		return render_template("decode_input.html")

@app.route('/decode', methods = ['POST', 'GET'])
def decode():
	if(request.method == "GET"):
		return render_template("decode_input.html")
	elif(request.method == "POST"):
		dputs = dcode_nputs()
		msg = dcode(dputs)
		return render_template("decode_output.html", msg = msg)

