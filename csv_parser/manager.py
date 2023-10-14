#import db_conn
import os
import sys
from parser_csv import parse_csv
from dump_query import dump_query



def work_with_csv(input_path, output_path):
    parse_csv(input_path)


def work_with_folder():
    #jak najit vsechn csv
    print("folder")

def work_with_quering(query, file_name):
    dump_query(query, file_name)