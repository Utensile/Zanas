import cv2
import matplotlib.pyplot as plt

img = cv2.imread('ImmagineProva5.jpeg',0)

img = cv2.resize(img, (240,240))
ret,thresh = cv2.threshold(img,127,255,0)
#im = cv2.Canny(thresh, 200, 250)

#cv2.imshow(" ",im)
cv2.waitKey(0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

min = 10000
ma = 0
areas = []
index = 101

#inutile, con sort me li mette dal piu piccolo al piu grande

for cnt in contours:
    area = cv2.contourArea(cnt)
    #print (area)
    if area < min:
        min = area
    if area > ma:
        ma = area
    areas.append(area)
    #cv2.drawContours(img, cnt, -1, (255, 0, 0), 2)

print("max: ", ma)


 

#index = areas.index(ma)

items = sorted(contours, key=cv2.contourArea, reverse= False)






cnt = items[len(items)-1]

for j in range(len(areas)):
    print(j, ":", areas[j])


print("--------")

hull = cv2.convexHull(cnt)
x, y, w, h = cv2.boundingRect(hull)

cx=((x+(x+w))/2)
cy=((y+(y+h))/2)

cv2.drawContours(img, cnt, -1, (255, 0, 0), 2)

print("x:",cx," y", cy)
#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow(" ",img)
plt.imshow(img)
plt.show()

