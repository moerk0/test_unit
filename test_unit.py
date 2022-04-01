
class TestUnit(object):
    def __init__(self, inDict) -> None:

        self.inChar = ''
        self.idx = 0

        self.inDict = inDict
        self.keyList = list(self.inDict)    # num index of dict.

    def compare(self) -> bool:
        testNum = self.keyList[self.idx]

        if self.inChar == self.inDict[ testNum  ]:
            print('yay')
            return True
        
        else:
            print('nay')
            return False

