import csv
from db_conn import db_connection

db = db_connection()

def dump_query(query, csv_file):
    db.execute_query(query)
    rows = db.temp_result
    description = db.temp_description

    if rows:
        # New empty list called 'result'. This will be written to a file.
        result = list()

        # The row name is the first entry for each entity in the description tuple.
        column_names = list()
        for i in description:
            column_names.append(i[0])

        result.append(column_names)
        for row in rows:
            result.append(row)

        # Write result to file.
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)


#dump_query("select * from pages;", f".\\dump.csv")