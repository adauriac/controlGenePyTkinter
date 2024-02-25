import controlGenePyCli
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import sys
import ctypes

"""
appel:
depuis msys2: /mingw64/bin/python controlGenePyTkinter.py
depuis powershell : C:\\Users\\ACXYS\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe .\\controlGenePyTkinter.py

Sorties
      addresse registre                 nom du label
Power       0x6b             canvasValues.itemconfig(powerVal
Flow        0x68             canvasValues.itemconfig(flowVal
Current     Ox7f             canvasValues.itemconfig(currentVal   
Tension     0x72             canvasValues.itemconfig(tensionVal
"""

class LED(Canvas):
    def __init__(self, master=None,R=10, **kwargs):
        self.R = R
        super().__init__(master, width=2*R, height=2*R,  **kwargs)
        # tkinter.messagebox.showinfo("titre","Creation LEDWidget %d"%R)
        self.state = False
        self.draw()

    def draw(self):
        color = "green" if self.state else "gray"
        # self.delete("all")
        R = self.R
        self.create_oval(2, 2, 2*R+2, 2*R+2, width=0, fill=color, outline=color)

    def set_state(self, state):
        self.state = state
        self.draw()

class LEDBttn(Canvas):
    def __init__(self, master=None,R=10,callBack=None, **kwargs):
        self.R = R
        self.callBack = callBack
        super().__init__(master, width=2*R, height=2*R,  **kwargs)
        # tkinter.messagebox.showinfo("titre","Creation LEDWidget %d"%R)
        self.state = False
        self.draw()
        self.bind("<Button-1>",lambda event:self.callBack(self))

    def draw(self):
        color = "green" if self.state else "gray"
        # self.delete("all")
        R = self.R
        self.create_oval(2, 2, 2*R+2, 2*R+2, width=6, fill=color, outline=color)

    def set_state(self, state):
        self.state = state
        self.draw()

class LEDWidget(Canvas):
    def init(self, master=None, **kwargs):
        super().init(master, width=20, height=20, bd=0, highlightthickness=0, **kwargs)
        self.state = False
        self.draw()

    def draw(self):
        color = "green" if self.state else "gray"
        self.delete("all")
        self.create_oval(2, 2, 18, 18, fill=color, outline=color)

    def set_state(self, state):
        self.state = state
        self.draw()

def setNewValues():
    global newValues
    powerCons = myGene.vals[myGene.addToIndex[0xB2]]
    powerMin = myGene.vals[myGene.addToIndex[0x96]]
    powerMax = myGene.vals[myGene.addToIndex[0x97]]
    flowCons = myGene.vals[myGene.addToIndex[0xB3]]
    flowMin = myGene.vals[myGene.addToIndex[0xA0]]
    flowMax = myGene.vals[myGene.addToIndex[0xA1]]
    print(powerMin,powerCons,powerMax)
    if powerCons<powerMin or powerCons>powerMax:
        tkinter.messagebox.showinfo("","Given data inconsistent")
        return                          
    newValues = True
    
def watch():
    global watchWaiting,cpt,myGene,newValues # car il sera modifie par getRegisters
    myGene.getRegisters()
    print("entering watch %d"%cpt)
    color = 'blue' if cpt%2 else 'red'
    cpt += 1
    if newValues:
        newValues = False
        print("je dois affecter les registres de consignes")
    canvasValues.itemconfig(ledVal,fill=color)
    canvasValues.itemconfig(powerVal,text="%d"%myGene.vals[myGene.addToIndex[0x6B]])
    canvasValues.itemconfig(flowVal,text="%d"%myGene.vals[myGene.addToIndex[0x68]])
    canvasValues.itemconfig(currentVal,text="%d"%myGene.vals[myGene.addToIndex[0x7F]])
    canvasValues.itemconfig(tensionVal,text="%d"%myGene.vals[myGene.addToIndex[0x72]])
    root.after(1000,watch)

############################################################################
#                           EN AVANT SIMONE                                #
############################################################################
myGene = controlGenePyCli.geneControler(simul=len(sys.argv)!=1)
ans = myGene.connect()
if not ans:
    msg = myGene.messageConnection
    print(msg)
    root = Tk()

    label = Label(root,text=msg,height=20,width=100)
    label.pack()
    root.mainloop()
    exit(1)

root = Tk()
w1 = 250 # 200
h1 = 520 #4*120
w2 = w1
h2 = h1/2
w = 250
h  = 250

# DISPOSITION GENERALE
colorConsigne = '#FEF0F0'
colorBoutonLed = '#F0F0F0'
colorValues = '#F0FEF0'
canvasBoutonLed = Canvas(root,width=w,height=h,background=colorBoutonLed)
frameBoutonLed = Frame(root,width=w,height=h,background=colorBoutonLed)
canvasConsignes = Canvas(root,width=w,height=h,background=colorConsigne)
frameConsignes = Frame(root,width=w,height=h,background=colorConsigne)
canvasValues = Canvas(root,width=w,height=h,background=colorValues)
frameValues = Frame(root,width=w,height=h,background=colorValues)
canvasLogo = Canvas(root,width=w,height=h);
canvasBoutonLed.grid(row=0,column=0)#,rowspan=2)
frameBoutonLed.grid(row=0,column=0)#,rowspan=2)
canvasConsignes.grid(row=0,column=1)
frameConsignes.grid(row=0,column=1)
canvasValues.grid(row=1,column=1)
# frameValues.grid(row=1,column=1)
canvasLogo.grid(row=1,column=0)

