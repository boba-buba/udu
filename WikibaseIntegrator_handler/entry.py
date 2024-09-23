import csv
import pandas as ps
from data_handler import process_first_row
from data_handler import insert_page_row, parse_reproductions, parse_captions
#journal name,issue,volume,year,page number,page index,image number,caption,area in percentage,x1,y1,x2,y2,image,width_page,height_page,language
#number of pages

def count_number_of_images_per_page(file_name: str) -> dict[str, str]:
    pages = {}
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if (row["page_number"] == ""):
                    pages[row["page_index"]] = row["image_number"]
                else:
                    pages[row['page_number']] = row['image_number']
        return pages
    except:
        print("File error")
        return pages




def parse_data(pages_csv_file_name: str, repros_csv_file_name: str):
    number_images_per_page = count_number_of_images_per_page(repros_csv_file_name)

    # magazine, volume, issue must be inserted here
    # all pages from pages file inserted here
    with open(pages_csv_file_name, 'r', encoding="utf-8") as pages_file:
        reader = csv.DictReader(pages_file, delimiter=';')

        first_row = next(reader)
        process_first_row(first_row)

        process_page_row(first_row, number_images_per_page)
        for row in reader:
            process_page_row(row, number_images_per_page)
        pages_file.flush()

    #insert roproduvtions and captions
    process_repro_rows(pages_csv_file_name)



#journal_name;issue;volume;publication_date;page_number;page_index;page_width;page_height;language;img_address;author;publisher;contributor
def process_page_row(page_row: dict[str, str], images_per_pages: dict[str, str]):
    # by default number, if number is null then index
    page_id = page_row["page_number"]
    if page_id == "":
        page_id = page_row["page_index"]

    # find repros per page, by default is 0 if page doesnt have any repros
    repros_per_page = "0"
    if page_id in images_per_pages.keys():
        repros_per_page = images_per_pages[repros_per_page]

    insert_page_row(page_row, repros_per_page, page_id)


def process_repro_rows(repros_csv_file_name: str):
    with open(repros_csv_file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            parse_reproductions(row)
        f.flush()

    with open(repros_csv_file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            parse_captions(row)
        f.flush()


pages = r"C:\Users\ncoro\source\repos\udu\csv_parser\csv_files\Le_Bulletin_de_la_vie_artistique_1921_01_2_pages.csv"
repros = r"C:\Users\ncoro\source\repos\udu\csv_parser\csv_files\Le_Bulletin_de_la_vie_artistique_1921_01_2_data.csv"


parse_data(pages, repros)

#parse_csv(r"C:\Users\ncoro\Downloads\1927.10__red_i__1_data.csv")
#parse_csv(r"C:\Users\ncoro\udu\csv_parser\csv_files\Volne smery_XXX_data.csv")