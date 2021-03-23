from tkinter import *
import tkinter.font as font
from ipcalculator2 import *

window = Tk()

name = Label(text="IP Calculator.") # to display IP Calculator at top of window
name.pack()

canvas1 = Canvas(window, width = 650, height = 450, background = "gray15") # initialising window colour and height etc.
canvas1.pack()

label2 = Label(window,width = 45 ,relief="solid",text= "Output", background= "gold")
canvas1.create_window(390, 100, window=label2)

label3 = Label(window,width = 60 ,height = 5,relief="solid",text= "Seperate input in text box by commas e.g 192.168.10.0,255.255.255.192", background = "gold")
canvas1.create_window(390, 350, window=label3)

border = Label(window,width = 70 ,height = 12,relief="solid", background = "gray", text= "Results will appear here")
canvas1.create_window(390, 210, window=border)


myFont = font.Font(size=10) # initilising text size



T = Text(window, height=4, width=40, relief = "solid", borderwidth = 2, background = "gray80")
T.pack() # textbox
T.insert('1.0','Type here.')


#canvas1.create_text(400,100,text =  "Output:")
entry1 = Entry() # 
canvas1.create_window(390, 40, window=T) # creating entry box
    
def class_stats ():
	
	clear_window = Label(window,background = "gray", width= 68, height= 10) # clearing window for next calculation.
	canvas1.create_window(390, 210, window=clear_window)
	ip_addr = T.get("1.0","end") # getting text from text box
	

	label1 = Label(window, background = "gray", text= get_class_stats(ip_addr)) # calls get class stats function
	canvas1.create_window(390, 210, window=label1) # calling label 1



def subnet_stats ():
	clear_window = Label(window,background = "gray", width= 68, height= 10) # clearing window for next calculation.
	canvas1.create_window(390, 210, window=clear_window)
	lines = T.get("1.0","end").split(",") # getting text from text box
	ip_addr = lines[0] # first is ip address in text box
	submask = lines[1] # second is submask in text box

	label2 = Label(window, background = "gray",text= get_subnet_stats(ip_addr,submask)) # calling get subnet stats
	canvas1.create_window(390, 210, window=label2)

def supernet_stats():
	clear_window = Label(window,background = "gray", width= 68, height= 10) # clearing window for next calculation.
	canvas1.create_window(390, 210, window=clear_window)

	ip_addr = T.get("1.0","end").split(",") # splitting text box data at comma

	label3 = Label(window, background = "gray",text= get_supernet_stats(ip_addr)) # calling get supernet stats
	canvas1.create_window(390, 210, window=label3)

#205.100.0.0,205.100.1.0,205.100.2.0,205.100.3.0

button1 = Button(text='Get Class Stats',relief = "solid", command=class_stats, height= 3, width = 15,background = "red3")
button1['font'] = myFont # assigning font size to button 1
canvas1.create_window(70, 120, window=button1) # each button here calls the functions that i wrote in this file

button2 = Button(text='Get Subnet Stats', relief = "solid",command=subnet_stats, height= 3, width = 15,background = "red3")
button2['font'] = myFont # assigning font size to button 1
canvas1.create_window(70, 200, window=button2)


button3 = Button(text='Get Supernet Stats', relief = "solid",command=supernet_stats, height= 3, width = 15,background = "red3")
button3['font'] = myFont # assigning font size to button 1
canvas1.create_window(70, 280, window=button3)

window.mainloop()
