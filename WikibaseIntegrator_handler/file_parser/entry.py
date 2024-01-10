import csv
import pandas as ps
from data_handler import process_first_row
#journal name,issue,volume,year,page number,page index,image number,caption,area in percentage,x1,y1,x2,y2,image


def parse_pages(file_name):
    pages = {}
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                pages[row['page index']] = row['image number']
        return pages
    except:
        print("File error")
        return pages



def parse_csv(file_name, lang='en'):

    page_images = parse_pages(file_name)
    if (len(page_images) == 0):
        return

    with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        first_row = next(reader)
        globals = process_first_row(first_row, lang)

        #insert_multi(first_row, page_images, globals)
        #for row in reader:
        #    insert_multi(row, page_images, globals)
        f.flush()


#parse_csv(r"C:\Users\ncoro\udu\csv_parser\csv_files\1901_Deutsche_Kunst_und_Dekoration_data.csv", 'de')
parse_csv(r"C:\Users\ncoro\udu\csv_parser\csv_files\Volne smery_XXXVII_2_data.csv", 'cs')