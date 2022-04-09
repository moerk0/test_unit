from operator import index
from  openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import Color
from dataclasses import dataclass


# The header of the output file. Modify if need. TODO: implement it as singleton in TestData
# the passed parameter should always be the last param. The coloring of the file depends on it.
# otherwise change index_of_passed in writeResults()
head = ['num','expected Char', 'recieved Char', 'passed']
len_h = len(head)


@dataclass
class TestData:
    """
    Famous Data Class. Each one object holds one Row of ExcelTable.
    Initially there will be 2 filled out, the program will fill out the last 2 entries
    """

    num: int
    expected: str
    recieved: str = None
    passed: bool =  False
    
    def content(self):
        return self.num, self.expected, self.recieved, self.passed
    


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
        """check if the file already exists. If yes open 
        if no create empty file with languages"""
        
        try:
            self.workbook_result = load_workbook(self.outFile)

        except:
            self.workbook_result = Workbook()
            l = list(self.languages.keys())
            self.workbook_result.active.title = l[0]
            for i in range(1,len(l)):
                self.workbook_result.create_sheet(title= f'{l[i]}')
        
        
        #fetch active workbook
        self.workbook_result.active = self.languages[self.lang]
        self.sheet_result = self.workbook_result.active

        #Write the header (see top line)
        cnt = 0
        for  col_num in self.sheet_result.iter_cols(max_col = len_h, min_row = 1):
            col_num[0].value = head[cnt]
            cnt+=1

    def writeResults(self, results):
        len_res = len(results) + 1

        # Color Section assuming that the last value will be the test result
        red = Color(index=2)
        green = Color(index=3)
        yellow = Color(index=5)
        color_col = 4
        index_of_passed = len_h - 1                   
        
        # iterator for data
        i = 0

        for rows in self.sheet_result.iter_rows(min_row = 2,max_col = 4, max_row = len_res):
            data = list(results[i].content())
            
            rows[0].value = data[0]         # num
            rows[1].value = data[1]         # expected
            rows[2].value = data[2]         # recieved
            rows[3].value = data[3]         # passed

            # color for passed
            if data[index_of_passed] is True:
                col = green
            else: 
                col = red
            rows[index_of_passed].fill = PatternFill(patternType='solid',fgColor=col)

            # color in case that No data has been recieved during test
            if data[2] is None:
                rows[2].fill = PatternFill(patternType='solid',fgColor=yellow)

            i += 1
       
    def saveResultFile(self):
        self.workbook_result.save(filename= self.outFile)
       



# ex = Excel('./sprachtabelle.xlsx', 'Französisch', 2,3)
# ex.createResultFile()
# ex.writeResults(ex.getTestData())
# ex.saveResultFile()
