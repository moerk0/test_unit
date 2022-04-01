def init():
   
    print("State: ini")

def wait4start():
    print("State: w4s")

def send(testUnit):

    print(f"State: send")

def test():
    print("State: test")

def passed():
    print("State: passed")

def failed():
    print("State: failed")


states = {
    0: init,
    1: wait4start,
    2: send,
    3: test,
    4: passed,
    5: failed,
    6: 'tot_cnt'
}

state_cnt = 0
