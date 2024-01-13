import sys
sys.path.insert(0, r'C:\Users\ncoro\udu\WikibaseIntegrator_handler')
import magazine_handler
import volume_handler
import issue_handler

import page_handler
import reproduction_handler
import caption_handler

import json

"""
Parse input data from ImageExtractor application. Parse and process 
data for insertion into PhotoReproMatrix DB.

From the first row we get magazine, volume and issue. Then we 
process pages, reproductions, captions altogether.

"""

def parse_date(data):
    #yyyy mm dd
    dates_dict = {}
    if len(data) == 1: # only 1 year: start: yyyy
        dates_dict["precision"] = 9
        dates_dict["start"] = f"+{data[0]}-00-00T00:00:00Z"
    elif len(data) == 2: # two years: yyyy yyyy
        dates_dict["precision"] = 9
        dates_dict["start"] = f"+{data[0]}-00-00T00:00:00Z"
        dates_dict["end"] = f"+{data[1]}-00-00T00:00:00Z"
    elif len(data) == 4: #yyyy mm yyyy mm
        dates_dict["precision"] = 10
        dates_dict["start"] = f"+{data[0]}-{data[1]}-00T00:00:00Z"
        dates_dict["end"] = f"+{data[2]}-{data[3]}-00T00:00:00Z"
    elif len(data) == 3: # only one yyyy mm dd
        dates_dict["precision"] = 11
        dates_dict["start"] = f"+{data[0]}-{data[1]}-{data[2]}T00:00:00Z"
    elif len(data) == 6: #yyyy mm dd yyyy mm dd
        dates_dict["precision"] = 11
        dates_dict["start"] = f"+{data[0]}-{data[1]}-{data[2]}T00:00:00Z"
        dates_dict["end"] = f"+{data[3]}-{data[4]}-{data[5]}T00:00:00Z"
    return dates_dict

magazine = magazine_handler.Magazine()
volume = volume_handler.Volume()
issue = issue_handler.Issue()
page = page_handler.Page()
repro = reproduction_handler.Repro()
caption = caption_handler.Caption()

def process_first_row(row):
    #insert magazine
    magazine.magazine_name = row["journal name"]
    if (magazine.magazine_in_db() == -1):
        magazine.magazine_insert_new(row["language"])
        magazine.magazine_in_db()
    else:
        print(f"Magazine already in db")

    #insert volume
    #if row["volume"] == "NA":

    volume.volume_title = magazine.magazine_name + ", vol. " + row["volume"]
    result = row['year'].split(" ") #check for 2 elements
    volume_data = parse_date(result)

    volume_data["vol_number"] = row["volume"]
    volume_data["title"] = volume.volume_title
    volume_data["magazine_numeric_id"] = int(magazine.magazine_qid[1:])
    if volume.volume_in_db() == -1:
        volume.volume_insert_new(volume_data, row["language"])
        volume.volume_in_db()
    else:
        print(f"Volume is already in db")

    #insert issue
    issue_data = {}

    if row["issue"] == "NA":
        issue.issue_title = volume.volume_title + ', issue 1-12'
        issue_data["issue_number"] = '1-12'
    else:
        issue.issue_title = volume.volume_title + ', issue ' + row['issue']
        issue_data["issue_number"] = row["issue"]

    issue_data["issue_title"] = issue.issue_title
    issue_data["volume_numeric_id"] = int(volume.volume_qid[1:])
    issue_data["lang"] = row["language"]


    if issue.issue_in_db() == -1:
        issue.issue_insert_new(issue_data, issue_data["lang"])
    else:
        print(f"Issue already in db")


