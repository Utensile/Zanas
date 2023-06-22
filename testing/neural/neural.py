import cv2
import matplotlib.pyplot as plt
import numpy as np

 
img = cv2.imread('ImmagineProva3.png')


def scalaImmagine():
    print('Original Dimensions : ',img.shape)
     
    global img3
    scale_percent = 20 # percent of original size
    width = 280
    height = 280
    dim = (width, height)
      
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
     
    print('Resized Dimensions : ',resized.shape)
     
    cv2.imshow("Resized image", resized)
    cv2.waitKey(0)

    plt.imshow(resized)
    plt.show()
    cv2.destroyAllWindows()

def init_neur():

    neurons = []
    cols = 3
    rows = 3


    for r in range(rows):
        neurons.append([0]*cols)


    print("nuron",neurons)



def main():
    scalaImmagine()
    init_neur()


def get_center():
    
    

main()
