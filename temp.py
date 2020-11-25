import openpyxl

book = openpyxl.Workbook()

sheet = book.active
sheet.title = "sheet"

# The data
cell = sheet._get_cell(1, 1).value = 'syidbuon'
sheet.column_dimensions['A'].width = 60


book.save(filename = "test.xlsx")