# LOGO
img = PhotoImage(file="logo.png")
canvasLogo.create_image(132,130,image=img)

# CONSIGNES
Label(frameConsignes,text="Power (W)",background=colorConsigne).grid(column=0,row=0)
Label(frameConsignes,text="Flow (l/mn)",background=colorConsigne).grid(column=0,row=1)
Label(frameConsignes,text="Power low limit (W)",background=colorConsigne).grid(column=0,row=2)
Label(frameConsignes,text="Power high limit (W)",background=colorConsigne).grid(column=0,row=3)
Label(frameConsignes,text="Flow low limit (l/mn)",background=colorConsigne).grid(column=0,row=4)
Label(frameConsignes,text="Flow high limit (l/mn)",background=colorConsigne).grid(column=0,row=5)
valPower = Label(frameConsignes,text="100",background=colorConsigne,height=2)
valFlow = Label(frameConsignes,text="100",width=5,background=colorConsigne,height=2)
valPowerLow = Label(frameConsignes,text="80",width=5,background=colorConsigne,height=2)
valPowerHigh = Label(frameConsignes,text="120",background=colorConsigne,height=2)
valFlowLow = Label(frameConsignes,text="90",background=colorConsigne,height=2)
valFlowHigh = Label(frameConsignes,text="110",background=colorConsigne,height=2)
valPower.grid(column=1,row=0)
valFlow.grid(column=1,row=1)
valPowerLow.grid(column=1,row=2)
valPowerHigh.grid(column=1,row=3)
valFlowLow.grid(column=1,row=4)
valFlowHigh.grid(column=1,row=5)
entryPower = Entry(frameConsignes,text="",width=5)
entryFlow = Entry(frameConsignes,text="",width=5)
entryPowerHigh = Entry(frameConsignes,text="",width=5)
entryPowerLow = Entry(frameConsignes,text="",width=5)
entryFlowHigh = Entry(frameConsignes,text="",width=5)
entryFlowLow = Entry(frameConsignes,text="",width=5)
entryPower.grid(column=2,row=0)
entryFlow.grid(column=2,row=1)
entryPowerLow.grid(column=2,row=2)
entryPowerHigh.grid(column=2,row=3)
entryFlowLow.grid(column=2,row=4)
entryFlowHigh.grid(column=2,row=5)
Button(frameConsignes,text="Submit",command=setNewValues).grid(column=2,row=6)

# VALUES
nl = 12 # #lines
R = 10 # rayon de la led
canvasValues.create_text(w2/2,(h1-h2)/nl,anchor="center",text="Values")
ledLab     = canvasValues.create_text(5,3*(h1-h2)/nl,anchor="w",text="Watchdog")
powerLab   = canvasValues.create_text(5,5*(h1-h2)/nl,anchor="w",text="Puissance (W)")
flowLab    = canvasValues.create_text(5,7*(h1-h2)/nl,anchor="w",text="Debit(1/mn)")
currentLab = canvasValues.create_text(5,9*(h1-h2)/nl,anchor="w",text="Courant pont (mA)")
tensionLab = canvasValues.create_text(5,11*(h1-h2)/nl,anchor="w",text="Tension PFC(V)")
ledVal     = canvasValues.create_oval(3*w2/4-R/2,3*(h1-h2)/nl-R/2,3*w2/4+R/2,3*(h1-h2)/nl+R/2)
powerVal   = canvasValues.create_text(3*w2/4+5,5*(h1-h2)/nl,anchor="center",text="111")
flowVal    = canvasValues.create_text(3*w2/4+5,7*(h1-h2)/nl,anchor="center",text="222")
currentVal = canvasValues.create_text(3*w2/4+5,9*(h1-h2)/nl,anchor="center",text="333")
tensionVal = canvasValues.create_text(3*w2/4+5,11*(h1-h2)/nl,anchor="c",text="444")

# BOUTON-LED
Label(frameBoutonLed,text="Generator",background=colorBoutonLed,height=2).grid(column=0,row=0)
Label(frameBoutonLed,text="Gaz",background=colorBoutonLed,height=2).grid(column=0,row=1)
Label(frameBoutonLed,text="Plasma",background=colorBoutonLed,height=2).grid(column=0,row=2)
Label(frameBoutonLed,text="Emergency stop",background=colorBoutonLed,height=2).grid(column=0,row=3)
Label(frameBoutonLed,text="Critical defect",background=colorBoutonLed,height=2).grid(column=0,row=4)
Label(frameBoutonLed,text="State",background=colorBoutonLed,height=2).grid(column=0,row=5)
butGenerator = LEDBttn(frameBoutonLed)
butGaz =  LEDBttn(frameBoutonLed)
butPlasma = LEDBttn(frameBoutonLed)
butEmergencyStop = LED(frameBoutonLed)
butCritcalDefect = LED(frameBoutonLed) 
butState = LED(frameBoutonLed)
butGenerator.grid(column=1,row=0)
butGaz.grid(column=1,row=1)
butPlasma.grid(column=1,row=2)
butEmergencyStop.grid(column=1,row=3)
butCritcalDefect.grid(column=1,row=4)
butState.grid(column=1,row=5)

# input("? ")
# pour que le watchdog s'arrete quand on ferme le fenetre principale
root.protocol("WM_DELETE_WINDOW",lambda : (root.after_cancel(watch),root.destroy()))
cpt = 0
newValues = False
watch()
root.mainloop()
