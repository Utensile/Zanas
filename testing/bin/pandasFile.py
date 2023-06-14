import numpy as np
import pandas as pd



##CREAZIONE DI SERIE DI DATI
#---------------------------------------------------
mydata = ['Boat', 'Car', 'Bike','Truck'] #valori di prova, prima si prova cosi, poi lo adatto
myseries1 = pd.Series(mydata) #creo la prima serie
#print (myseries1)

print("--------------------")

mydata = [1, 50, 166, 255]
myseries2 = pd.Series(mydata)
#print (myseries2)

print("--------------------")

#---------------------------------------------------
##CREAZIONE DI UN DATAFRAME -> serie associate con uno stesso index, ogni colonna ha un oggetto(proprio dello serie-->quindi se serie uno ha come oggetto int anche la colonna ha come oggetto int)
#---------------------------------------------------
mydfdata = [('Boat',1), ('Car', 50), ('Bike', 166),('Truck', 255)] #dati del dataFrame
#mydf = pd.DataFrame(mydfdata, columns=['cose', 'numeri']) #do al dataframe i dati, secondo parametro utile per dare nomi a colonne
mydf = pd.DataFrame(mydfdata) 
mydfdata2 = ['Fdsaf', 1225]
mydf.loc[len(mydf.index)] = mydfdata2
#print(mydf) -> intero dataframe
#print(mydf['cose']) -> solo una colonna
#print(mydf.dtypes) #->tutti i tipi delle colonne

print(mydf)