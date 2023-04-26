from PIL import Image
import pytesseract
import cv2
import imutils
import os, sys, inspect #For dynamic filepaths
import numpy as np;	
import re
import time
import Comm

timeEntered = 0
cam = cv2.VideoCapture(0)

carsList = []
class carInPark:
    def __init__(self, licensePlate, timeEntered, isACT):
        self.licensePlate = licensePlate
        self.timeEntered = timeEntered
        self.isACT = isACT
    
 
def killCar(licensePlate):
    for car in carsList:
        if (car.licensePlate == licensePlate):
            print("killed: " + licensePlate)
            print(car.isACT)
            carsList.remove(car)
            Comm.getPayment(16.50)

def predominantColour(img):
    a2D = img.reshape(-1, img.shape[-1])
    col_range = (256,256,256)
    a1D = np.ravel_multi_index(a2D.T, col_range)
    colours = np.unravel_index(np.bincount(a1D).argmax(), col_range)
    if (colours[0] + colours[1] + colours[2] < 600):
        return False
    return True

while True:
    check, frame = cam.read()

    img = cv2.resize(frame,(320,240))
    
    imgNew = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_empty = np.zeros((img.shape[0], img.shape[1]))
    img2 = cv2.normalize(imgNew, img_empty, 0, 255, cv2.NORM_MINMAX)
    
    #img3 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY)[1]
    #img4 = cv2.GaussianBlur(img3, (1, 1), 0)
    
    edges = cv2.Canny(img2,30,200)
    cnts,newCnts = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cntsImageCopy = img2.copy()
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:40]
    screenCnt = None
    cv2.drawContours(cntsImageCopy, cnts, -1, (0, 255, 0), 3)

    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) != 4:
            continue   
        screenCnt = approx
        x,y,w,h = cv2.boundingRect(c)
        
        if w < 30:
            continue
        cropped = img2[y:y+h,x:x+w]
   
        cropped3 = cv2.threshold(cropped, 120, 255, cv2.THRESH_BINARY)[1]
        cropped4 = cv2.GaussianBlur(cropped3, (1, 1), 0)
        
        cv2.imshow("threshold", cropped3)
        cv2.imshow("Blurred", cropped4)

        text = pytesseract.image_to_string(cropped4)
        text = re.sub("[^A-Za-z0-9]","",text)
        text = re.sub("o","0",text)
        if len(text) != 6:
            continue
        cv2.imshow("cropped", cropped)
        print(text)

        colourCropped = img[y:y+h,x:x+w]
        cv2.imshow("colour",colourCropped)
        if (x < 160):
            print("exit")
            killCar(text)
        elif (time.time() - timeEntered > 5):
            print("entered")
            newCar = carInPark(text, time.time(), predominantColour(colourCropped))
            carsList.append(newCar)
            timeEntered = time.time()


    # Output
    #cv2.imshow("Threshold", img3)
    #cv2.imshow("Blurred", img4)
    cv2.imshow("Edges", edges)
    cv2.imshow("Contours", cntsImageCopy)
    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break
    

cam.release()
cv2.destroyAllWindows()
