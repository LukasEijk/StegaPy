# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:05:51 2021

@author: bauer
"""

import numpy as np
from PIL import Image

# Programmieren der Funktionen, die für das Verschlüsseln notwendig sind.


def LetzteStelle(txt, neu):#nimmt einen string und setzt an letzte stelle "neu"
    'ersetzt letztes Zeichen vom String mit Zeichen neu '
    testneu = ""
    # for char in range(len(txt)-1):
    #     testneu += txt[char]
    # testneu += neu
    testneu = txt[:-1] + neu
    return testneu


def str2bits(nachricht):
    'Nimmt eine Nachricht und wandelt diese in einen String mit Binär um - erste 64 bit geben länge der nachricht an'
    dummy = [bin(ord(char))[2:].zfill(8) for char in nachricht]
    text = ""
    for entry in dummy:
        text += entry
    laenge = len(text)
    #die ersten 64 bit sind die laenge der nachricht
    blaenge = bin(laenge)[2:].zfill(64)
    return blaenge + text



#speicherort1 
def verschluessel(ort, Zielort, Nachricht):
    'ort, zielort sind speicherort mit dateiendung , Nachricht ist ein str'
    
    #lese datei ein und wandle sie in ein np.array um 
    with Image.open(ort) as img:
        pix = np.array(img)
     
    #ermittle Zeilen und Spaltenanzahl 
    rows = pix.shape[0]
    columns = pix.shape[1]
   
    #zu schreibender Text     
    zuSchreiben = str2bits(Nachricht)
    
    #Greife auf pixel und Farbe zu 
    # pix[row, column][color] 0 = rot, 1 = grün , 2 = blau 
    
    TextBackupBin = zuSchreiben # als Möglichkeit zur überprüfung ob nachricht geschrieben, noch nicht verwendet
    
    
    # schreibe die Nachricht in die Pixel
    #loop solange len(zuSchreiben)>0
    r = 0   #zu loopoende Reihe
    c = 0   # zu loopende Spalte
    veraend = "0" #musste ich so machen, ansonsten wirft es einen fehler bei der umwandlung in int
    akt = "0" #musste ich so machen, ansonsten wirft es einen fehler bei der umwandlung in int
    while zuSchreiben:
        if c <= columns:
            #lese den binärwert des r,c roten pixels aus 
            vorher = bin(pix[r,c][0])[2:].zfill(8)
            if zuSchreiben[0] != vorher[-1]:
                veraend = str(LetzteStelle(vorher, zuSchreiben[0]))
                akt = veraend
            else: akt = veraend
            c += 1
                
        else: #korrigiere Überlauf
            c = 0
            r += 1
            vorher = bin(pix[r,c][0])[2:].zfill(8)
            if zuSchreiben[0] != vorher[-1]:
                #verändere die letzte stelle
                veraend = LetzteStelle(vorher, zuSchreiben[0])
                akt = veraend
            else: 
                akt = vorher
        print(akt)
        umgewandelt = int(akt, 2)  #wandle binär zurück in zahl 
        pix[r,c][0] = umgewandelt # weise neuen farbwert zu         
        c += 1
        zuSchreiben = zuSchreiben[1:] #aktualisiere die zu schreibende nachricht
        
    new_im = Image.fromarray(pix)
    new_im.save(Zielort)
    
    # return new_im


###### Lese Nachricht wieder aus. 
# Die ersten 64 Bits enhalten die Länge der Nachricht

def LaengeNachricht(Ort):
    #lese datei ein und gib aus den ersten 64 roten pixel der Least significant bits die länge der nachricht zurück'
    #meines erachtens hätte ich die ersten 64 bits nur in die erste zeile geschrieben 
    with Image.open(Ort) as img:
        pix = np.array(img)
    
    lastBits = ""
    for i in range(64):
        #liest den int wert vom roten pixel ein als binärzahl ein 
        dummy = bin(pix[0,i][0])[2:].zfill(8)
        # nimmt den letzten bit des pixels 
        lastBits += dummy[-1]
        
    # nimmt die so erstellte Binärzahl und gibt Integer an 
    return int(lastBits, 2)
        



def entschluessel(Ort):
    #ermittle wie lange die nachricht ist
    laengeNachricht = LaengeNachricht(Ort)

    #lese datei ein und wandle sie in ein np.array um 
    with Image.open(Ort) as img:
        pix = np.array(img)
        
    rows = pix.shape[0]
    columns = pix.shape[1]
   

    # Startzeile ab dem die Nachricht beginnt
    #länge der nachricht geht ja von range(0,64) also muss ich von der 6
    c = 64 #wenn 
    r = 0
    
    #Solange die Nachricht nicht komplett ausgelesen ist loope durch
    # hole alle letzten Bits raus 
    erg = ""
    while laengeNachricht:
        if c <= columns:
            #lese den letzten bit des binärwert des r,c roten pixels aus 
            erg += bin(pix[r,c][0])[2:].zfill(8)[-1] 
            
            # gehe in nächste spalte
            c += 1
                
        else: #korrigiere Überlauf
            c = 0
            r += 1   
            erg += bin(pix[r,c][0])[2:].zfill(8)[-1]
            
    # nun muss man aus dem string dem string der alle binärzahlen enthält wieder buchstaben erzeugen 
    
    # erzeuge liste aus gruppe mit jeweils 8 bits 
    ergList = []
    while erg:
        ergList.append(chr(int(erg[:8],2)))
        erg = erg[8:]
    
    # verwende erg wieder um die Nachricht darin zu speichern 
    erg = ""
    
    for entry in ergList:
        erg += entry
    
    return erg
    



