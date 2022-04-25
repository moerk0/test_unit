from abc import ABC
from dataclasses import dataclass


@dataclass
class State(ABC):
    def run(self) -> int:
        print(f"Running: {self}")
        return 0

    def next(self) -> object:
        print(f"Transitioning from {self}")


class Prepare(State):
    def __init__(self) -> None:
        super().__init__()

    def run(
        self,
    ) -> int:
        return super().run()

    def next(self) -> State:
        super().next()
        return Send()


class Send(State):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> int:
        return super().run()

    def next(self) -> State:
        super().next()
        return Test()


class Test(State):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> int:
        return super().run()

    def next(self) -> State:
        super().next()
        return Prepare()


class Finished(State):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> int:
        return super().run()

    def next(self):
        super().next()


@dataclass
class Statemachine(ABC):
    def __init__(self, state):
        self.current_state: State = state
        self.current_state.run()

    def runAll(self):
        state: State = self.current_state
        cnt = 0
        while True:
            if (state := state.next()) != None:
                state.run()

            elif (state := state.next()) == Prepare:
                idx += 1
                state.run()

            else:
                break


class TestUnit(Statemachine):
    def __init__(self):
        super().__init__(Prepare())


# print(type(Prepare().next()))
# print(type(Send().next()))
# print(type(Test().next()))
# print(type(Finished().next()))

state = Prepare()


tu = TestUnit()
tu.runAll()
