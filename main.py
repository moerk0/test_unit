
from GUI import Gooey 
from excelHandler import Excel
from test_unit import TestUnit
from serialHandler import SerialCom



def prepare():

 # It is working but: veeeeeeeeery sketchy in the Forum they say: better use Multithreading!
    gu.delay(5)
    gu.window.update() 
    

    if gu.running is True:                  
        gu.button_handler('abort', aborted)   

                          #
           
        if tu.count_idx() is not False:                 #
            states['send']()                # Little Nest
        else:                               #
            states['finished']()            #
    
    else:
        gu.button_handler('send', send)
       

def send():
    
    # Set true after the button is pushed
    if gu.running is not True:
        gu.running = True
    
    
    ardu.writeNum(tu.getNextNum())

    print(f"State: send: {tu.getNextNum()}")
    gu.delay(5)
    #tu.getChar(ardu.readChar())
    
    tu.getChar(gu.getInputChar())
    gu.window.update()


    gu.window.update()

    states['test']()

def test():
    tu.compare()
    print(tu.testdata[tu.idx].content())
    
    states['prepare']()



def aborted():
    gu.output_box_1.config(text='test suspended, Continue?')
    gu.running = False
    states['prepare']()

def finished():
    gu.output_box_1.config(text= 'fini, again?')
    gu.output_box_2.config(text= f'saving output to:{None}')
    tu.idx = 0


states = {
    'init': True,                       # This is a bool because I need the objects globally accessable
    'prepare':  prepare,
    'send':        send,
    'test':        test,
    'aborted':  aborted,
    'finished':finished,
    'error': "unexpected error occured"
}




if __name__ == "__main__":
    
    gu = Gooey()
    
    ## command out to dry run
    try:
        ex = Excel('./sprachtabelle.xlsx', 'Französisch',2 ,3)
        tu = TestUnit(ex.getTestData())
        gu.output_box_2.config(text=f"selected lang:{ex.sheet.title}, fetched {len(tu.testdata)} entries")
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

#This task gets suspended
    gu.runLoop()



