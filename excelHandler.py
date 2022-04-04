from  openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import Color
from dataclasses import dataclass

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
                print(f"{n} is no integer. Skipping")

        return l


    def createResultFile(self):
        """Create Sheets for all Languages listed in langugaes 
        then check if the file already exists. If yes open if no create"""
        
        try:
            self.workbook_result = load_workbook(self.outFile)

        except:
            self.workbook_result = Workbook()
            l = list(self.languages.keys())
            self.workbook_result.active.title = l[0]
            for i in range(1,len(l)):
                self.workbook_result.create_sheet(title= f'{l[i]}')
        
        
        # 
        self.workbook_result.active = self.languages[self.lang]
        self.sheet_result = self.workbook_result.active
        self.sheet_result.append(['num','expected Char', 'recieved Char', 'passed'])
        

    def writeResults(self, results):
        length = len(results)

        # Color Section assuming that the last value will be the test result
        red = Color(index=2)
        green = Color(index=3)
        color_col = 4
        index_of_passed = 3                   # The 4th val returned by DataClass
        
        # counter 
        i = 0
        row = 2 # assuming that the first Row of the file fits the headers

        while i < length:
            data = list(results[i].content())
            self.sheet_result.append(data)

            if data[index_of_passed] is True:
                col = green
            else: 
                col = red

            self.sheet_result.cell(column = color_col, row = row).fill = PatternFill(patternType='solid',fgColor=col)
            row +=1
            i += 1
       
    def saveResultFile(self):
        self.workbook_result.save(filename= self.outFile)
       

      




   



# ex = Excel('./sprachtabelle.xlsx', 'Französisch', 2,3)
# ex.createResultFile()
# ex.writeResults(ex.getTestData())
# ex.saveResultFile()
