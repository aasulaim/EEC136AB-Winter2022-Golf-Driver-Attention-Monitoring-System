"""
Demonstration of the GazeTracking library
"""

import cv2
from gaze_tracking import GazeTracking
import Jetson.GPIO as GPIO
import time


gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

inputPin2 = 16
inputPin3 = 18
outputPin = 23
outputPin2 = 24
outputPin3 = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inputPin2, GPIO.IN) 
GPIO.setup(inputPin3, GPIO.IN)
GPIO.setup(outputPin, GPIO.OUT)
GPIO.setup(outputPin2, GPIO.OUT)
GPIO.setup(outputPin3, GPIO.OUT)

count = 0
a = 1
b = 1
c = 1
d = 13
looking = 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        	break
        	
    y = GPIO.input(inputPin2)
    z = GPIO.input(inputPin3)

    GPIO.output(outputPin,a)
    GPIO.output(outputPin2,b)
    GPIO.output(outputPin3,c)

    count = count + 1
    
    if text == "Looking center" or text == "Looking left" or text == "Looking right":
    	looking = 1
    else: 
    	looking = 0
	
    if looking == 1 and count < 3*d:
    	print("Driver is looking")
    	count = 0
    	a = 1
    	b = 1
    	c = 1	
	
    elif looking == 0 and count == 3*d:	
    	a = 0
    	print("")
    	print("LED 1 ON")
    	print("WARNING")
    	print("")

    elif looking == 1 and count < 6*d:	
		
    	a = 1
    	print("LED 1 OFF")
    	print("Driver is looking")
    	print("")
    	count = 0
	
    elif looking == 0 and count == 6*d:
		
    	a = 0
    	b = 0
    	print("LEDs 1 AND 2 are ON")
    	print("STRIKE 1")
    	print("")
	
    elif looking == 1  and count < 9*d:
    	count = count - 1
    	if y == 0:
    		a = 1	
    		b = 1
    		print("LEDs 1 AND 2 are OFF")
    		print("Driver is looking")
    		print("")
    		count = 0

    elif looking == 0 and count == 9*d:
		
    	a = 0
    	b = 0
    	c = 0
    	print("LEDs 1, 2, 3 are ON")
    	print("STRIKE 2")
    	print("")

	
    elif looking == 1 and count < 12*d:
    	count = count - 1
    	if y == 0:
    		a = 1	
    		b = 1
    		c = 1
    		print("LEDs 1, 2, 3 are OFF")
    		print("Driver is looking")
    		print("")
    		count = 0

		
    elif looking == 0 and count == 12*d:
    	a = 1
    	b = 1
    	c = 1
    	print("LEDs OFF")
    	print("STRIKE 3! Restart System")
    	print("")
    	
    elif looking == 1 and count > 12*d and z == 0:
    	count = 0;
    	print("SYSTEM RESTART")
   
GPIO.cleanup()
webcam.release()
cv2.destroyAllWindows()
