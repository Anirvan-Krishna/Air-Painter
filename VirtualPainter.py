import cv2
import handTrackingModule as htm
import numpy as np
import time
import os

###########################

brushThickness = 15
eraserThickness = 50

###########################

# For extracting images from the folder
folderPath = "Header"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []

# Adding the images to overlayList
for imgPath in myList:

    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

#print(len(overlayList))

header = overlayList[0]
drawColor = (255, 0, 255)
#print(header.shape)

# Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = htm.HandDetector(detection_confidence=0.85)
xp, yp = 0, 0


imgCanvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# Displaying the video
while True:
    
    # Import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # Finding Hand Landmarks
    img = detector.find_hands(img)
    lmlist = detector.find_positions(img, draw=False)
    
    if len(lmlist) != 0:
        #print(lmlist)

        # Tip of index and middle fingers
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingers_up()
        # print(fingers)


        # Check which fingers are up
        # if selection mode - 2 fingers up
        if fingers[1] and fingers[2]:
            
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1-30), (x2, y2+30), drawColor, cv2.FILLED)
            #print("selection mode")

            # Checking for the click after entering header
            if y1 < 125:
                if  250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)

                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)

                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)

                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

        
        # If drawing mode: Index finger is up
        elif fingers[1] and fingers[2]==False:
            
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1


            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else: 
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    #Setting the header
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 8)

    cv2.imshow('canvas', imgCanvas) 
    cv2.imshow('img', img)
    cv2.waitKey(1)

