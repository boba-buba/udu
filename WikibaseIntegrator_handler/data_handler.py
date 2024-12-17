import sys
import magazine_handler
import volume_handler
import issue_handler

import page_handler
import reproduction_handler
import caption_handler

import json
import time
from datetime import datetime

"""
Parse input data from ImageExtractor application. Parse and process 
data for insertion into PhotoReproMatrix DB.

From the first row we get magazine, volume and issue. Then we 
process pages, reproductions, captions altogether.

"""
magazine = magazine_handler.Magazine()
volume = volume_handler.Volume()
issue = issue_handler.Issue()
page = page_handler.Page()
repro = reproduction_handler.Repro()
caption = caption_handler.Caption()


def parse_date(data: list[str]) -> dict[str, str]:
    """
    Parse date and create format for Wikibase
    """
    #yyyy mm dd
    dates_dict = {}
    if len(data) == 6: #yyyy mm dd yyyy mm dd
        dates_dict["precision"] = 11
        dates_dict["start"] = f"+{data[0]}-{data[1]}-{data[2]}T00:00:00Z"
        dates_dict["end"] = f"+{data[3]}-{data[4]}-{data[5]}T00:00:00Z"
    return dates_dict


def compare_and_change_date(date: dict[str, str]):
    """Compare publication date of the volume with the date from the db and if the start date is earlier or end date is later then change it in db."""
    # getting here start and end date
    qid = str(volume.volume_qid)
    q='SELECT ?start ?end WHERE { wd:' + qid + ' wdt:P31 ?start. wd:' + qid +' wdt:P32 ?end. SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}'
    result = volume.volume_general_query(q)

    json_format = json.dumps(result[0])
    python_f = json.loads(json_format)

    start = python_f['start']['value'][:10].split('-')
    end = python_f['end']['value'][:10].split('-')
    new_start = date['start'][1:11].split('-')
    new_end = date['end'][1:11].split('-')

    start_date = datetime(int(start[0]), int(start[1]), int(start[2]))
    end_date = datetime(int(end[0]), int(end[1]), int(end[2]))
    new_start_date = datetime(int(new_start[0]), int(new_start[1]), int(new_start[2]))
    new_end_date = datetime(int(new_end[0]), int(new_end[1]), int(new_end[2]))


    # compare  if volume.start > date.start and if volum.end < date.end
    new_info = {"precision" : 11}
    if (new_start_date < start_date):
        new_info["start"] = date['start']
    if (new_end_date > end_date):
        new_info["end"] = date['end']
    # if needed  volume.update
    if len(new_info) > 1:
        volume.volume_update_date(new_info)


def process_first_row(row: dict[str, str]):
    """Process data from the first row of the csv and based on data add magazine, volume and issue"""
    #insert magazine
    magazine.magazine_name = row["journal_name"]
    if (magazine.magazine_in_db() == -1):
        magazine.magazine_insert_new(row["language"])
        magazine.magazine_in_db()
        print("magazine " + magazine.magazine_name + " was inserted.")
    # else:
        # print(f"Magazine already in db")

    #insert volume
    volume_id = row["volume"]
    if volume_id == "":
        volume_id = "None"

    volume.volume_title = magazine.magazine_name + ", vol. " + volume_id

    result = row['publication_date'].split("-") #check for 2 elements
    volume_data = {}

    volume_data["vol_number"] = volume_id
    volume_data["title"] = volume.volume_title
    while  magazine.magazine_in_db() == -1:
        time.sleep(2.5)
        magazine.magazine_in_db()
    volume_data["magazine_numeric_id"] = int(magazine.magazine_qid[1:])
    if volume.volume_in_db() == -1:
        volume_data.update(parse_date(result))
        volume.volume_insert_new(volume_data, row["language"])
        volume.volume_in_db()
        print("volume " + volume.volume_title + " was inserted.")
    else:
        compare_and_change_date(parse_date(result))
        # print(f"Volume is already in db")

    #insert issue
    issue_data = parse_date(result)

    if row["issue"] == "":
        issue.issue_title = volume.volume_title + ', issue 1-12'
        issue_data["issue_number"] = '1-12'
    else:
        issue.issue_title = volume.volume_title + ', issue ' + row['issue']
        issue_data["issue_number"] = row["issue"]

    issue_data["issue_title"] = issue.issue_title
    while volume.volume_in_db() == -1:
        time.sleep(2.5)
        volume.volume_in_db()
    issue_data["volume_numeric_id"] = int(volume.volume_qid[1:])
    issue_data["lang"] = row["language"]
    issue_data.update({"author": row["author"], "publisher": row["publisher"],
                     "contributor": row["contributor"]})

    if issue.issue_in_db() == -1:
        issue.issue_insert_new(issue_data, issue_data["lang"])
        print("issue " + issue.issue_title + " was inserted.")
    # else:
    #     print(f"Issue already in db")


