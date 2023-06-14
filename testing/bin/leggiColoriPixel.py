
from PIL import Image


x = 0
y = 0
COLORE = (255,0,0,255)
im = Image.open('ImmagineProva3.png') # Can be many different formats.



w, h = im.size# Get the width and hight of the image for iterating over
#print (pix[x,y] ) # Get the RGBA Value of the a pixel of an image
#pix[x,y] = COLORE  # Set the RGBA Value of the image (tuple)
#im.save('alive_parrot.png')
pix = im.load()


im = im.convert("RGBA")
pix = im.load()
print(pix[x,y])


def elabora_foto(img):
    global x,y,COLORE
    print ("w: ",w,"h: ", h)
    for i in range(w):
        for j in range(h):
            r,g,b,a = pix[i,j]

            #rgba(153,118,18,255)
            if(60 <= r <= 250 and 80 <= g <= 250 and 0 <= b <= 60 and a == 255):
                cambia_colore(i, j)


def cambia_colore(i : int, j: int):
    pix[i,j] = COLORE 

def main():

    elabora_foto()
    im.save('alive_parrot2.png')


main()

