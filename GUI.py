from tkinter import *
from turtle import Turtle


class Gooey:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("gooey for test unit")

        self.button = Button(self.window)
        self.running = False
        self.input_bar = Entry(self.window)

        self.output_box_1 = Label(self.window)
        self.output_box_2 = Label(self.window)

        self.input_bar.pack()
        self.output_box_1.pack()
        self.output_box_2.pack()
        self.button.pack()
        
    def runLoop(self):
        self.window.mainloop()

    def getInputChar(self):
        inp = self.input_bar.get()
        
        try:
            ord(inp)          #       check if input is single ASCII char
            input = inp
        except:
            TypeError
        #    inp = "no char or too many chars recieved"
            input = None
        
        self.output_box_1.config(text=f"{inp}")
        return input
    
    #Tihs only corresponds to Arduino Code, hence it is not configured as BT-Keyboard
    def setInputChar(self, char):
        self.output_box_1.config(text=f"{char}")

    def clear_input(self):
            self.input_bar.delete(0, 'end')


    def button_handler(self, txt, cmd):
       
        self.input_bar.focus_set()
        self.button.configure(text= txt, command= cmd)

    def delay(self, delayT):
        self.window.after(delayT)



# gu = Gooey()
# gu.button_handler("getcha", gu.getInputChar)

# gu.runLoop()