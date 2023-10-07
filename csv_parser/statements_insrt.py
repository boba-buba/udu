import csv

db = 'prm_d'

def is_float(value):
  if value is None:
      return False
  try:
      float(value)
      return True
  except:
      return False


def insert_into_table(dict_values, db_name, table_name):
    #check if insert or update
    #insert:
    statement = f"INSERT INTO {db_name}.{table_name} ("
    values = f"values ("
    first_key = list(dict_values)[0]
    for key in dict_values:
        if key != first_key:
            statement += ", "
            values += ", "
        statement += f"{key}"
        if (is_float(dict_values[key])):
            values += f"{dict_values[key]}"
        else:
            values += f"'{dict_values[key]}'"
    statement += ") "
    values += ");"
    return statement+values




def insert_statement(row):
    magazine_id  = -1
    page_id =  -1
    issue_id = -1
    volume_id = -1

    with open('try.sql', 'a', encoding='utf-8') as f:
        statement_magazine = insert_into_table({'name' : row['journal name']}, db, "magazines")
        f.write(statement_magazine+'\n')
        statement_volume = insert_into_table(
            {'num' : row['volume'], 'magazine_id' : 1}, db, 'volumes' # now magazine_id must set manually
        )
        f.write(statement_volume+'\n')
        statement_issue = insert_into_table(
            {'num' : row['issue'], 'volume_id': 1}, db, 'issues' # now volume_id must set manually
        )
        f.write(statement_issue+'\n')


def insert_multi(row):
    with open('try.sql', 'a', encoding='utf-8') as f:
        # page insert
        p_text = 0
        if (len(row['caption']) > 0): p_text = 1
        statement_page = insert_into_table(
            {'num' : row['page number'], 'p_index' : row['page index'],
             'num_repro' : row['image number'], 'issue_id' : 1, 'p_text' : p_text}, # issue_id manually
             db, 'pages'
        )
        f.write(statement_page+'\n')

        # repro insert
        width = abs(int(row['x1']) - int(row['x2']))
        height = abs(int(row['y1']) - int(row['y2']))
        dimension = round(height/width, 3)

        statement_repro = insert_into_table(
            {'page_id': row['page index'], 'x1' : row['x1'], 'y1' : row['y1'], 'x2' : row['x2'], # for now page_index not page_id
             'y2' : row['y2'], 'width' : width, 'height' : height, 'dimension' : dimension,
             'area' : row['area in percentage'], 'origin_image' : row['image'] }, db, 'reproductions'
        )
        f.write(statement_repro+'\n')

        # caption insert
        if (p_text == 1):
            statement_caption = insert_into_table(
                {'page_id' : row['page index'] }, db, 'captions' # page_index not page_id
            )
            f.write(statement_caption+'\n')




