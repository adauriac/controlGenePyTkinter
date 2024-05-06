import controlGenePyCli
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

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

class LED(tk.Canvas):
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

class LEDBttn(tk.Canvas):
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

class LEDWidget(tk.Canvas):
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

class controlGenePyTkinter():
    def __init__(self,parent=None,simul=False):
        # create the  controlGenePyCli class = the command line interpreteur class
        self.myGene = controlGenePyCli.geneControler(simul)
        ans = self.myGene.connect()
        if not ans:
            msg = self.myGene.messageConnection
            print(msg)
            label = tk.Label(parent,text=msg,height=20,width=100)
            label.pack()
            # root.mainloop()
            return
        # here cpnnection established
        if parent==None:
            parent = tk.Tk()
        self.parent = parent
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
        canvasBoutonLed = tk.Canvas(parent,width=w,height=h,background=colorBoutonLed)
        frameBoutonLed = tk.Frame(parent,width=w,height=h,background=colorBoutonLed)
        canvasConsignes = tk.Canvas(parent,width=w,height=h,background=colorConsigne)
        frameConsignes = tk.Frame(parent,width=w,height=h,background=colorConsigne)
        self.canvasValues = tk.Canvas(parent,width=w,height=h,background=colorValues)
        frameValues = tk.Frame(parent,width=w,height=h,background=colorValues)
        canvasLogo = tk.Canvas(parent,width=w,height=h);
        canvasBoutonLed.grid(row=0,column=0)#,rowspan=2)
        frameBoutonLed.grid(row=0,column=0)#,rowspan=2)
        canvasConsignes.grid(row=0,column=1)
        frameConsignes.grid(row=0,column=1)
        self.canvasValues.grid(row=1,column=1)
        # frameValues.grid(row=1,column=1)
        canvasLogo.grid(row=1,column=0)

        # LOGO
        img = tk.PhotoImage(file="logo.png")
        canvasLogo.create_image(132,130,image=img)

        # CONSIGNES
        tk.Label(frameConsignes,text="Power (W)",background=colorConsigne).grid(column=0,row=0)
        tk.Label(frameConsignes,text="Flow (l/mn)",background=colorConsigne).grid(column=0,row=1)
        tk.Label(frameConsignes,text="Power low limit (W)",background=colorConsigne).grid(column=0,row=2)
        tk.Label(frameConsignes,text="Power high limit (W)",background=colorConsigne).grid(column=0,row=3)
        tk.Label(frameConsignes,text="Flow low limit (l/mn)",background=colorConsigne).grid(column=0,row=4)
        tk.Label(frameConsignes,text="Flow high limit (l/mn)",background=colorConsigne).grid(column=0,row=5)
        valPower = tk.Label(frameConsignes,text="100",background=colorConsigne,height=2)
        valFlow = tk.Label(frameConsignes,text="100",width=5,background=colorConsigne,height=2)
        valPowerLow = tk.Label(frameConsignes,text="80",width=5,background=colorConsigne,height=2)
        valPowerHigh = tk.Label(frameConsignes,text="120",background=colorConsigne,height=2)
        valFlowLow = tk.Label(frameConsignes,text="90",background=colorConsigne,height=2)
        valFlowHigh = tk.Label(frameConsignes,text="110",background=colorConsigne,height=2)
        valPower.grid(column=1,row=0)
        valFlow.grid(column=1,row=1)
        valPowerLow.grid(column=1,row=2)
        valPowerHigh.grid(column=1,row=3)
        valFlowLow.grid(column=1,row=4)
        valFlowHigh.grid(column=1,row=5)
        entryPower = ttk.Entry(frameConsignes,text="",width=5)
        entryFlow = ttk.Entry(frameConsignes,text="",width=5)
        entryPowerHigh = ttk.Entry(frameConsignes,text="",width=5)
        entryPowerLow = ttk.Entry(frameConsignes,text="",width=5)
        entryFlowHigh = ttk.Entry(frameConsignes,text="",width=5)
        entryFlowLow = ttk.Entry(frameConsignes,text="",width=5)
        entryPower.grid(column=2,row=0)
        entryFlow.grid(column=2,row=1)
        entryPowerLow.grid(column=2,row=2)
        entryPowerHigh.grid(column=2,row=3)
        entryFlowLow.grid(column=2,row=4)
        entryFlowHigh.grid(column=2,row=5)
        tk.Button(frameConsignes,text="Submit",command=self.setNewValues).grid(column=2,row=6)

        # VALUES
        nl = 12 # #lines
        R = 10 # rayon de la led
        self.canvasValues.create_text(w2/2,(h1-h2)/nl,anchor="center",text="Values")
        ledLab     = self.canvasValues.create_text(5,3*(h1-h2)/nl,anchor="w",text="Watchdog")
        powerLab   = self.canvasValues.create_text(5,5*(h1-h2)/nl,anchor="w",text="Puissance (W)")
        flowLab    = self.canvasValues.create_text(5,7*(h1-h2)/nl,anchor="w",text="Debit(1/mn)")
        currentLab = self.canvasValues.create_text(5,9*(h1-h2)/nl,anchor="w",text="Courant pont (mA)")
        tensionLab = self.canvasValues.create_text(5,11*(h1-h2)/nl,anchor="w",text="Tension PFC(V)")
        self.ledVal     = self.canvasValues.create_oval(3*w2/4-R/2,3*(h1-h2)/nl-R/2,3*w2/4+R/2,3*(h1-h2)/nl+R/2)
        self.powerVal   = self.canvasValues.create_text(3*w2/4+5,5*(h1-h2)/nl,anchor="center",text="111")
        self.flowVal    = self.canvasValues.create_text(3*w2/4+5,7*(h1-h2)/nl,anchor="center",text="222")
        self.currentVal = self.canvasValues.create_text(3*w2/4+5,9*(h1-h2)/nl,anchor="center",text="333")
        self.tensionVal = self.canvasValues.create_text(3*w2/4+5,11*(h1-h2)/nl,anchor="c",text="444")

        # BOUTON-LED
        tk.Label(frameBoutonLed,text="Generator",background=colorBoutonLed,height=2).grid(column=0,row=0)
        tk.Label(frameBoutonLed,text="Gaz",background=colorBoutonLed,height=2).grid(column=0,row=1)
        tk.Label(frameBoutonLed,text="Plasma",background=colorBoutonLed,height=2).grid(column=0,row=2)
        tk.Label(frameBoutonLed,text="Emergency stop",background=colorBoutonLed,height=2).grid(column=0,row=3)
        tk.Label(frameBoutonLed,text="Critical defect",background=colorBoutonLed,height=2).grid(column=0,row=4)
        tk.Label(frameBoutonLed,text="State",background=colorBoutonLed,height=2).grid(column=0,row=5)
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
        parent.protocol("WM_DELETE_WINDOW",lambda : (parent.after_cancel(self.watch),parent.destroy()))
        self.cpt = 0
        self.newValues = False
        # sys.exit(123)
        # return
        # self.watch()
        # parent.mainloop()
    # FIN def __init__(parent=None,simul=False)
    # #############################################################################

    def watch(self):
        global watchWaiting # car il sera modifie par getRegisters
        self.myGene.getRegisters()
        print("entering watch %d"%self.cpt)
        color = 'blue' if self.cpt%2 else 'red'
        self.cpt += 1
        if self.newValues:
            self.newValues = False
            print("je dois affecter les registres de consignes")
        self.canvasValues.itemconfig(self.ledVal,fill=color)
        self.canvasValues.itemconfig(self.powerVal,text="%d"%self.myGene.vals[self.myGene.addToIndex[0x6B]])
        self.canvasValues.itemconfig(self.flowVal,text="%d"%self.myGene.vals[self.myGene.addToIndex[0x68]])
        self.canvasValues.itemconfig(self.currentVal,text="%d"%self.myGene.vals[self.myGene.addToIndex[0x7F]])
        self.canvasValues.itemconfig(self.tensionVal,text="%d"%self.myGene.vals[self.myGene.addToIndex[0x72]])
        self.parent.after(1000,self.watch)
    # FIN def watch(self):
    # #############################################################################

    def setNewValues(self):
        powerCons = self.myGene.vals[self.myGene.addToIndex[0xB2]]
        powerMin = self.myGene.vals[self.myGene.addToIndex[0x96]]
        powerMax = self.myGene.vals[self.myGene.addToIndex[0x97]]
        flowCons = self.myGene.vals[self.myGene.addToIndex[0xB3]]
        flowMin = self.myGene.vals[self.myGene.addToIndex[0xA0]]
        flowMax = self.myGene.vals[self.myGene.addToIndex[0xA1]]
        print(powerMin,powerCons,powerMax)
        if powerCons<powerMin or powerCons>powerMax:
            tkinter.messagebox.showinfo("","Given data inconsistent")
            return                          
        self.newValues = True
    # FIN def setNewValues(self)
    # #############################################################################
# FIN class controlGenePyTkinter():

############################################################################
#                           EN AVANT SIMONE                                #
############################################################################
if __name__ == "__main__":
    my = controlGenePyTkinter()
