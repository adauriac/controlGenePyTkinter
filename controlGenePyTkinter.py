import controlGenePyCli
from tkinter import *
from tkinter import ttk

myGene = controlGenePyCli.geneControler()
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
colorConsigne = '#FEF0F0'
canvasBoutonLed = Canvas(root,width=w1,height=h1,background='#F0F0F0')
canvasConsignes = Canvas(root,width=w2,height=h2,background=colorConsigne)
frameConsignes = Frame(root,width=w2,height=h2,background=colorConsigne)
canvasValues = Canvas(root,width=w2,height=h1-h2,background='#F0FEF0')

canvasBoutonLed.grid(row=0,column=0,rowspan=2)
canvasConsignes.grid(row=0,column=1)
frameConsignes.grid(row=0,column=1)
canvasValues.grid(row=1,column=1)

cpt = 0
newValues = False
def setNewValues():
    global newValues
    newValues = True
    
def watch():
    global watchWaiting,cpt,myGene,newValues # car il sera modifie par getRegisters
    myGene.getRegisters()
    print("entering watch %d"%cpt)
    color = 'blue' if cpt%2 else 'red'
    cpt += 1
    if newValues:
        newValues = False
        print("je dois affecetr les registres de consignes")
    canvasValues.itemconfig(ledVal,fill=color)
    canvasValues.itemconfig(powerVal,text="%d"%myGene.vals[myGene.addToIndex[0x6B]])
    canvasValues.itemconfig(flowVal,text="%d"%myGene.vals[myGene.addToIndex[0x68]])
    canvasValues.itemconfig(currentVal,text="%d"%myGene.vals[myGene.addToIndex[0x7F]])
    canvasValues.itemconfig(tensionVal,text="%d"%myGene.vals[myGene.addToIndex[0x72]])
    root.after(1000,watch)
  
# canvasConsignes.create_text(w2/2,h2/12,text="Consignes")
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

# input("? ")
# pour que le watchdog s'arrete quand on ferme le fenetre principale
root.protocol("WM_DELETE_WINDOW",lambda : (root.after_cancel(watch),root.destroy()))
# exit(123)
watch()
root.mainloop()
