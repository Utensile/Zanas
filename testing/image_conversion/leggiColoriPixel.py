
from PIL import Image
import pandas as pd
import numpy as np
import os

df = pd.DataFrame([], columns=["Rocket_Type","Image_Path","Yellow_Percentage", "Black_Percentage", "White_Percentage" ])

counter = 0
#im = Image.open('C:/Users/simon/Desktop/testing/image_conversion/ImmagineProva6.jpeg')
pg = 0
pb = 0
pw = 0
npx_tot = 0
w = 0
h = 0

COLORE = (255,0,0,255)
#im = Image.open('C:/Users/simon/Desktop/testing/image_conversion/ImmagineProva6.jpeg') # Can be many different formats.

def carica_immagine(path: str):
    global pg, pb, pw, npx_tot, w, h

    im = Image.open(path) # Can be many different formats.
    w, h = im.size# Get the width and hight of the image for iterating over
    #print (pix[x,y] ) # Get the RGBA Value of the a pixel of an image
    #pix[x,y] = COLORE  # Set the RGBA Value of the image (tuple)
    #im.save('alive_parrot.png')
    pg = 0
    pb = 0
    pw = 0
    npx_tot = 0
    im = im.convert("RGBA")
    pix = im.load()

    elabora_foto(pix, w, h, im)



def createFileList(myDir, format='.jpeg'):
    fileList = []
    print(myDir)
    labels = []
    names = []
    keywords = {"T" : "Zthree", "k":"Kenue", "O": "One"} # ["Lettera iniziale della cartella":"cosa verra scritto nel file csv"]

    for root, dirs, files in os.walk(myDir, topdown=True):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
            for keyword in keywords:
                if keyword in name:
                    labels.append(keywords[keyword])
                else:
                    continue
            names.append(name)
    #print(labels)
    return fileList, labels, names
# load the original image





def elabora_foto(pix, w : int, h:int, im):
    global  npx_tot, pg, pw, pb
    #print ("w: ",w,"h: ", h)
    for i in range(w):
        for j in range(h):
            r,g,b,a = pix[i,j]
            npx_tot += 1
            #rgba(153,118,18,255)
            if(60 <= r <= 250 and 80 <= g <= 250 and 0 <= b <= 60 and a == 255):
                pg += 1
                cambia_colore(i, j, pix, (255, 0,0, 255))  
                
            elif(0 <= r <= 50 and 0 <= g <= 50 and 0 <= b <= 50 and a == 255):
                pb += 1
                cambia_colore(i, j, pix, (0, 255,0, 255))  
            elif(210 <= r <= 255 and 210 <= g <= 255 and 210 <= b <= 255 and a == 255):
                pw += 1
                cambia_colore(i, j, pix, (0, 0,255, 255))  

    salva_foto(im)
    determina_abbondanza_percentuale()

                




def determina_abbondanza_percentuale():
    global pg, pb, pw, npx_tot
    
    #print("numero di pixel gialli:", pg)
    #print("in percentuale: ", pg/npx_tot*100)
    pg = pg/npx_tot*100
    
    
    #print("numero di pixel neri:", pb)
    #print("in percentuale: ", pb/npx_tot*100)
    pb = pb/npx_tot*100
    
    #print("numero di pixel bianchi:", pw) 
    #print("in percentuale: ", pw/npx_tot*100)
    pw = pw/npx_tot*100
    

def salva_foto(im):
    global counter
    s = "C:/Users/simon/Desktop/testing/result/elaborato"+str(counter)+".png"
    #print(counter)
    im.save(s)


def cambia_colore(i : int, j: int, pix, color):
    pix[i,j] = color


def main():
    global counter, pg, pb, pw
    
    myFileList, labels, names  = createFileList('C:/Users/simon/Desktop/testing/merged')
    i = 0
    
    for file in myFileList:
        print(file)
        counter+=1
        carica_immagine(file)
        print(labels[i])
        '''
        #  SCOMMENTA QUESTA PARTE PER LA VISUALIZZAZIONE DI DATI IN EXCELL
        pg = str(pg)
        pg = pg.replace(".","P")
        pb = str(pb)
        pb = pb.replace(".","P")
        pw = str(pw)
        pw = pw.replace(".","P")
        '''
        value_list = [labels[i], file , pg, pb, pw]
        df.loc[len(df.index)] =  value_list
        i+=1







main()

print(df)
df.to_csv("C:/Users/simon/Desktop/testing/result/rocket.csv", index=False)