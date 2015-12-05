#-*- coding: utf-8 -*-
__author__ = 'KucVN'
try:
	import Image
except ImportError:
	from PIL import Image
import pytesseract
import glob
import os

class MyOCR(object):

	def __init__(self, img_path):
		self.img_path = img_path

	def get_filename(self):
		return self.img_path.split('\\')[-1].split('.')[0]

	def get_path(self):
		return os.path.dirname(self.img_path)

	def to_txt(self):
		return pytesseract.image_to_string(Image.open(self.img_path), config='-l ttn')
		#return pytesseract.image_to_string(Image.open(img_path), config=('tessedit_char_whitelist','0123456789'))


if __name__ == '__main__':
	mfiles = glob.glob(os.path.join('..', '..', '..', 'tmp', '*.gif'))
	for mfile in mfiles:
		#im = Image.open(mfile)
		#im.save()
		#mtxt = MyOCR(mfile)
		#print mtxt.to_txt()
		#print mtxt.get_filename()
		#print mtxt.get_path()
		MyOCR(mfile).to_txt()
