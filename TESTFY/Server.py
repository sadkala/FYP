import socketserver
import datetime
import base64
import numpy as np
import cv2
import imutils
import mysql.connector
from mysql.connector import Error
import Main
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

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("get....")
        image1 = []
        try:
            while True:
                data=self.request.recv(5120) #拿到客戶端發送的數據 
                #print('data,',data)#照片=data
                # data = base64.b64decode(data)
                if not data or len(data) == 0:
                    break
                image1.extend(data)
                            
            
            image = np.asarray(bytearray(image1), dtype="uint8")#映像陣列
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            Image = imutils.resize(image,width=400,height=400)
            #Main.main(Image)###############throw my image inside py
            plateNumber=Main.main(Image)
            print("Platenumber send="+plateNumber)
            ######################
            insertVariblesIntoTable(plateNumber)#insert into mysql
            ######################
            self.request.sendall(plateNumber)##send car plate to client edit text##cant send
            print("I send it")
            ################################################
        except Exception:
            print(self.client_address,"連接斷開")
        finally:
            self.request.close()    #異常之後，關閉連接

    #before handle,連接建立：
    def setup(self):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now_time)
        print("連接建立：",self.client_address)

    # finish run  after handle
    def finish(self):
        print("釋放連接")


if __name__=="__main__":
    HOST,PORT = "",8004
    # server=socketserver.TCPServer((HOST,PORT),MyTCPHandler)  #實例對象，傳入參數

    # 多線程
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()   #一直運行


