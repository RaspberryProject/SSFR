import pygame
import pygame.camera
import zbar
import Image

from pygame.locals import *


def saveWebcamImage():
	pygame.init()
	pygame.camera.init()

	cam = pygame.camera.Camera("/dev/video0",(640,480))
	cam.start()

	image = cam.get_image()

	pygame.image.save(image, 'webcam.jpg')

	cam.stop()

	return True

def readBarcode():
	saveWebcamImage()

	scanner = zbar.ImageScanner()
	pil = Image.open("webcam.jpg").convert('L')
	width, height = pil.size

	raw = pil.tostring()

	image = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(image)

	symbol_data = ""
	for symbol in image:
		symbol_data = symbol.data
		break
	return symbol_data
