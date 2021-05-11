import mysql.connector
from mysql.connector import Error

def insertVariblesIntoTable(PlateNumber):
    try:
        connection=mysql.connector.connect(host='localhost',user='root',db='test')
        cursor=connection.cursor()
        SQL_insert_thing="INSERT INTO demotable665(PlateNumber)VALUES (%(carno)s)"
        CarPlate={'carno':PlateNumber}
        print(CarPlate)
        cursor.execute(SQL_insert_thing,CarPlate)
        connection.commit()
        print("Thing inserted inside nicely")

    except mysql.connector.Error as error:
        print("Failed to insert ".format(error))

    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("Mysql connection is closed")

insertVariblesIntoTable("MCLRNF1")