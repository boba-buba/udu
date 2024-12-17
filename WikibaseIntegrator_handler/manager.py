#import db_conn
import os
#import sys
from entry import parse_data

def is_csv(file_name):
    if file_name.endswith('.csv'):
        return True
    else:
        return False


def work_with_csv(input_path: str, output_path: str = ""):
    #TODO create path for data/pages
    #parse_data(input_path_pages, input_path_repros)
    if "pages" in input_path:
        data_csv = input_path.replace("pages", "data")
        if os.path.isfile(data_csv) == True:
            print("Parsing files: " + input_path + " and " + data_csv)
            parse_data(input_path, data_csv)
        else:
            print("No ..._data.csv file for file ", input_path, ".")


def work_with_folder(dir_name):
    names = []
    entries = os.listdir(dir_name)
    for i, entry in enumerate(entries):
        #print(entry)
        if is_csv(entry):
            names.append(dir_name+"/"+entry)

    for csv_file in names:
        work_with_csv(csv_file)

# def work_with_quering(query, file_name):
#     dump_query(query, file_name)