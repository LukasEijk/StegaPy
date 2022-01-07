# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:05:51 2021

@author: bauer & johannes (korrektur)
"""

import numpy as np
from PIL import Image
import tkinter
from tkinter import filedialog
import os


# Programmieren der Funktionen, die für das Verschlüsseln notwendig sind.


def LetzteStelle(txt, neu):#nimmt einen string und setzt an letzte stelle "neu"
    'ersetzt letztes Zeichen vom String mit Zeichen neu '
    testneu = ""
    # for char in range(len(txt)-1):
    #     testneu += txt[char]
    # testneu += neu
    testneu = txt[:-1] + neu
    return testneu

def jpg2png(ort):
    ziel = ort[:-3]+ r"png"
    im1 = Image.open(ort)
    im1.save(ziel)
    return ziel

def str2bits(nachricht):
    'Nimmt eine Nachricht und wandelt diese in einen String mit Binär um - erste 64 bit geben länge der nachricht an'
    dummy = [bin(ord(char))[2:].zfill(8) for char in nachricht if ord(char) <= 255]
    text = "".join(dummy)
    laenge = len(text)
    #die ersten 64 bit sind die laenge der nachricht
    blaenge = bin(laenge)[2:].zfill(64)
    return blaenge + text



#speicherort1 
def verschluessel(Nachricht):
    'ort, zielort sind speicherort mit dateiendung , Nachricht ist ein str'
    
    # verwende tkinter um die datei einfach auszuwählen 
    root = tkinter.Tk()

    def close_win():
       root.destroy()
    
    # erstelle close button 
    button = tkinter.Button(root, text= "Close", font=('Poppins bold', 16),
    command=close_win).pack(pady=20)
    files = filedialog.askopenfilenames(parent = root,
                                        title = "Wähl ein Bild aus",
                                        filetypes=[("Bild-Dateien", ".png")] )

    # files gibt ein Tupel zurück mit dem Speicherort der gewählten Datei
    ort = files[0]
    split = os.path.splitext(ort)
    
    Zielort = Zielort = split[0]+"_verschl"+split[1]
    
    
    #lese datei ein und wandle sie in ein np.array um 
    with Image.open(ort) as img:
        pix = np.array(img)
     
    print(pix.shape)
    
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
        if c < columns:#here
            #lese den binärwert des r,c roten pixels aus 
            vorher = bin(pix[r,c][0])[2:].zfill(8)
            if zuSchreiben[0] != vorher[-1]:
                veraend = str(LetzteStelle(vorher, zuSchreiben[0]))
                akt = veraend
            else: akt = vorher # here
            # c += 1 # here
                
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
    for i in range(64): # here achtung wenn bild weniger als 64 pixel breit
        #liest den int wert vom roten pixel ein als binärzahl ein 
        zeile = i // 64 # here integer division: ergebnis ohne nachkommastelle
        spalte = i % 64 # here
        lastBits += bin(pix[zeile,spalte][0])[2:][-1] # here
        # nimmt den letzten bit des pixels 
        
    # nimmt die so erstellte Binärzahl und gibt Integer an 
    return int(lastBits, 2)
        



def entschluessel():
    
    # verwende tkinter um die datei einfach auszuwählen 
    root = tkinter.Tk()

    def close_win():
       root.destroy()
    
    # erstelle close button 
    button = tkinter.Button(root, text= "Close", font=('Poppins bold', 16),
    command=close_win).pack(pady=20)
    files = filedialog.askopenfilenames(parent = root,
                                        title = "Wähl ein Bild aus",
                                        filetypes=[("Bild-Dateien", ".png")] )

    # files gibt ein Tupel zurück mit dem Speicherort der gewählten Datei
    Ort = files[0]
    
    #ermittle wie lange die nachricht ist
    laengeNachricht = LaengeNachricht(Ort)

    #lese datei ein und wandle sie in ein np.array um 
    with Image.open(Ort) as img:
        pix = np.array(img)
        
    rows = pix.shape[0]
    columns = pix.shape[1]
   

    # Startzeile ab dem die Nachricht beginnt
    #länge der nachricht geht ja von range(0,64) also muss ich von der 6
    c = 64 % columns # here 
    r = 64 // rows # here
    
    #Solange die Nachricht nicht komplett ausgelesen ist loope durch
    # hole alle letzten Bits raus 
    erg = ""
    for _ in range(laengeNachricht): # here (schleife bricht sonst nicht ab)
        if c < columns: # here (0 bis 63)
            #lese den letzten bit des binärwert des r,c roten pixels aus 
            erg += bin(pix[r,c][0])[2:].zfill(8)[-1] 
            
            # gehe in nächste spalte
            c += 1
                
        else: #korrigiere Überlauf
            c = 0
            r += 1
            erg += bin(pix[r,c][0])[2:].zfill(8)[-1] 
            c += 1 # here
    # nun muss man aus dem string dem string der alle binärzahlen enthält wieder buchstaben erzeugen 
    
    # erzeuge liste aus gruppe mit jeweils 8 bits 
    ergList = []
    while erg:
        ergList.append(chr(int(erg[:8],2)))
        erg = erg[8:]
    
    # verwende erg wieder um die Nachricht darin zu speichern 
    erg = "".join(ergList) # here (kurzschreibweise)
    
    return erg
    
# inb="bild.png"
# outb="out.png"
# verschluessel(inb, outb, "Hallo Welt!")
# print("in")
# with Image.open(inb) as img:
#     pix = np.array(img)
#     print(pix[:5,])
# print("out")
# with Image.open(outb) as img:
#     pix = np.array(img)
#     print(pix[:5,])

# print(entschluessel(outb))

#### DAS WAR EIN TEST 
    

# inb = r"C:\Users\bauer\OneDrive\TUM\5- Wissenschaftliche Programmierung\Code_Beispiele\Test.png"
# outb = r"C:\Users\bauer\OneDrive\TUM\5- Wissenschaftliche Programmierung\Code_Beispiele\WebsiteTest.png"
# nachricht = """AstraZeneca-Chef Pascal Soriot hat den Verdacht zurückgewiesen, sein Unternehmen liefere eigentlich für die EU bestimmte Impfdosen an andere Länder. AstraZeneca verkaufe das Vakzin »nicht anderswo für Profit«, versicherte Soriot in einem am Dienstagabend veröffentlichten Interview mit einem Verbund europäischer Zeitungen, zu dem das deutsche Blatt »Die Welt« gehört.

