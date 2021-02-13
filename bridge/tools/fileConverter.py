import csv
from xlsxwriter.workbook import Workbook


def CSVtoXLSX(csv_path):
    xlsx_path = csv_path[:-4] + '.xlsx'
    workbook = Workbook(xlsx_path)
    worksheet = workbook.add_worksheet()
    with open(csv_path, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()
    return xlsx_path

