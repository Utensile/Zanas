import cv2
import matplotlib.pyplot as plt
import numpy as np

def scalaImmagine(img):
    print('Original Dimensions:', img.shape)
    scale_percent = 20  # percent of original size
    width = 280
    height = 280
    dim = (width, height)
    # resize image
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img

def convertImage(img):
    result = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

   # lower_black = np.array([0, 0, 0])
   # high_black = np.array([70, 70, 70])
    lower_maincolor = np.array([0, 0, 0])
    upper_maincolor = np.array([50, 50, 50])

    mask = cv2.inRange(hsv, lower_maincolor, upper_maincolor)
   # mask2 = cv2.inRange(hsv, lower_black, high_black)

    result[mask != 0] = (0, 0, 0)

    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, img_m = cv2.threshold(result, 10, 255, cv2.THRESH_BINARY_INV)
    return img_m

def contorni(img_m, img):

    cv2.imshow("img_,", img_m)
    _, contours, _ = cv2.findContours(img_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    items = sorted(contours, key=cv2.contourArea, reverse=True)
    
    item = items[0]
    x, y, w, h = cv2.boundingRect(item)
    cX = int((x + (x + w)) / 2)
    cY = int((y + (y + h)) / 2)

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(img, (cX, cY), 5, (255, 255, 0), -1)
    cv2.putText(img, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    cv2.imshow("Resized image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_center(img):
    img_m = convertImage(img)
    contorni(img_m, img)

def main(img):
    img = scalaImmagine(img)
    get_center(img)

vid = cv2.VideoCapture("videoProvaLancio.mp4")

if not vid.isOpened():
    print("ERROR")

while True:
    ret, frame = vid.read()

    if not ret:
        break

    frame_resized = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
    h = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    main(frame)

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()
