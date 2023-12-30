import sys
sys.path.insert(0, r'C:\Users\ncoro\udu\WikibaseIntegrator_handler')
import magazine_handler
import volume_handler

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

def process_first_row(row, lang = 'en'):

    #insert magazine
    magazine_name = row['journal name']
    magazine.name = magazine_name
    if (magazine.magazine_in_db(magazine_name=magazine_name) == -1):
        label = 'label'
        if (lang != 'en'):
            label = 'label_' + lang
        data = {label : magazine_name }
        magazine.magazine_insert_new(data, lang)
    else:
        print(f"Magazine already in db")


    #insert volume
    result = row['year'].split(" ") #check for 2 elements
    volume_data = parse_date(result)
    volume_data["vol_number"] = row["volume"]
    volume_data["title"] = magazine_name + ", Vol. " + volume_data["vol_number"]
    volume_data["magazine"] = magazine_name
    volume_data["magazine_numeric_id"] = int(magazine.magazine_in_db(magazine_name)[1:])
    if volume.volume_in_db(volume_data["title"]) == -1:
        with open("debug.txt", 'w', encoding="utf-8") as f:
            f.write(json.dumps(volume_data))
            f.flush()
        #print(volume_data)
        volume.volume_insert_new(volume_data, lang)
    else:
        print(f"volume is already in db")


    """
    #insert issue
    statement_issue = insert_into_table(
        {'num' : row['issue'], 'volume_id': volume_id}, 'issues'
    )
    db.insert_db(statement_issue)
    issue_id =set_global('issue', [row['issue'], volume_id, magazine_id])

    return [magazine_id, volume_id, issue_id]
    """
    return []