#journal name;issue;volume;year;page number;page index;image number;caption;area in percentage;x1;y1;x2;y2;image;width_page,height_page,language
def process_row(row, page_num_of_repro):
    print(magazine.magazine_qid, volume.volume_qid, issue.issue_qid)

    # preparation steps
    iss_vol_nimeric_id = issue.issue_in_db()
    while (iss_vol_nimeric_id == -1):
        iss_vol_nimeric_id = issue.issue_in_db()
    page_title = issue.issue_title + ", p. " + row["page number"]


    # page insert     data = page_title, page_number, page_index, num_of_repro, has_text, iss_vol_numeric_id, page_width, page_height
    p_text = 0 # zda u tech captions vsechno bude v poradku
    if (len(row["caption"]) > 0): p_text = 1

    if (row["page number"] in page_num_of_repro):
        page.page_title = page_title
        if page.page_in_db() == -1:
            page_data = {"page_title": page_title, "page_number" : row["page number"], "page_index" : row["page index"], 
                        "num_of_repro" : page_num_of_repro[row["page number"]], "has_text" : p_text, "iss_vol_numeric_id" : int(iss_vol_nimeric_id[1:]),
                        "height_page" : row["height_page"], "width_page" : row["width_page"]}

            page.page_insert_new(page_data, row["language"])
            page.page_in_db()
        del page_num_of_repro[row["page number"]]
    """
    # repro insert data = { repro_title, area, on_page, x1, y1, x2, y2, width, height }
    width = abs(int(row['x1']) - int(row['x2']))
    height = abs(int(row['y1']) - int(row['y2']))
    page_qid = page.page_in_db()
    while (page_qid == -1):
        page_qid = page.page_in_db()
    repro.repro_title = page_title + ", repro " + row["image number"]
    if repro.repro_in_db() == -1:

        repro_data = {"repro_title" :  repro.repro_title, "area" : row["area in percentage"], "on_page" : int(page_qid[1:]), "x1" : row["x1"], "y1" : row["y1"],
                     "x2" : row["x2"], "y2": row["y2"], "width" : width, "height" : height}
        repro.repro_insert_new(repro_data, row["language"])
        repro.repro_in_db()



    # caption insert #data = { caption_title, text, on_page, repro}
    if row["caption"] != "":
        repro_qid = repro.repro_in_db()
        while (repro_qid == -1):
            repro_qid = repro.repro_in_db()
        caption.caption_title = repro.repro_title + ", caption"
        if caption.caption_in_db() == -1:
            caption_data = {"caption_title" : caption.caption_title, "text" : row["caption"], "on_page" : int(page_qid[1:]), "repro" : int(repro_qid[1:])}
            caption.caption_insert_new(caption_data, row["language"])
    """

def parse_reproductions(row):
    # repro insert data = { repro_title, area, on_page, x1, y1, x2, y2, width, height }
    width = abs(int(row['x1']) - int(row['x2']))
    height = abs(int(row['y1']) - int(row['y2']))

    page.page_title = issue.issue_title + ", p. " + row["page number"]
    page_qid = page.page_in_db()
    while (page_qid == -1):
        page_qid = page.page_in_db()

    repro.repro_title = page.page_title + ", repro " + row["image number"]
    if repro.repro_in_db() == -1:

        repro_data = {"repro_title" :  repro.repro_title, "area" : row["area in percentage"], "on_page" : int(page_qid[1:]), "x1" : row["x1"], "y1" : row["y1"],
                     "x2" : row["x2"], "y2": row["y2"], "width" : width, "height" : height}
        repro.repro_insert_new(repro_data, row["language"])
        repro.repro_in_db()


def parse_captions(row):
    # caption insert #data = { caption_title, text, on_page, repro}
    if row["caption"] != "":

        page.page_title = issue.issue_title + ", p. " + row["page number"]
        page_qid = page.page_in_db()
        while (page_qid == -1):
            page_qid = page.page_in_db()

        repro.repro_title = page.page_title + ", repro " + row["image number"]
        repro_qid = repro.repro_in_db()
        while (repro_qid == -1):
            repro_qid = repro.repro_in_db()

        caption.caption_title = repro.repro_title + ", caption"
        if caption.caption_in_db() == -1:
            caption_data = {"caption_title" : caption.caption_title, "text" : row["caption"], "on_page" : int(page.page_qid[1:]), "repro" : int(repro_qid[1:])}
            caption.caption_insert_new(caption_data, row["language"])







