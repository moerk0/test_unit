class Character:
    def __init__(self, name) -> None:
        self.health = 100
        self.name = None

    
    def getHealth(self):
        print(self.health)
    
    def getName(self):
        print(self.name)


class TestUnit(object):
    
    def __init__(self) -> None:
       # self.fsm = FSM()
        self.var = 'a'

class FSM(TestUnit):
    def __init__(self) -> None:
        super().__init__()
        self.y = 20
    
    def doNothing():
        pass
    def getVar(self):
        return super().var

class State(FSM):
    def __init__(self, argument) -> None:
        self.fsm = argument
        self.x = 10

    def doSthg(self):
        print("doing somthing")




class Init(State, FSM):
    def __init__(self, argument) -> None:
        super().__init__(argument)

tu = TestUnit()

i = Init(FSM)
i.doNothing
print(i.var)