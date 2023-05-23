from PIL import Image
import cv2
import numpy as np
import requests
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

cam = cv2.VideoCapture(0)

loops = 0
left = 0
right = 0


while True:
    check, image = cam.read()
    image = cv2.resize(image,(450,250))
    image_arr = np.array(image)

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(grey, (5,5), 0)
    
    #stretches the image outwards
    dilated = cv2.dilate(blur, np.ones((3,3)))

    #creates the kernel shape for the morphEx, this shape is a 2x2 ellipes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    
    #morpholgEx dilates then erodes(expands then shrinks), this is helpful in removing small holes in objects
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    
    car_cascade_src = 'cars.xml'
    car_cascade = cv2.CascadeClassifier(car_cascade_src)
    cars = car_cascade.detectMultiScale(closing, 1.1, 1)

    cnt = 0
    for (x,y,w,h) in cars:
        if x > 225:
            right += 1
        else:
            left += 1
        cv2.rectangle(image_arr, (x,y), (x+w,y+h), (255,0,0), 2)
        cnt += 1
    #print(cnt, " cars found")
    cv2.imshow("cars", image_arr)
    
    loops += 1

    if loops > 100:
        if left > 25:
            print("left on")
            ser.write(b"light,ly\n")
        else:
            print("left off")
            ser.write(b"light,ln\n")
        if right > 25:
            print("right on")
        else:
            print("right off")
        loops = 0
        right = 0
        left = 0
    
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