# AstraZeneca habe seinen Impfstoff gemeinnützig entwickelt, »wir verdienen damit kein Geld«, betonte der Unternehmenschef. Er fügte hinzu: »Ich denke, wir behandeln Europa wirklich fair.«

# In der EU-Kommission gibt es den Verdacht, Engpässe bei der Belieferung der Europäischen Union mit dem AstraZeneca-Vakzin könnten darauf zurückzuführen sein, dass der britisch-schwedische Hersteller Großbritannien und andere Nicht-EU-Länder mit ungekürzten Mengen des Impfstoffs beliefert.

# AstraZeneca hatte bei zwei Treffen mit der EU-Kommission und den Mitgliedstaaten am Montag Brüssel zufolge nicht ausreichend erklären können, wie es zu den Lieferengpässen gekommen ist. Nach Angaben der Kommission ist für diesen Mittwoch ein weiteres Treffen mit dem Unternehmen angesetzt.

# Soriot hob hervor, dass AstraZeneca seinen Liefervertrag mit Großbritannien drei Monate früher als mit der EU geschlossen habe. Auch bei der Belieferung Großbritanniens habe es »Anfangsprobleme« gegeben. Dort habe es aber drei Monate mehr Zeit gegeben, um diese Probleme zu beheben. In der EU befinde sich AstraZeneca zwei Monate hinter dem ursprünglichen Plan.

# »Aber der Vertrag mit den Briten wurde drei Monate vor dem mit Brüssel geschlossen. Wir hatten dort drei Monate mehr Zeit, um Pannen zu beheben.« Sein Unternehmen sei vertraglich nicht zur Lieferung bestimmter Mengen Impfstoff verpflichtet. Brüssel wollte nach seinen Worten mehr oder weniger zum selben Zeitpunkt beliefert werden wie die Briten – obwohl diese drei Monate früher unterzeichnet hätten. »Darum haben wir zugesagt, es zu versuchen, uns aber nicht vertraglich verpflichtet.«

# Hintergrund ist die Ankündigung der Pharmafirma, nach der für diese Woche erwarteten Zulassung zunächst weniger Impfstoff zu liefern als vereinbart. Statt 80 Millionen Impfdosen sollen nach EU-Angaben bis Ende März nur 31 Millionen ankommen. Den angegebenen Grund – Probleme in der Lieferkette – will die EU nicht gelten lassen. Sie fordert Vertragstreue. Die EU-Kommission hat Vertreter des britisch-schwedischen Konzerns an diesem Mittwoch zur Krisensitzung mit Experten der EU-Staaten geladen.

# Soriot weist geringe Wirksamkeit bei älteren Menschen zurück
# Berichte deutscher Medien, die Wirksamkeit des AstraZeneca-Impfstoffs sei bei älteren Menschen nur gering, wies Soriot zurück. Das »Handelsblatt« hatte berichtet, bei dem Vakzin werde nur mit einer Wirksamkeit von acht Prozent bei den über 65-Jährigen gerechnet. Soriot nannte diese Zahl falsch: »Wie kann man annehmen, dass Prüfbehörden rund um den Globus ein Mittel zulassen, das nur acht Prozent Wirksamkeit hat?«

# Auch das Bundesgesundheitsministerium hatte am Dienstag die Berichte über eine geringere Wirksamkeit des AstraZeneca-Präparats bei Senioren dementiert. Es sprach von einer möglichen Verwechslung von Zahlen. Aus den genannten Daten lasse sich keine geringe Wirksamkeit bei Älteren herleiten, erklärte das Ministerium. Bekannt sei aber »seit dem Herbst, dass in den ersten eingereichten Studien von AstraZeneca weniger Ältere beteiligt waren als bei den Studien anderer Hersteller«.

# Das AstraZeneca-Vakzin ist bislang nicht in der EU zugelassen. Eine Entscheidung der europäischen Arzneimittelbehörde EMA über die Zulassung des Präparats wird für Freitag erwartet. 

# """


# # nachricht = "Das ist ein Test und bei kurzen Sachen funktioniert es"
# verschluessel(inb, outb, nachricht)
# print(entschluessel(outb))
# print("erledigt")

