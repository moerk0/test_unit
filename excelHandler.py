import openpyxl

def createExcelSheet(path, activeSheet):

    """Active Sheet is the numerical index of all sheets, for US-ENG its 0,for french 1, etc."""

    workbook = openpyxl.load_workbook(filename=path, data_only=True)            
    workbook.active = activeSheet
    sheet = workbook.active
    print(f"availablue sheets: {workbook.sheetnames}")
    print(f"selected sheet: {sheet.title}")
    return sheet

def fillList(num_column, char_column, sheet):
        row_cnt = sheet.max_row
        print(f"Max Rows: {row_cnt}")
        l = {}

        for row in range(1, row_cnt):
            c = sheet.cell(row=row, column=char_column)
            n = sheet.cell(row=row, column=num_column)
            c = c.value
            n = n.value
            try:
                l[int(n)] = c
            except:
                ValueError
                print(f"{n} is no integer. Skipping")

        return l


# sheet = createExcelSheet(path='./goBraille Sprachtabelle.xlsx', activeSheet=3)
# c = sheet.cell(row=3, column=3)
# print(fillList(2,3,sheet))
