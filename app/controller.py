import sqlite3 as sql
from werkzeug.utils import secure_filename
from model import *


conn = sql.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS Vault (rank_id INTEGER PRIMARY KEY AUTOINCREMENT, words TEXT, representation TEXT)')
cur =  conn.cursor()
conn.close()

def ncode_nputs():
	sil = request.files['sil']
	nputs = request.form['inputs']
	sil.save(secure_filename(sil.filename))
	silwet = sil.filename
	return nputs,silwet

def dcode_nputs():
	image = request.files['image']
	image.save(secure_filename(image.filename))
	filename = image.filename
	print filename
	return filename
