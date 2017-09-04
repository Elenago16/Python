# Programmeringsteknik webbkurs KTH P-uppgift 
# Elena Goncharuk
# 21 september 2014
#
# 176 Repeterade ord
# Ett program som lä̈ser text f̊rån en fil, skriver ut texten
# på skä̈rmen och markerar ett ord om det har upprepas inom
# ett intervall på ca 40 ord

from tkinter import *
import os.path

# Konstanter
ANTAL_ORD = 40 #antal ord som kontrolleras
UNDANTAGFIL = "Undantag.txt" #filen med ord som ska inte kontrolleras

undantagslista = []

# Funktioner för hantering av grafiskt anvä̈ndargrä̈nssnitt

class Fönstret (Frame):
    # Konstruktorn
    def __init__ (self, parent):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.parent.title("Kontroll för repeterade ord")
        self.visaWidgets()
        return

    # Skapar widgetar       
    def visaWidgets (self):
        introFrame = Frame () 
        introTxt = ("Välkommen!\nHär kan du kontrollera om din " +
        "text innehåller repeterade ord. Orden som har\nupprepats " +
        "inom ett intervall på ca " + str(ANTAL_ORD) + " ord kommer " +
        "att markeras på skärmen.\nDu kan även hoppa över vissa ord, " +
        "ordet kommer då ignoreras\n tills du stänger av programmet. Markera " +
        "i kryssrutan för\n att ignorera ordet även i framtida körningar.")
        intro = Label(introFrame, text=introTxt, width=20, height=6)
        intro.pack(pady=4, padx=4, fill=BOTH, expand=1)
        introFrame.pack(fill=BOTH)

        bigFrame = Frame()

        leftFrame = Frame(bigFrame, borderwidth=2, relief=GROOVE)
        
        Scr = Scrollbar(leftFrame)
        self.texten = Text(leftFrame, height=20, width=50, state=DISABLED,
                            wrap=WORD, yscrollcommand=Scr.set)
        Scr.config(command=self.texten.yview)
        Scr.pack(side=RIGHT, fill=Y)
        self.texten.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=3)
        leftFrame.pack(side=LEFT, fill=BOTH, expand=True)

        rightFrame = Frame(bigFrame, pady=20, padx=5)
        
        undantagFrame = Frame(rightFrame)
        self.undantagEntry = Entry(undantagFrame)
        self.undantagEntry.pack(side=LEFT, padx=3)
        undantagKnp = Button(undantagFrame, text="Spara ordet",
                              command=self.läsaOrdet)
        undantagKnp.pack(side=LEFT)
        undantagFrame.pack(side=TOP)
        
        kryssFrame = Frame(rightFrame)
        self.kryssad = IntVar(kryssFrame)
        self.undantagKryss = Checkbutton(kryssFrame, text="Spara permanent",
                                          variable = self.kryssad)
        self.undantagKryss.pack(anchor="e")
        kryssFrame.pack(side=TOP)
        self.undantagLbl = Label(rightFrame, text="")
        self.undantagLbl.pack(side=TOP)
        
        filFrame = Frame(rightFrame)
        öppnaKnp = Button(filFrame, text="Öppna fil", command=self.öppnaFil)
        öppnaKnp.pack(side=LEFT)
        self.okKnp = Button(filFrame, text="Kontrollera", command=self.starta, state=DISABLED)
        öppnaKnp.pack(side=LEFT)
        self.okKnp.pack(side=LEFT)
        filFrame.pack(side=TOP)

        avslutaFrame = Frame(rightFrame)
        avslutaKnp = Button(avslutaFrame, text="Avsluta",
                         command=root.destroy)
        avslutaKnp.pack(padx=15)
        avslutaFrame.pack(side=BOTTOM, fill="y", anchor="e")

        rightFrame.pack(side=LEFT, fill="y")
        bigFrame.pack(fill="both", expand=True, padx=8, pady=8)
        return
        
    # Öppna filen-dialog
    def öppnaFil (self):
        self.filnamn = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        self.okKnp.config(state=NORMAL)
        return

    # Läser indata från Entry och skriver ett meddelande om statusen
    def läsaOrdet (self):
        ordet = self.undantagEntry.get().strip().lower()
        if ordet == "":
            self.undantagLbl.config(fg="red", text="Fältet är tomt")
        elif iListan(ordet, undantagslista):
            self.undantagLbl.config (fg="red", text="Ordet är redan sparat")
        else:
            sparaUndantag (ordet, self.kryssad.get())
            self.undantagLbl.config(fg="green", text="Ordet är sparat")
        self.undantagKryss.deselect()
        self.undantagEntry.delete(0, END)
        return
        
    # Startar kontrollen av texten från filen
    def starta (self):
        self.undantagLbl.config(text="")
        self.texten.config(state=NORMAL)
        self.texten.delete(1.0, END)
        self.texten.config(state=DISABLED)
        kontrolleraTexten(self.filnamn)
        return
        

    # Skrivet ett Ord-objekt i Text-widget med ev. markeringar
    # IN: Ord-objekt
    def visaOrdet (self, ordet):
        self.texten.tag_config("mark", background="yellow")
        self.texten.config (state=NORMAL)
        if ordet.markerat:
            self.texten.insert (END, ordet.innehåll, "mark")
        else:
            self.texten.insert (END, ordet.innehåll)
        self.texten.insert (END, ordet.tecken + " ")
        self.texten.config(state=DISABLED)
        return
        
