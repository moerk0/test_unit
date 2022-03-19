from socket import timeout
from fsm import State, FSM
from excelHandler import createExcelSheet, fillList
from test_unit import TestUnit


class Init(State):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        sheet = createExcelSheet(path='./ascii-table.xlsx', activeSheet=0)
        tu.inList = fillList(num_column=2, char_column=3, sheet=sheet)          


if __name__ == "__main__":

    tu = TestUnit()
    
    Init.run(tu)

    print(tu.inList)
    
