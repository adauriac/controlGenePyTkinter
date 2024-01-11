import controlGenePyCli
from tkinter import *

myGene = controlGenePyCli.geneControler()
ans = myGene.connect()
if not ans:
    msg = myGene.messageConnection
    print(msg)
    root = Tk()
    root2 = Tk()

    label = Label(root,text=msg,height=20,width=100)
    label.pack()
    root.mainloop()
    exit(1)

root = Tk()
canvasBoutonLed = Canvas(root,width=100*2,height=2*120*2,background='#F0F0F0')
canvasConsignes = Canvas(root,width=100*2,height=2*120,background='#FEF0F0')
canvasValues = Canvas(root,width=100*2,height=2*120,background='#F0FEF0')


canvasBoutonLed.grid(row=0,column=0,rowspan=2)
canvasConsignes.grid(row=0,column=1)
canvasValues.grid(row=1,column=1)

led = canvasBoutonLed.create_oval(50,50,100,100)
canvasBoutonLed.itemconfig(led,fill='red')

cpt = 0
def watch():
    global cpt,myGene,root
    print("entering blink %d"%cpt)
    color = 'blue' if cpt%2 else 'red'
    cpt += 1
    canvasBoutonLed.itemconfig(led,fill=color)
    w = root.after(1000,watch)
  
canvasConsignes.create_text(40,10,text="Consignes")

canvasValues.create_text(40,10,text="Values")
canvasValues.create_text(40,10+1*30,text="Puissance (W)")
#labValLeg=Label(canvasValues,text="Valeurs")
#labValLeg.pack()
#labValPow=Label(canvasValues,text="%d"%10)
#labValPow.pack()
canvasValues.create_text(40,10+2*30,text="Debit(1/mn)")
canvasValues.create_text(40,10+3*30,text="Courant pont (mA)")
canvasValues.create_text(40,10+4*30,text="Tension PFC(V)")

watch()
root.mainloop()