#journal_name;issue;volume;publication_date;page_number;page_index;page_width;page_height;language;img_address;author;publisher;contributor
def insert_page_row(row: dict[str, str], page_num_of_repro: str, page_id: str):
    """Parses page row from csv file and inserts page into the database if page is not there"""

    #print(magazine.magazine_qid, volume.volume_qid, issue.issue_qid)

    # preparation steps
    iss_vol_numeric_id = issue.issue_in_db()
    while (iss_vol_numeric_id == -1):
        iss_vol_numeric_id = issue.issue_in_db()
    page_title = issue.issue_title + ", p. " + page_id


    # page insert     data = page_title, page_number, page_index, num_of_repro, has_text, iss_vol_numeric_id, page_width, page_height


    page.page_title = page_title
    if page.page_in_db() == -1:
        page_data = {"page_title": page_title, "page_number" : row["page_number"], "page_index" : row["page_index"], 
                    "num_of_repro" : page_num_of_repro, "iss_vol_numeric_id" : int(iss_vol_numeric_id[1:]),
                    "height_page" : row["page_height"], "width_page" : row["page_width"], "img_address": row["img_address"]}

        page.page_insert_new(page_data, row["language"])
        page.page_in_db()
        print("page " + page.page_title + " was inserted.")
    # else:
    #     print("page already in db")

    #del page_num_of_repro[row[page_id]]



#journal_name;issue;volume;publication_date;page_number;page_index;image_number;caption;area_in_percentage;x1;y1;x2;y2;image;width_page;height_page;language;.img_address;author;publisher;contributor
def parse_reproductions(row: dict[str, str]):
    """ Parse one row and insert reproduction into the db, if it is not there already """
    width = abs(int(row['x1']) - int(row['x2']))
    height = abs(int(row['y1']) - int(row['y2']))

    page_id = row["page_number"]
    if page_id == "":
        page_id = row["page_index"]
    page.page_title = issue.issue_title + ", p. " + page_id
    page_qid = page.page_in_db()
    while (page_qid == -1):
        time.sleep(2.5)
        page_qid = page.page_in_db()

    repro.repro_title = page.page_title + ", repro " + row["image_number"]
    if repro.repro_in_db() == -1:

        repro_data = {"repro_title" :  repro.repro_title, "area" : row["area_in_percentage"], "on_page" : int(page_qid[1:]), "x1" : row["x1"], "y1" : row["y1"],
                     "x2" : row["x2"], "y2": row["y2"], "width" : width, "height" : height, "img_address": row["img_address"]}
        repro.repro_insert_new(repro_data, row["language"])
        repro.repro_in_db()
        print("repro " + repro.repro_title + " was inserted.")
    # else: print("repro already in DB")

def clean_caption(text: str) -> str:
    result = ""
    for c in text:
        if c.isalpha() or c in ['-', '.', '!', '?', ' ']:
            result += c
            #print(ord(c), c)
    return result

def parse_captions(row: dict[str, str], log_file):
    """ Parse reproduction row and if there the caption is not empty insert the new caption into the db (if not already in db). """
    # caption insert #data = { caption_title, text, on_page, repro}
    if row["caption"] != "":
        page_id = row["page_number"]
        if page_id == "":
            page_id = row["page_index"]
        page.page_title = issue.issue_title + ", p. " + page_id
        page_qid = page.page_in_db()
        while (page_qid == -1):
            time.sleep(2.5)
            page_qid = page.page_in_db()

        repro.repro_title = page.page_title + ", repro " + row["image_number"]
        repro_qid = repro.repro_in_db()
        while (repro_qid == -1):
            repro_qid = repro.repro_in_db()

        caption.caption_title = repro.repro_title + ", caption"
        if caption.caption_in_db() == -1:
            text_max_400_chars = row["caption"]
            # if len(text_max_400_chars) >= 400:
            #     text_max_400_chars = text_max_400_chars[:390]

            # text_max_400_chars = clean_caption(text_max_400_chars)
            if len(text_max_400_chars) > 0 and any(c.isalpha() for c in text_max_400_chars):
                caption_data = {"caption_title" : caption.caption_title, "text" : text_max_400_chars, "on_page" : int(page.page_qid[1:]), "repro" : int(repro_qid[1:])}
                try:
                    caption.caption_insert_new(caption_data, row["language"])
                    print("caption " + caption.caption_title + " was inserted.")
                except:
                    log_file.write("Caption:\n")
                    log_file.write(text_max_400_chars+'\n')
                    log_file.write("On page:\n")
                    log_file.write(page.page_title+'\n')
                    log_file.write("Reproduction:\n")
                    log_file.write(repro.repro_title+'\n')
                    log_file.write("\n\n")
                    #print("Caption " + text_max_400_chars + " was not inserted. INSERT MANUALLY.")







