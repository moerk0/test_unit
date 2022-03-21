from fsm import State, FSM
from excelHandler import createExcelSheet, fillList
from test_unit import TestUnit
from serial import Serial

class Init(State):
    def __init__(self) -> None:
        super().__init__()

    def run(self, testunit,  serialobj) -> None:
        sheet = createExcelSheet(path='./ascii-table.xlsx', activeSheet=0)
        testunit.inList = fillList(num_column=2, char_column=3, sheet=sheet)          
        
        #   this chunck could also be called at definition
        serialobj.baudrate = 115200
        serialobj.port = '/dev/tty0'
        serialobj.open()
    
        if serialobj.is_open:
            exit()


    def exit(self):

        return super().exit()


if __name__ == "__main__":

    tu = TestUnit()
    serialDevice = Serial()    
    
    Init().run(tu, serialDevice)
    
    print(tu.inList)
  
    
