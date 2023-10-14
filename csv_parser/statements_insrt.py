import csv
from enum import Enum
from db_querying import execute_query
db = 'prm_d'



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


magazine_id  = -1
page_id =  -1
issue_id = -1
volume_id = -1

def set_global(column, info):
    match column:
        case "magazine":
            query = f'select id from magazines where name="{info}";'
            #print(query)
            magaizine = execute_query(query)
            if (len(magaizine) > 0):
                #print(magaizine[0][0])
                return magaizine[0][0]
        case "volume":
            volume = execute_query(f"select id from volumes where num={info} and magazine_id={magazine_id}")
            if (len(volume) > 0):
                volume_id = volume[0]
        case "issue":
            issue = execute_query(f"select i.id from issues i inner join volumes v on i.volume_id=v.id inner join magazines m on v.magazine_id=m.id where i.num={info} and v.id={volume_id} and m.id={magazine_id};")
            if (len(issue) > 0):
                issue_id = issue[0]
        case _:
            return





def insert_statement(row):

    with open('try.sql', 'a', encoding='utf-8') as f:
        #insert magazine
        statement_magazine = insert_into_table({'name' : row['journal name']}, "magazines")
        f.write(statement_magazine+'\n')
        magazine_id = set_global("magazine", row['journal name'])

        #insert volume
        result = row['year'].split(" ") #check for 2 elements
        statement_volume = insert_into_table(
            {'num' : row['volume'], 'magazine_id' : magazine_id, 'timespan_start' : result[0], 'timespan_end' : result[1]}, 'volumes' # now magazine_id must set manually
        )
        f.write(statement_volume+'\n')
        set_global("volume", row['volume'])

        #insert issue
        statement_issue = insert_into_table(
            {'num' : row['issue'], 'volume_id': volume_id}, 'issues' # now volume_id must set manually
        )
        f.write(statement_issue+'\n')
        set_global("issue", row['issue'])


def insert_multi(row):

    with open('try.sql', 'a', encoding='utf-8') as f:
        # page insert
        p_text = 0
        if (len(row['caption']) > 0): p_text = 1
        statement_page = insert_into_table(
            {'num' : row['page number'], 'p_index' : row['page index'],
             'num_repro' : row['image number'], 'issue_id' : issue_id, 'p_text' : p_text}, # issue_id manually, jeste to num_repro
             'pages'
        )
        f.write(statement_page+'\n')

        # repro insert
        width = abs(int(row['x1']) - int(row['x2']))
        height = abs(int(row['y1']) - int(row['y2']))

        statement_repro = insert_into_table(
            {'page_id': row['page index'], 'x1' : row['x1'], 'y1' : row['y1'], 'x2' : row['x2'], # for now page_index not page_id
             'y2' : row['y2'], 'width' : width, 'height' : height, 'dimension' : 'Pixels',
             'area' : row['area in percentage'], 'origin_image' : row['image'] }, 'reproductions'
        )
        f.write(statement_repro+'\n')

        # caption insert
        if (p_text == 1):
            statement_caption = insert_into_table(
                {'page_id' : row['page index'] }, 'captions' # page_index not page_id
            )
            f.write(statement_caption+'\n')




