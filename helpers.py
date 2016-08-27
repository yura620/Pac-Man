import pygame
from pygame.locals import *


def load_image(fullname, colorkey=None):
	try:
		image = pygame.image.load(fullname)
	except pygame.error:  # , message):
		print('Cannot load image:', fullname)
		# raise (SystemExit, message)

	image = image.convert()							# change the pixel format of an image

	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0, 0))			# get the color value at a single pixel
		image.set_colorkey(colorkey, RLEACCEL)		# Set the transparent colorkey

	return image, image.get_rect()
