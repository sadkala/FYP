import mysql.connector
from mysql.connector import Error
import Server 

connection=mysql.connector.connect(host='localhost',user='root',db='test')
cursor=connection.cursor()
SQL_select_thing="SELECT * FROM demotable665 "
cursor.execute(SQL_select_thing)
myresult=cursor.fetchall()

for x in myresult:
    print(x)