import RPi.GPIO as GPIO

def getButton():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)	
	symbol = ""
	while True:
		if(GPIO.input(23) == 1):
			symbol="23"
			break
		if(GPIO.input(24) == 0):
			symbol="24"
			break
	GPIO.cleanup()
	return symbol