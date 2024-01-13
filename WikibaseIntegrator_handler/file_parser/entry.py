import csv
import pandas as ps
from data_handler import process_first_row
from data_handler import process_row 
#journal name,issue,volume,year,page number,page index,image number,caption,area in percentage,x1,y1,x2,y2,image,width_page,height_page,language
#number of pages

def parse_pages(file_name):
    pages = {}
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                pages[row['page number']] = row['image number']
        return pages
    except:
        print("File error")
        return pages



def parse_csv(file_name):

    page_images = parse_pages(file_name)
    if (len(page_images) == 0):
        return

    with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        first_row = next(reader)
        process_first_row(first_row)

        process_row(first_row, page_images)
        for row in reader:
            process_row(row, page_images)
        f.flush()


#parse_csv(r"C:\Users\ncoro\udu\csv_parser\csv_files\1901_Deutsche_Kunst_und_Dekoration_data.csv", 'de')
parse_csv(r"C:\Users\ncoro\udu\csv_parser\csv_files\Volne smery_XXX_data.csv")