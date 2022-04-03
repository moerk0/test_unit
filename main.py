
from GUI import Gooey 
from excelHandler import Excel
from test_unit import TestUnit
from serialHandler import SerialCom
import asyncio

#async def run_gui(gui):


def prepare():

 # It is working but: veeeeeeeeery sketchy in the Forum they say: use Multithreading!
    gu.window.update()  # top of the flop: Gooey is not well inherited … …
##########################
    if gu.running is True:
        gu.button_handler('end', aborted)
        
        if tu.getNextNum() != 0:
            states['send']()
        else:
            states['finished']()
    else:
        gu.button_handler('send', send)
       

def send():
    gu.running = True

    print(f"State: send: {tu.getNextNum()}")
    gu.delay(1000)
    states['passed']()

def test():
    print("State: test")

def passed():
    print("State: passed")
    states['prepare']()

def failed():
    print("State: failed")

def aborted():
    gu.output_box_1.config(text='test suspended, Continue?')
    gu.running = False
    states['prepare']()

def finished():
    gu.output_box_1.config(text= 'fini')
    gu.output_box_2.config(text= f'saving output to:{None}')

states = {
    'init': True,                       # This is a bool because I need the objects globally accessable
    'prepare':  prepare,
    'send':        send,
    'test':        test,
    'passed':    passed,
    'failed':    failed,
    'aborted':  aborted,
    'finished':finished,
    'error': "unexpected error occured"
}




if __name__ == "__main__":
    
    gu = Gooey()
    
    ## command out to dry run
    try:
        ex = Excel('./sprachtabelle.xlsx', 'Französisch',2 ,3)
        tu = TestUnit(ex.getDict())
        gu.output_box_2.config(text=f"selected lang:{ex.sheet.title}, fetched {len(tu.inDict)} entries")
    except:
        gu.output_box_2.config(text="could not open, bad path?")
        states['init'] = False

    try:
        ardu = SerialCom('/dev/ttyUSB0', 115200)
        gu.output_box_1.config(text=f"Port: {ardu.port} openend")
    except:
        gu.output_box_1.config(text="bad port, please restart")
        states['init'] = False
    ##

    if states['init'] is True:
        states['prepare']()

#This task get suspended
    gu.runLoop()



