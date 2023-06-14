import cv2
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

#import IPython.display as ipd

webcam = cv2.VideoCapture("C:/Users/simon/Desktop/testing/videoProvaLancio.mp4") #credo sia esterna la webcam (1 esterna, 0 interna)



print("fps:",webcam.get(cv2.CAP_PROP_FPS))#printo gli fps della cam
print("height:",webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))#printo la altezza del frame
print("width:",webcam.get(cv2.CAP_PROP_FRAME_WIDTH))#printo gli fps della cam

def get_immagine():
    while True:
        ret, frame = webcam.read() # legge i dati nella webcam

        if ret == True:
            cv2.imshow("Frame_Name", frame) # setta un frame in cui mostra l'immagine
            key = cv2.waitKey(1) #()tempo in secondi -> aspetto ogni tot secondi che un tasto sia premuto
            labels = pd.read_csv('C:/Users/simon/Desktop/testing/rocket.csv')
            print(labels.head())








            if key == ord("q"): #metodo per cambiare il q a un carattere unicode
                break

def elabora_immagine():
    print("")
    labels = pd.read_csv() #crea file panda
    labels.head()



def mostra_frame():
   # fig, axs = plt.subplot(5,5, figsize=(30,20))
    print("")

def main():
    get_immagine()
    
        

main()
webcam.release()
cv2.destroyAllWindows()
