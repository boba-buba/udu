from db_config import config
from db_conn import connect_to_mysql


def execute_query(query):
    cnx = connect_to_mysql(config, attempts=3)

    if cnx and cnx.is_connected():

        with cnx.cursor() as cursor:
            result = cursor.execute(query)
            rows = cursor.fetchall()
           # for row in rows:
            #    print(row)
            return rows
        #cnx.close()

    else:

        print("Could not connect")


'''
result = execute_query("show tables;")
print(result)
result = execute_query("select * from nations;")
print(len(result) == 0)'''