# Slut för anvä̈ndargrä̈nssnittet


# En klass som beskriver ett ord.
# Attribut:
#    innehåll - ord utan skiljetecken
#    tecken - innehåler skijetecken som följer ordet i texten
#    markerat - visar om ordet är markerat
class Ord:
        
    # Konstruktorn
    def __init__ (self, innehåll):
        self.innehåll = innehåll
        self.tecken = ""
        self.markerat = 0
        return
    
    # Separerar bokstaver och skiljetecken
    def rensa (self):
        if len(self.innehåll)>1:
            while not self.innehåll[(len(self.innehåll) - 1)].isalnum():
                self.tecken = self.innehåll [(len(self.innehåll) - 1)] + self.tecken
                self.innehåll = self.innehåll[:-1]
        else:
            if not self.innehåll.isalnum():
                self.tecken = self.innehåll
                self.innehåll = ""
        return
        
# Här slutar Ordsklassen

# Lagrar innehållet från filen i en lista, rad för rad
# IN: namnet på filen
# UT: lista med rader
def skapaListan (filnamn):
    listan = []
    if  os.path.isfile(filnamn):
        fil = open(filnamn, "r", encoding = "utf-8")
        listan = [rad.strip() for rad in fil]
        fil.close()
    return listan

# Kontrollerar om en sträng finns i listan
# IN: ordet = en sträng
#     lista = lista med strängar
# UT: 1 om ordet finns, annars 0
def iListan (ordet, lista):
    resultat = 0
    if ordet.lower() in lista:
            resultat = 1
            return resultat
    return resultat

# Sparar ordet i listan  och ev. i filen med undantag
# IN: ordet = en sträng
#     sparaPermanent = 1 om ordet ska sparas i filen
def sparaUndantag (ordet, sparaPermanent):                    
    if sparaPermanent:
        file = open(UNDANTAGFIL, "a", encoding = "utf-8")
        file.write(ordet +"\n")
        file.close()
    undantagslista.append(ordet)
    return

# Markerar Ord-objekt om den finns i listan med ord
# IN: ordet = Ord-objekt
#     ordlista = en lista med strängar
# UT: Ord-objekt 
def kontrolleraOrdet (ordet, ordlista):
    ordet.rensa() # separerar bokstaver och skiljetecken
    if iListan (ordet.innehåll, ordlista):
        if not iListan (ordet.innehåll, undantagslista):
            ordet.markerat = 1
    return ordet

# Markerar upprepade ord i texten 
# IN: filen med en text
def kontrolleraTexten (filnamn):
    ordlista = ANTAL_ORD * [None] # en lista med ord
    fil = open(filnamn, 'r', encoding = 'utf-8')
    txt = fil.read().split() #en lista med ord från texten
    i = 0 # ett index för ordlistan
    for enDel in txt: 
        ordet = Ord(enDel) # skapar ett Ord-objekt
        kontrolleraOrdet (ordet, ordlista) #kontrollerar om det finns i listan
        ordlista [i] = ordet.innehåll.lower() #sparar ordet i ordlistan
        if i == ANTAL_ORD -1: # ordlistan ska fyllas på kontinuerligt
            i = 0
        else:
            i+=1
        Fönstret.visaOrdet(app, ordet) #Skriva ut ordet på skärmen             
    fil.close()
    return
    

#  --------  Här börjar huvudprogrammet -----------

undantagslista = skapaListan (UNDANTAGFIL)
root = Tk() #root-fönster
root.resizable(0,0) # fönstret är fixerat i storleken
app = Fönstret(root) #initierar fönstret
root.mainloop()
