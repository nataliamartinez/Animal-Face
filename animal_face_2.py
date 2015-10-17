#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot
from picbot import PicBot
from PIL import Image, ImageDraw, ImageFont
from sys import argv

import os
import random
import numpy
import cv2

import keys


classifier = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(classifier)


def face_detect(image):
	"""
	Return rectangles of identified face regions
	"""

	# numpy grayscale image for face detection
	array = numpy.asarray(image)
	gray_image = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)

	# tweak this for better results ..

	faces = faceCascade.detectMultiScale(
    	gray_image,
    	scaleFactor=1.1,
    	minNeighbors= 5,
    	minSize=(25, 25),
    	flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	# convert boxes from arrays to tuples
	boxes = [(x, y, x + w, y + h) for (x, y, w, h) in faces]
	return boxes


def animals(image):
	""" 
	Paste animal faces on human faces :)!
	"""

	# work on a copy
	image = image.copy()
	
	# identify boxes
	boxes = face_detect(image)

	
	# grabing random files of img from the folder of animals_faces	
	directory = os.path.join(os.path.dirname(__file__), "animal_faces")
	#print directory


	# esto era lo q tenia antes --- directory = './animal_faces/'
	directory_list = os.listdir(directory)
	directory_list.remove('.DS_Store')

	# for item in directory_list:
	# 	print (item)

	# print the first  quote from the file and print it 
	# text_file = open('quotes.txt', 'r')
	# quote = text_file.readline()
	# print quote


	#print a random quote from the file
	quote = random.choice(list(open('quotes.txt')))
	#print quote

	# use a display font 35 bit
	font = ImageFont.truetype("SigmarOne.ttf",35)
	# draw quote on pic	
	draw = ImageDraw.Draw(image)

	# draw black version of the quote- like a shadow
	draw.text((150, 100), quote ,(0,0,0),font=font)

	#draw a white version of the quote
	draw.text((145, 95), quote ,(255,255,255),font=font)

	draw = ImageDraw.Draw(image)

	#img.show()


	# draw boxes
	for box in boxes:
		#print(box)

		# get the coordinates for the box
		x1, y1, x2, y2 = box

		# taking a random choice from the list created before
		one_animal = random.choice(directory_list)
		# adding the name of the file on the rute so it can be opend later...
		imgfile = os.path.join(directory, one_animal)

		# open the cat img on the boxes
		cat = Image.open(imgfile)

		#resize the img of the cat
		cat = cat.resize(((x2-x1)* 2 , (y2-y1)*2), resample=Image.BICUBIC)
		
		# change the referense point from the upper left corner to half of it (center)
		dx = (x2-x1)/2
		dy = (y2-y1)/2

		# paste the cat into the original image with the faces
		image.paste(cat, (x1 - dx, y1 - dy), cat)

	return image, boxes




#---def quote(image):
	""" 
	Writes a random quote from a file ontop of the img with the animal faces!

	"""
	#text_file = open('quotes.txt', 'r')
	#quote = text_file.readline()
	#print quote

	#return image




if __name__ == '__main__':

	print("Loading source image")
	src = Image.open("Tpjc_Soccer_Team.jpg")
	#src.show()

	print("Testing face animal")
	img, boxes = animals(src)
	img.show()

	#print ("Testing quote")
	#img



