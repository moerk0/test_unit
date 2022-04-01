from tkinter import *


class Gooey:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("gooey for test unit")
        self.button = Button(self.window, text='retrieve input', width=25, command=lambda: self.getInputChar())
        self.input_bar = Entry(self.window)
        self.output_box = Label(self.window, text='this is an output box')

        self.input_bar.pack()
        self.output_box.pack()
        self.button.pack()
        self.window.mainloop()

    def getInputChar(self):
        inp = self.input_bar.get()
        
        try:
            ord(inp)          #       check if input is single ASCII char
            input = inp
        except:
            TypeError
            inp = "no char or too many chars recieved"
            input = None
        
        self.output_box.config(text=f"{inp}")
        return input
    
    def clear_input(self):
            self.input_bar.delete(0, 'end')

    #def buttonhandler(self):
        
    


gui = Gooey()