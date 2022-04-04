from tkinter import *


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
            msg = inp
        except:
            TypeError
            msg = "no char or too many chars recieved"
            inp = None
        
        self.output_box_1.config(text=f"{msg}")
        return inp
    
    #Tihs only corresponds to Arduino Code, hence it is not configured as BT-Keyboard
    def setInputChar(self, char):
        self.output_box_1.config(text=f"{char}")

    def clear_input(self):
            self.input_bar.delete(0, 'end')


    def button_handler(self, txt, cmd):
        
        self.button.configure(text= txt, command= cmd)

    def delay(self, delayT):
        self.window.after(delayT)



# gu = Gooey()
# gu.setInputChar('a')
# gu.runLoop()