import cv2
import matplotlib.pyplot as plt

'''
image = cv2.imread('immagineProva4.jpeg')
original_image= image

gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)

cv2.imshow("Canny", edges)

contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)


#dividi contorni
smallest_item= sorted_contours[0]





#largest item
'''
'''
M = cv2.moments(largest_item)

print(M)


x,y,w,h= cv2.boundingRect(largest_item)


xcoordinate1= x 

xcoordinate2= x + w

xcoordinate_center= int(M['m10']/M['m00'])


print("Larger Box")

print("x coordinate 1: ", str(xcoordinate1))

print("x coordinate 2: ", str(xcoordinate2))

print("x center coordinate ", str(xcoordinate_center))

print("")


ycoordinate1= y 

ycoordinate2= y + h

ycoordinate_center = int(M['m01']/M['m00'])



print("y coordinate 1: ", str(ycoordinate1))

print("y coordinate 2: ", str(ycoordinate2))

print("y center coordinate ", str(ycoordinate_center))


print("")

#smallest item
M2= cv2.moments(smallest_item)

x2,y2,w2,h2= cv2.boundingRect(smallest_item)


x2coordinate1= x2 

x2coordinate2= x2 + w2

x2coordinate_center= int(M2['m10']/M2['m00'])


print ("Smaller Box")

print("x coordinate 1: ", str(x2coordinate1))

print("x coordinate 2: ", str(x2coordinate2))

print("x center coordinate ", str(x2coordinate_center))

print ("")


y2coordinate1= y2 

y2coordinate2= y2 + h2

y2coordinate_center= int(M2['m01']/M2['m00'])

'''
'''
img = cv2.imread('left.jpg')

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
# convert the grayscale image to binary image
ret,thresh = cv2.threshold(gray_image,127,255,0)
 
# calculate moments of binary image
M = cv2.moments(thresh)
 
# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
 
# put text and highlight the center
cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
# display the image
cv2.imshow("Image", img)
cv2.waitKey(0)
'''
'''
print("y coordinate 1: ", str(y2coordinate1))

print("y coordinate 2: ", str(y2coordinate2))

print("y center coordinate ", str(y2coordinate_center)
'''
'''
print(M)

plt.imshow(image)
plt.show()
'''
import numpy as np
img =  cv2.imread('ImmagineProva3.png') #apro l'immagine
img = cv2.resize(img, (0,0), fx= 0.2, fy=0.2)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #la converto in rgb
        
        # Threshold of blue in HSV space
lower_blue = np.array([0, 0, 0])
upper_blue = np.array([255, 255, 255])
        # preparing the mask to overlay
mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions
result = cv2.bitwise_and(img, img, mask = mask)


#DA ELIMINARE PER SORTARE L'ELEMENTO

result= cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)





 #resize per non esplodere

cv2.imshow("Result: ", result)

img_c = cv2.Canny(result, 50,200)
#cv2.imshow("Canny: ", img_c)


contours, hierarchy= cv2.findContours(img_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = np.vstack(contours)
#cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
print("Number of Contours found = " + str(len(contours)))
cv2.imshow("Contorni: ", img)

min = 10000
max = 0

index = -1 #per trovare la posizione del vettore parti da -1 perchè se no il primo viene contato


for cnt in contours:
    area = cv2.contourArea(cnt)
    #print (area)
    if area < min:
        min = area
    if area > max:
        max = area
        index += 1
        cv2.drawContours(img, [cnt], -1, (255, 0, 0), 2)
    
#
items = sorted(contours, key=cv2.contourArea, reverse= False) #sorting degli elementi


print(index)
item = items[len(items)-1]
M = cv2.moments(item)
x2,y2,w2,h2= cv2.boundingRect(item)


x2coordinate1= x2 

x2coordinate2= x2 + w2

cX = int((x2+(x2+w2))/2)
cY = int((y2+(y2+h2))/2)
cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0, 255), 2)


print(M)

plt.imshow(img)
plt.show()
#cv2.imshow("conversion: ", img)
