from time import sleep
from fsm import states
from GUI import Gooey 
from excelHandler import createExcelSheet, fillList
# from test_unit import TestUnit
from serial import Serial

class TestUnit(object):
    def __init__(self) -> None:
        
        self.inChar = ''
        self.idx = 0

        self.sheet = createExcelSheet(path='./sprachtabelle.xlsx' , activeSheet=0)  #   './ascii-tablle.xlsx'
        self.inDict = fillList(num_column=2, char_column=3, sheet=self.sheet) 
        self.keyList = list(self.inDict)                                             # num index of dict.

    def compare(self) -> bool:
        testNum = self.keyList[self.idx]

        if self.inChar == self.inDict[ testNum  ]:
            print('yay')
            return True
        
        else:
            print('nay')
            return False

# print(tu.inDict.keys())




# while 1:
#     if states[state_cnt] == 'tot_cnt':
#         state_cnt = 0
#     else:    
#         states[state_cnt]()
#         state_cnt += 1
    
#     sleep(1)



arr = ['a', 'A', 'b']

if __name__ == "__main__":
    states[0]()
    tu = TestUnit()
    ser = Serial(baudrate=115200, port='/dev/ttyUSB0', timeout=5)
    if ser.is_open() is True:
        ser.write('100')
        
        gu = Gooey()

        print(ser.read())

    tu.inChar = gu.getInputChar()
    print(tu.inChar)



#     def exit(self):

#         return super().exit()




#     tu = TestUnit()
#     serialDevice = Serial()    
    
#     Init().run(tu, serialDevice)
    
#     print(tu.inDict)
#     states[0]
    
#class Init(State):
#    def __init__(self) -> None:
#        super().__init__()
#
#    def run(self, testunit,  serialobj) -> None:
#        sheet = createExcelSheet(path='./ascii-table.xlsx', activeSheet=0)
#        testunit.inDict = fillList(num_column=2, char_column=3, sheet=sheet)          
#        
#        #   this chunck could also be called at definition
#        serialobj.baudrate = 115200
#        serialobj.port = '/dev/ttyUSB0'
#        serialobj.open()
#    
#        if serialobj.is_open:
#            exit()
#