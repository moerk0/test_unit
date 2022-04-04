
class TestUnit(object):
    def __init__(self, inDict) -> None:
        self.inChar = ''
        self.idx = 0

        self.inDict = inDict
        self.keyList = list(self.inDict)    # num index of dict.
        self.nextNum = self.keyList[self.idx] # Initialise the first Entry in the dict

    def compare(self) -> bool:
        

        if self.inChar == self.inDict[ self.nextNum  ]:
            return True
        
        else:
            return False

    def getNextNum(self):
        if self.idx < len(self.keyList):        # Check if idx is in bound
            self.nextNum = self.keyList[self.idx]
            self.idx+=1
            
        else:
            self.nextNum = 0

        return self.nextNum

   

