from tkinter import Tk
from tkinter.ttk import Button, Entry, Label
from threading import Thread




class Gooey:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("gooey for test unit")
        self.window.geometry("300x300")
        

        self.button_1 = Button(self.window)
        self.button_2 = Button(self.window)
        self.button_3 = Button(self.window)
        
        self.input_bar = Entry(self.window)

        self.output_box_1 = Label(self.window)
        self.output_box_2 = Label(self.window)

        self.button_1.pack(pady=10)
        self.button_2.pack(pady=10)
        self.input_bar.pack(pady=20)
        self.output_box_1.pack(pady=20)
        self.output_box_2.pack(pady=20)
        self.button_3.pack()
        
    def runLoop(self):
        self.window.mainloop()

    def getInputChar(self):
        inp = self.input_bar.get()
        
        try:
            ord(inp)          #       check if input is single ASCII char
            input = inp
        except:
            input = None
        
        return input
    
    #Tihs only corresponds to Arduino Code, hence it is not configured as BT-Keyboard
    def setInputChar(self, char):
        self.output_box_1.config(text=f"{char}")

    def clear_input(self):
            self.input_bar.delete(0, 'end')


    def button_handler(self,whichBut: Button , txt:str, cmd)->None:
       
        self.input_bar.focus_set()
        whichBut.configure(text= txt, command= cmd)

    def delay(self, delayT):
        self.window.after(delayT)
    

        



#gu = Gooey()
# gu.button_handler("getcha", gu.getInputChar)
#gu.runLoop()