from  openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import Color
from dataclasses import dataclass


# The header of the output file. Modify if need.
values = {'num':0, 'expected':1, 'received':2, 'passed':3}

@dataclass
class TestData:
    """
    Famous Data Class. Each one object holds one Row of ExcelTable.
    Initially there will be 2 filled out, the program will fill out the last 2 entries
    """

    num: int
    expected: str
    received: str = None
    passed: bool =  False
    
    def content(self):
        return self.num, self.expected, self.received, self.passed
    


class Excel:
    def __init__(self, filename, lang, num_column, char_column) -> None:
        
        self.languages = {          # TODO: Automate recognition process
            'US-Englisch' : 0,
            'Französisch' : 1,
            'Spanisch' : 2,
            'Italienisch' : 3,
            'Türkisch' : 4
        }
        
        self.lang = lang

        self.workbook_origin = load_workbook(filename=filename, data_only=True)
        self.workbook_origin.active = self.languages[lang]
        self.sheet = self.workbook_origin.active
        
        self.num_column = num_column        # Where to find the in Numbers 
        self.char_column = char_column      # Where to find the out Chars
        
        
        self.outFile = f'{filename[:-5]}_results.xlsx'


    def getTestData(self):
        self.row_cnt = self.sheet.max_row + 1    # I don't know why plus eins
        print(f"Max Rows: {self.row_cnt}")
        l = []

        for row in range(1, self.row_cnt):
            c = self.sheet.cell(row=row, column=self.char_column)
            n = self.sheet.cell(row=row, column=self.num_column)
            c = c.value
            n = n.value
            try:
                l.append(TestData(int(n), str(c)))
            except:
                ValueError
                print(f"Row:{row} - {n} is no integer. Skipping")

        return l


    def createResultFile(self):
        """check if the file already exists. If yes load 
        if no create empty file with languages"""
        
        try:
            self.workbook_result = load_workbook(self.outFile)

        except:
            l = list(self.languages.keys())                         #   Create list of Languages
            h = list(values.keys())                                 #               of Headers

            self.workbook_result = Workbook()                       #   Open new Workbook
            self.workbook_result.active.title = l[0]                #   change title of first sheet
            self.workbook_result.active.append(h)                   #   write Header to in the first line

            for i in range(1,len(l)):                               #   create new sheets and write header
                self.workbook_result.create_sheet(title= f'{l[i]}')
                self.workbook_result.active = i
                self.workbook_result.active.append(h)
        
        
        #select current language
        self.workbook_result.active = self.languages[self.lang]
        self.sheet_result = self.workbook_result.active


    def writeResults(self, results):
        len_res = len(results) + 1

        # Color Section
        red = Color(index=2)
        green = Color(index=3)
        yellow = Color(index=5)
        white = PatternFill(fill_type=None)
        
        # iterator for data.
        i = 0

        for cols in self.sheet_result.iter_rows(min_row = 2, max_row = len_res):
            data = list(results[i].content())
            
            cols[0].value = data[values['num']]
            cols[1].value = data[values['expected']]        
            cols[2].value = data[values['received']]        
            cols[3].value = data[values['passed']]

            # color for passed
            if data[values['passed']] is True:
                color = green
            else: 
                color = red
            
            cols[values['passed']].fill = PatternFill(patternType='solid',fgColor=color)

            # color in case that No data has been received during test
            if data[values['received']] is None:
                cols[values['received']].fill = PatternFill(patternType='solid',fgColor=yellow)
            else:
                cols[values['received']].fill = white


            i += 1
       
    def saveResultFile(self):
        self.workbook_result.save(filename= self.outFile)
       



# ex = Excel('../test_unit/sprachtabelle.xlsx', 'Französisch', 2,3)
# ex.createResultFile()
# ex.writeResults(ex.getTestData())
# ex.saveResultFile()
