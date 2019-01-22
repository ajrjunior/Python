import xlwt
from datetime import datetime

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(9, 0, 1234.56, style0)
ws.write(8, 0, datetime.now(), style1)
ws.write(6, 0, 2)
ws.write(6, 1, 3)
ws.write(6, 2, xlwt.Formula("A3+B3"))

wb.save('example1.xls')
