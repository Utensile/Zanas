from PIL import Image
import numpy as np
import sys
import os
import csv
import pandas as pd
# default format can be changed as needed
def createFileList(myDir, format='.jpeg'):
    fileList = []
    print(myDir)
    labels = []
    names = []
    keywords = {"T" : "2",} # keys and values to be changed as needed

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
myFileList, labels, names  = createFileList('C:/Users/simon/Desktop/testing/merged')



i = 0

value = []
df = pd.DataFrame([],columns=["Labels", "pixels"])

for file in myFileList:
    print(file)
    img_file = Image.open(file)
    #img_file.show()
# get original image parameters...
    width, height = img_file.size
    format = img_file.format
    mode = img_file.mode
# Make image Greyscale
    img_grey = img_file.convert('L')
    pix = img_grey.load()
    #img_grey.save('result.png')
    #img_grey.show()
# Save Greyscale values

    for w in range(width):
        for h in range(height):
            value.append(pix[w,h])
                #writer.writerow(value)
         
    #value = np.asarray(img_grey.getdata(), dtype=np.int64).reshape((width, height))
    #print(value.ctypes)
    #value = np.append(value)
    s = ""
    for g in value:
        s+=str(g)+" "

    df.loc[len(df.index)] = labels[i],s
    i +=1

   
    #with open("rocket.csv", 'a') as f:
     #   writer = csv.writer(f)
      #  writer.writerow(value)
print(df)
df.to_csv("rocket.csv", index=False)
