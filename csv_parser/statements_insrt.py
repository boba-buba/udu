import csv
from db_conn import db_connection


db = db_connection()

def parse_caption(text):
    new_text = text.replace("'", "\\" + "'")
    #new_text = new_text.replace("(", "\\" + "()")
    return new_text


def is_in_db(query):
    db.execute_query(query)
    result = db.temp_result
    if (len(result) != 0):
        return result[0][0]
    return 0

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
            db.execute_query(f'select id_magazine from magazines where name="{info[0]}";')
            magazine = db.temp_result
            if (len(magazine) > 0):
                return magazine[0][0]
        case "volume":
            db.execute_query(f"select id_volume from volumes where num={info[0]} and magazine_id={info[1]};")
            volume = db.temp_result
            if (len(volume) > 0):
                return volume[0][0]
        case "issue":
            db.execute_query(f"select i.id_issue from issues i inner join volumes v on i.volume_id=v.id_volume inner join magazines m on v.magazine_id=m.id_magazine where i.num={info[0]} and v.id_volume={info[1]} and m.id_magazine={info[2]};")
            issue = db.temp_result
            if (len(issue) > 0):
                return issue[0][0]
        case "page":
            db.execute_query("SELECT id_page FROM pages WHERE id_page=(SELECT MAX(id_page) FROM pages);")
            page = db.temp_result
            if (len(page) > 0):
                return page[0][0]
        case _:
            return None


def insert_statement(row):

    #insert magazine
    magazine_name = row['journal name']
    magazine_query = f'select id_magazine from magazines where name="{magazine_name}";'
    if (is_in_db(magazine_query) == 0):
        statement_magazine = insert_into_table({'name' : row['journal name']}, "magazines")
        db.insert_db(statement_magazine)

    magazine_id = set_global("magazine", [row['journal name']])

    #insert volume
    result = row['year'].split(" ") #check for 2 elements
    time_start = result[0].split("-") #yyyy mm dd
    time_end = result[1].split("-")

    statement_volume = insert_into_table(
        {'num' : row['volume'], 'magazine_id' : magazine_id, 'year_start' : time_start[0], 'month_start' : time_start[1],
            'day_start' : time_start[2], 'year_end' : time_end[0], 'month_end' : time_end[1], 'day_end' :time_end[2] }, 'volumes'
    )
    db.insert_db(statement_volume)
    volume_id = set_global("volume", [row['volume'], magazine_id])


    #insert issue
    statement_issue = insert_into_table(
        {'num' : row['issue'], 'volume_id': volume_id}, 'issues'
    )
    db.insert_db(statement_issue)
    issue_id =set_global('issue', [row['issue'], volume_id, magazine_id])

    return [magazine_id, volume_id, issue_id]


def insert_multi(row, page_images, globals):

    # page insert
    p_text = 0 # zda u tech captions vsechno bude v poradku
    if (len(row['caption']) > 0): p_text = 1

    if (row['page index'] in page_images):
        statement_page = insert_into_table(
            {'num' : row['page number'], 'p_index' : row['page index'],
            'num_repro' : page_images[row['page index']], 'issue_id' : globals[2], 'p_text' : p_text}, 'pages'
        )
        #tady se zeptat na page id
        db.insert_db(statement_page)
        del page_images[row['page index']]
    page_id = set_global('page', [])

    # repro insert
    width = abs(int(row['x1']) - int(row['x2']))
    height = abs(int(row['y1']) - int(row['y2']))

    statement_repro = insert_into_table(
        {'page_id': page_id, 'x1' : row['x1'], 'y1' : row['y1'], 'x2' : row['x2'], # for now page_index not page_id
            'y2' : row['y2'], 'width' : width, 'height' : height, 'dimension' : 'Pixels',
            'area' : row['area in percentage'], 'original_image' : row['image'] }, 'reproductions'
    )

    db.insert_db(statement_repro)

    # caption insert
    if (p_text == 1):
        caption = parse_caption(row['caption'])
        statement_caption = insert_into_table(
            {'page_id' : page_id, 'text' : caption }, 'captions' # page_index not page_id
        )
        db.insert_db(statement_caption)


