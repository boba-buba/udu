import csv
import pandas as ps
from statements_insrt import insert_statement, insert_multi
#journal name,issue,volume,year,page number,page index,image number,caption,area in percentage,x1,y1,x2,y2,image

file = r"C:\Users\ncoro\udu\csv_parser\csv_files\Volné směry_XXXVII_1_data.csv"

with open(file, 'r', encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=';')

    first_row = next(reader)
    insert_statement(first_row)
    insert_multi(first_row)
    for row in reader:
        insert_multi(row)
    f.flush()


