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
            if n is not None and n.isdigit():
                l[c] = int(n)

        return l