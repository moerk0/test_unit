# from excelHandler import Excel, TestData




class TestUnit(object):
    """
    this object collects the testdata that is returned from the ExcelHandler.
    testdata is a list of Objects containing:
    num     expectedChar    recievedChar    passed

    further it is managing the index of the test. 
    Therefore it knows when the test run is completed
    in the future it would be nice if this object knows the contents and vars of Data already
    but I Don't know how to make that happen. especialy looking at the excel handler

     """
    def __init__(self, testdata) -> None:
        self.idx = -1
        self.testdata = testdata  #object that Holdes: num   expected    recieved    passed
        self.running = False


    def compare(self) -> bool:
        

        if self.testdata[self.idx].cha == self.testdata[self.idx].received:
            self.testdata[self.idx].passed = True
            return True
        
        else:
            return False

    def count_idx(self)-> bool:
        self.idx +=1
        
        if self.idx < len(self.testdata):        # Check if idx is in bound
            return True
        else:
            return False


    def setChar(self, c):
        print(c)
        self.testdata[self.idx].received = c
   
    def getNextNum(self):
        return self.testdata[self.idx].num

    def getResults(self):
        return self.testdata



#ex = Excel('./sprachtabelle.xlsx', 'Französisch',2 ,3)
#tu = TestUnit(ex.getTestData())
#print(type(tu.testdata))
#tu.getTestValues()
#tu.setChar('a')
#print(tu.testdata[0].content())
#print(tu.getTestValues())