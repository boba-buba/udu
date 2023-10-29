import csv
from db_conn import db_connection
from statements_insrt import is_float

db = db_connection()
def get_ids(file_name, id_name):
    ids = []
    with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',')

        for row in reader:
            ids.append(int(row[id_name]))
        f.flush()
    return ids


def parse_csv(file_name, ids, id_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',')

        table_name = "captions"
        i = 0
        print(ids)
        for row in reader:
            print(ids[i])
            stm = insert_into_table_with_condition(dict(row), table_name, id_name, ids[i])
            db.insert_db(stm)
            #print(stm)
            i += 1
        f.flush()

def insert_into_table_with_condition(dict_values, table_name, id_name, id):
    #insert:
    statement = f"UPDATE {table_name} SET "
    #values = f"values ("
    last_key = list(dict_values)[-1]
    for key in dict_values:
        statement += f"{key} = "
        if (is_float(dict_values[key])):
            statement += f"{dict_values[key]}"
        else:
            statement += f"'{dict_values[key]}'"
        if (key != last_key): statement += ", "
    statement += f" WHERE {id_name}={id};"
    return statement


#parse_csv(r"C:\Users\ncoro\udu\dump.csv", get_ids(r"C:\Users\ncoro\udu\repros.csv", "id"), "id")
