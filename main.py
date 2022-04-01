
from GUI import Gooey 
from excelHandler import Excel
from test_unit import TestUnit
from serialHandler import SerialCom

def init():
   
    print("State: ini")

def wait4start():
    gu.button.configure(text= 'start Test', command= send)
    print("State: w4s")

def send():
    if tu.idx < len(tu.keyList):
        num = tu.keyList[tu.idx]
        tu.idx+=1
        print(f"State: send: {num}")
        
        gu.window.after(200)
        states['passed']
    else:
        gu.output_box_1.config(text="finished")

def test():
    print("State: test")

def passed():
    print("State: passed")
    states['send']

def failed():
    print("State: failed")


states = {
    'init': True,                       # This is a bool because I need the objects globally accessable
    'w4start':lambda: wait4start(),
    'send': lambda:send(),
    'test': lambda:test(),
    'passed': lambda:passed(),
    'failed': lambda:failed(),
    'error': "unexpected error occured"# Not gonna happen :D
}

if __name__ == "__main__":
    
    gu = Gooey()
    
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

    
    if states['init'] is True:
        states['w4start']()


    gu.runLoop()
