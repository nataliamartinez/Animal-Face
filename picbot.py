
#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot
from PIL import Image

import StringIO
import urllib2

class PicBot:
	""" 
	Whenever you tweet an image to this bot, 
	it will reply with a processed version of the image 
	"""
	
	def get_image(self, tweet):
		""" Return tweeted image if possible """

		# iterate over all the entities associated with the tweet
		for media in tweet.entities.get("media",[{}]):

			# check if any og them contains a photo
			if media.get("type", None) == "photo":

				# get the url of the photo
				url = media["media_url"]
	    		
	    		# extract the filename
				filename = url.split('/')[-1]

				# download the photo and load it into memory
				fd = urllib2.urlopen(url)
				file = StringIO.StringIO(fd.read())

				# open as PIL image
				image = Image.open(file)
				return image

		# if no image was found return None
		return None


	def on_mention(self, tweet, prefix):
		""" 
		Actions to take when a mention is received.
		"""

		# Try to extract the image file from the tweet
		try:
			image = self.get_image(tweet)
		except Exception as e:
			print(e)
			return

		# call the respective hooks
		if image is None:
			self.on_mention_without_image(tweet, prefix)
		else:
			self.on_mention_with_image(tweet, prefix, image)


	def on_mention_with_image(self, tweet, prefix, image):
		"""
		React to mentions with images
		"""

		# process image, resulting in a new image and a comment
		image, status = self.process_image(image, prefix)

		# filename and format for uplaoding
		filename, format = "result.jpg", "JPEG"

		# write image to a StringIO file
		file = StringIO.StringIO()
		image.save(file, format=format)

		# post tweet
		try:
			self.post_tweet(status[:140], reply_to=tweet, media=filename, file=file)
		except Exception as e:
			print(e)



	def on_process_image(self, img, prefix):
		"""
		Image processing, implement it in your subclass
		"""
		raise NotImplementedError("You need to implement this to tweet to timeline (or pass if you don't want to)!")
        
