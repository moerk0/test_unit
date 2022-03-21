class State:
    def __init__(self) -> None:
        self.complete = False
        self.timeout = 10

    def run(self):
        pass

    def next(self, input):
        pass


class StateMachine:
    def __init__(self) -> None:
       self.states = {}
       self.currentState = None
       
       self.transitions = {}
       self.trans = None

    def add_state(self, name, state, end_state=0):
        name = name.upper()
        self.states[name] = state

    def set_state(self, stateName):
        self.currentState = self.states[stateName]
    
    def set_trans(self, transName):
        self.trans = self.transitions[transName]
    


    def run(self):
      if(self.trans):
          self.trans.run
            

class Start(State):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        print("Start")

    def next(self, input):
        if input == 0:
            print("zero")
        else:
            print("not Zero")
        
class Fini(State):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        print("End")
    
    def next(self, input):
        return ActualMachine.end

class ActualMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__(ActualMachine.start)

ActualMachine.start = Start()
ActualMachine.end = Fini()

i = StateMachine()
i.add_state("start", State)
i.add_state("quit", Fini)

