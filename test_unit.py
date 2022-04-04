from excelHandler import Excel


class TestUnit(object):
    def __init__(self, testdata) -> None:
        self.idx = 0

        self.testdata = testdata     #object that Holdes: num   expected    recieved    passed


    def compare(self) -> bool:
        

        if self.testdata[self.idx].expected == self.testdata[self.idx].recieved:
            self.testdata[self.idx].passed = True
            return True
        
        else:
            return False

    def count_idx(self)-> bool:

        if self.idx < len(self.testdata):        # Check if idx is in bound
            self.idx+=1
            return True
        else:
            return False

    def getNextNum(self):
        return self.testdata[self.idx].num

    def getChar(self, c):
        self.testdata[self.idx].recieved = c

    def getTestValues(self):
        for i in range(len(self.testdata)):
            print(f"{self.testdata[i].content()}")

        return self.testdata


# ex = Excel('./sprachtabelle.xlsx', 'Französisch',2 ,3)
# tu = TestUnit(ex.getTestData())
# # print(type(tu.testdata))
# # tu.getTestValues()
# # tu.getChar('a')
# print(tu.testdata[0].content())
# # print(tu.getTestValues())