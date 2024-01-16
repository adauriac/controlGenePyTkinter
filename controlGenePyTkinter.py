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
canvasBoutonLed = Canvas(root,width=w1,height=h1,background='#F0F0F0')
canvasConsignes = Canvas(root,width=w2,height=h2,background='#FEF0F0')
canvasValues = Canvas(root,width=w2,height=h1-h2,background='#F0FEF0')

canvasBoutonLed.grid(row=0,column=0,rowspan=2)
canvasConsignes.grid(row=0,column=1)
canvasValues.grid(row=1,column=1)

cpt = 0
def watch():
    global watchWaiting,cpt,myGene # car il sera modifie par getRegisters
    myGene.getRegisters()
    print("entering watch %d"%cpt)
    color = 'blue' if cpt%2 else 'red'
    cpt += 1
    canvasValues.itemconfig(ledVal,fill=color)
    canvasValues.itemconfig(powerVal,text="%d"%myGene.vals[myGene.addToIndex[0x6B]])
    canvasValues.itemconfig(flowVal,text="%d"%myGene.vals[myGene.addToIndex[0x68]])
    canvasValues.itemconfig(currentVal,text="%d"%myGene.vals[myGene.addToIndex[0x7F]])
    canvasValues.itemconfig(tensionVal,text="%d"%myGene.vals[myGene.addToIndex[0x72]])
    root.after(1000,watch)
  
canvasConsignes.create_text(w2/2,h2/12,text="Consignes")
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
watch()
root.mainloop()
