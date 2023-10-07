import mysql.connector as mysql
from mysql.connector import errorcode

import csv, os


def db_check(line, db_name, table_name):
    outFolder = r"C:\Users\ncoro\udu\csv_parser"
    cn = mysql.connect(user = 'root', password = '5pigswererelaxingonthebeach', host = 'web10', database = 'prm_d')
    cursor = cn.cursor()
    #table = 'cities'
    query = f'SELECT * from {db_name}.{table_name};'

    cursor.execute(query)

    rows = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    dotcsv = f'{table_name}.csv'

    outFile = open(os.path.join(outFolder,dotcsv),'w',newline ='')
    myFile = csv.writer(outFile)
    myFile.writerow(column_names)
    myFile.writerows(rows)
    cursor.close
    #statement = f"INSERT INTO {db_name}.{table_name} () VALUES "

try:
    connection = mysql.connect(host='147.231.55.155',
                            database='prm_d',
                            user='korop',
                            password='5pigsonthe_rooF')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except mysql.Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


#def main():
    '''tableList = []
    cn = mysql.connect(user = 'root', password = '5pigswererelaxingonthebeach', host = 'web10', database = 'prm_d')
    cursor = cn.cursor()
    allTables = "show tables"
    cursor.execute(allTables)
    for (allTables) in cursor:
        tableList.append(allTables[0])
    cursor.close
    print(tableList)'''