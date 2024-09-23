#import db_conn
import os
#import sys
from entry import parse_data

def is_csv(file_name):
    if file_name.endswith('.csv'):
        return True
    else:
        return False


def work_with_csv(input_path, output_path = ""):
    #TODO create path for data/pages
    #parse_data(input_path_pages, input_path_repros)
    print()


def work_with_folder(dir_name):
    names = []
    entries = os.listdir(dir_name)
    for i, entry in enumerate(entries):
        print(entry)
        if is_csv(entry):
            names.append(dir_name+"/"+entry)

    for csv_file in names:
        work_with_csv(csv_file)

# def work_with_quering(query, file_name):
#     dump_query(query, file_name)