from view import *
from controller import *
import cv2
import numpy as np
import random
from pprint import pprint

shapes = ['Circle', 'Circle', 'Circle']
whole_reps = []
salts = []
whitepix = []

def whitex(silwet):
	print silwet
	img = cv2.imread(silwet,0)

	rows = img.shape[0]
	cols = img.shape[1]

	for i in range(0,rows):
		for j in range(0,cols):
			if img[i,j] == 255:
				whitepix.append((j,i))
				img[i,j] = 0
			else:
				img[i,j] = 0

	cv2.imwrite("44.jpg",img)


def drawing(aray_naku,last):
	img = cv2.imread('44.jpg')
	for draw in whole_reps:
		coords = draw[0]
		shp = draw[1]
		size = draw[2]
		color = draw[3]
		if draw[1] == "Square":
			cv2.rectangle(img,coords,(coords[0]-size-5,coords[1]-size-5),color,-1)
			whole_reps.remove(draw)
			# cv2.imshow("image",img)
			# cv2.waitKey(1)
		elif draw[1] == "Circle":
			img[coords[1],coords[0]] = color
			# cv2.imshow("image",img)
			# cv2.waitKey(1)
		elif draw[1] == "Triangle":
			c = coords[0]
			b = coords[1]
			d=c+size
			e = b+size
			t2 = size * 2
			pts = np.array([[c,b],[d,e],[d-t2,e]], np.int32)
			pts = pts.reshape((-1,1,2))
			cv2.polylines(img,[pts],True,color,2)
			whole_reps.remove(draw)
			# cv2.imshow("image",img)
			# cv2.waitKey(1)
		# cv2.imwrite("44.jpg",img)
		# cv2.imwrite("copy-44.jpg",img)
	# cv2.imwrite("44.jpg",img)
	cv2.imwrite("store"+str(last)+".jpg",img)
	cv2.imwrite("copy"+str(last)+".jpg",img)



def rands(i,char):
	char_reps = []	
	B = random.randint(0, 255)
	G = random.randint(0, 255)
	R = random.randint(0, 255)

	repshape = random.choice(shapes)
	res=random.choice(whitepix)
	rx = res[0]
	ry = res[1]
	size = 9

		

	char_reps = [(rx,ry),repshape,size,(B,G,R),i]

	if char_reps in whole_reps:
		print "huli ka"
		rands()
	else:
		return char_reps

def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())


def ncode(nputs,silwet):
	whitex(silwet)



	i=0
	for char in nputs:
		char_reps = rands(i,char)
		whole_reps.append(char_reps)
		i+=1

	salt_num = 0
	x=-1
	xx='--1'
	while(salt_num < 10000):
		salt_rep = rands(x,xx)
		whole_reps.append(salt_rep)
		salt_num+=1

	

	# drawing(salts,last)
	repres = str(whole_reps)
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO Vault(words, representation) VALUES(?,?)",(nputs,repres,))
	last = cur.lastrowid
	con.commit()
	con.close()

	drawing(whole_reps,last)

	orig = cv2.imread(silwet,0)
	cv2.imshow("orig",orig)
	img = cv2.imread('store'+str(last)+".jpg")
	cv2.imshow("image",img)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def dcode(dputs):
	conn = sql.connect('database.db')
	cur = conn.cursor()
	cur.execute("SELECT rank_id FROM Vault")
	rows = cur.fetchall()
	for row in rows:
		print str(row[0])+".jpg"

		image1 = img = cv2.imread("store"+str(row[0])+".jpg")
		image2 = img = cv2.imread(dputs)

		res=is_similar(image1,image2)

		print res
		decoded = ""
		if(res):
			conn = sql.connect('database.db')
			cur = conn.cursor()
			cur.execute("SELECT * FROM Vault WHERE rank_id = ?",(row[0],))
			decoded = cur.fetchone()[1]
			
			break
		else:
			decoded = "Cannot interpret this image"
	return decoded