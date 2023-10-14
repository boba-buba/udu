import csv
from db_conn import db_connection


db = db_connection()

def is_float(value):
  if value is None:
      return False
  try:
      float(value)
      return True
  except:
      return False


def insert_into_table(dict_values, table_name):
    #check if insert or update
    #insert:
    statement = f"INSERT INTO {table_name} ("
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


def set_global(column, info):
    match column:
        case "magazine":
            db.execute_query(f'select id from magazines where name="{info[0]}";')
            magazine = db.temp_result
            if (len(magazine) > 0):
                return magazine[0][0]
        case "volume":
            db.execute_query(f"select id from volumes where num={info[0]} and magazine_id={info[1]};")
            volume = db.temp_result
            if (len(volume) > 0):
                print(volume)
                return volume[0][0]
        case "issue":
            db.execute_query(f"select i.id from issues i inner join volumes v on i.volume_id=v.id inner join magazines m on v.magazine_id=m.id where i.num={info[0]} and v.id={info[1]} and m.id={info[2]};")
            issue = db.temp_result
            if (len(issue) > 0):
                return issue[0][0]
        case "page":
            db.execute_query("SELECT id FROM pages WHERE id=(SELECT MAX(id) FROM pages);")
            page = db.temp_result
            if (len(page) > 0):
                return page[0][0]
        case _:
            return None


def insert_statement(row):

    with open('try.sql', 'a', encoding='utf-8') as f:
        #insert magazine
        statement_magazine = insert_into_table({'name' : row['journal name']}, "magazines")
        f.write(statement_magazine+'\n')
        db.insert_db(statement_magazine)
        magazine_id = set_global("magazine", [row['journal name']])

        #insert volume
        result = row['year'].split(" ") #check for 2 elements
        statement_volume = insert_into_table(
            {'num' : row['volume'], 'magazine_id' : magazine_id, 'timespan_start' : result[0], 'timespan_end' : result[1]}, 'volumes' # now magazine_id must set manually
        )
        f.write(statement_volume+'\n')
        db.insert_db(statement_volume)
        volume_id = set_global("volume", [row['volume'], magazine_id])


        #insert issue
        statement_issue = insert_into_table(
            {'num' : row['issue'], 'volume_id': volume_id}, 'issues'
        )
        f.write(statement_issue+'\n')
        db.insert_db(statement_issue)
        issue_id =set_global('issue', [row['issue'], volume_id, magazine_id])

    return [magazine_id, volume_id, issue_id]


def insert_multi(row, page_images, globals):

    with open('try.sql', 'a', encoding='utf-8') as f:
        # page insert
        #page_id = -1
        p_text = 0 # zda u tech captions vsechno bude v poradku
        if (page_images[row['page index']] == row['image number']):
            if (len(row['caption']) > 0): p_text = 1
            statement_page = insert_into_table(
                {'num' : row['page number'], 'p_index' : row['page index'],
                'num_repro' : page_images[row['page index']], 'issue_id' : globals[2], 'p_text' : p_text}, 'pages'
            )
            f.write(statement_page+'\n')
            #tady se zeptat na page id
            db.insert_db(statement_page)
        page_id = set_global('page', [])

        # repro insert
        width = abs(int(row['x1']) - int(row['x2']))
        height = abs(int(row['y1']) - int(row['y2']))

        statement_repro = insert_into_table(
            {'page_id': page_id, 'x1' : row['x1'], 'y1' : row['y1'], 'x2' : row['x2'], # for now page_index not page_id
             'y2' : row['y2'], 'width' : width, 'height' : height, 'dimension' : 'Pixels',
             'area' : row['area in percentage'], 'origin_image' : row['image'] }, 'reproductions'
        )
        f.write(statement_repro+'\n')

        # caption insert
        if (p_text == 1):
            statement_caption = insert_into_table(
                {'page_id' : page_id, 'text' : row['caption'] }, 'captions' # page_index not page_id
            )
            f.write(statement_caption+'\n')




