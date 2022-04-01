import openpyxl

class Excel:
    def __init__(self, filename, lang, num_column, char_column) -> None:
        
        self.languages = {          # TODO: Automate recognition process
            'US-Englisch' : 0,
            'Französisch' : 1,
            'Spanisch' : 2,
            'Italienisch' : 3,
            'Türkisch' : 4
        }

        self.workbook_origin = openpyxl.load_workbook(filename=filename, data_only=True)
        self.workbook_origin.active = self.languages[lang]
        self.sheet = self.workbook_origin.active
        
        self.workbook_result = None # This represents the resuls table
        # not yet
        # implemented

        self.num_column = num_column        # Where to find the in Numbers 
        self.char_column = char_column      # Where to find the out Chars

        
    def getDict(self):
        row_cnt = self.sheet.max_row + 1    # I don't know why plus eins
        print(f"Max Rows: {row_cnt}")
        d = {}

        for row in range(1, row_cnt):
            c = self.sheet.cell(row=row, column=self.char_column)
            n = self.sheet.cell(row=row, column=self.num_column)
            c = c.value
            n = n.value
            try:
                d[int(n)] = c
            except:
                ValueError
                print(f"{n} is no integer. Skipping")

        return d

#ex = Excel('./sprachtabelle.xlsx', 'US-Englisch', 2,3)
#ex.getDict()

