
import tkinter
#import xldr 	#	?
#import serial
from random import randint
import time


###### Base Objects of FSM

class Transition(object):
	def __init__(self, toState):
		self.toState = toState

	def run(self):
		print("Transitioning")


class FiniteStateMachine(object):
	def __init__(self):
		self.states = {}
		self.transtions = {}
		self.currentState = None
		self.trans = None

	def addState(self, stateName, state):
		self.states[stateName] = state 

	def setState(self, stateName):
		self.currentState = self.states[stateName]

	def transitionState(self, transName):
		self.trans = self.tranistions[transName]

	def addTransition(self, transName, transtion):
		self.transtions[transName] = transtion

	def run(self):
		if(self.trans):
			self.trans.run()
			self.SetState(self.trans.toState)
			self.trans = None
		
		self.currentState.run()


class State(object):
	def __init__(self, FSM) -> None:
		self.FSM = FSM
		self.timer = 0
		self.startTime = 0
	
	# For enter I used some snippet. Don't know what to do with it
	def enter(self):
		self.timer = randint(0,5)
		self.startTime = int(time.clock())

	def run(self):
		pass

	def exit(self):
		print("______________________________")


### States of FSM


class Init(State):
	def __init__(self) -> None:
		super(Init, self).__init__(FiniteStateMachine)
	
	def enter(self):
		super(Init, self).enter() 	#				This the same like the one below?
		print("Establishing Serial Connection,\n Checking For Bluetooth,\n Open Excel")


	def run(self):
		pass
	#do establishing code here

	def exit(self):
		print("All set and done ready to test")
	

class Wait4Input(State):
	def __init__(self) -> None:
		super(Wait4Input, self).__init__(FiniteStateMachine)

	def enter(self):
		super().enter()			#			Same??

	def run(self):
		print("push button to proceed")
		# if button pushed:
		#	proceed
		#	clearOutputWindow()				GUI related
		# else:
		#	pass

	def exit(self):
		print("begin test procedure")


class Send(State):
	def __init__(self) -> None:
		super(Send, self).__init__(FiniteStateMachine)

	def enter(self):
		super().enter()
	
	def run(self):
		print("Send $Num to GoBraille")
		# do goBraille Magic
		print("getTheChar") # Where to store?

	def exit(self):
		print("got it")
		# return inChar
		return super().exit()



class Test(State):
	def __init__(self) -> None:
		super().__init__(FiniteStateMachine)
		self.result = None #	Bool

	def enter(self):
		return super().enter()

	def run(self, inChar=None):
		# getExcelRow of inChar
		# excelNum = getAscii Num of inChar
		# if(excelNum == num):
		# 	result = true
		# else:
		# 	result = false 
		pass

	def exit(self):
		if(self.result):
			self.FSM = "hallo"
		else: 
			super().FSM.trans = "tschüss"
		
		print(super().FSM.trans)
		return super().exit()


class Passed(State):
	def run(self):
		print("""Test passed, state = send""")


class Failed(State):
	def run(self):
		print("""Warning Characters do not match. Expected output :…
		state = Wait4Input""")








# class Char(object):
# 	def __init__(self) -> None:
# 		self.FSM = FiniteStateMachine(self)


if __name__ == "__main__":
	tu = FiniteStateMachine()
	i = Test()
	i.exit()

	
	














	#class FiniteTestMachine(StateMachine): 
##	def __init__(self, initialState): self.currentState = initialState
#
#	init = State("init", initial=True)
#	w84inp = State("wait for input") 
#	send = State("Send inputNum via Serial") 	# and recieve via bluetooth
#	test = State("perform test") 
#	passed = State("Char matches inputNum") 
#	fail = State("Char does not match … expected: …") 
#	error = State("Don't know what's happening") 
#	
#	begin = init.to(w84inp)
#	sendNum = w84inp.to(send)
#	performTest = send.to(test)
#	passedTest = test.to(passed)
#	failedTest = test.to(fail)
#	failedTest = fail.to(error)
#
#	def run(self):
#		assert 0, "run not implemented"
#
#	def next(self, input):
#		assert 0, "next not implemented"
#
#	def runAll(self, inputs):
#		for i in inputs:
#			print(i)
#			self.current_state = self.current_state.next(i)
#			self.current_state.run()
#
#
#
#test_unit = FiniteTestMachine()
#print(test_unit.current_state)
#
#test_unit.begin()
# print(test_unit.is_w84inp)
# test_unit.sendNum()
# print(test_unit.is_w84inp)
# test_unit.runAll(3)


# class StateMachine:
# 	def __init__(self, initialState):
# 		self.currentState = initialState
# 		self.currentState.run()


	
# 	# Template method:
# 	def runAll(self, inputs):
# 		for i in inputs:
# 			print(i)
# 			self.currentState = self.currentState.next(i)
# 			self.currentState.run()

# a = State("huhu")
