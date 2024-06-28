#import相關套件
import mysql.connector
import pandas.io.sql as sql
import pandas as pd

def connect():
    #連結到資料庫
    config = {
        'user':'113403',
        'password':'@All3403@',
        'host':'140.131.114.242',
        'database':'113-law'
    }
    cnx=mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx,cursor

def creatdata(t,cursor):
    #新增資料
    # text='AAA1234'
    data = {'license_plate': [t],
            'date_time': ['2024-05-15 10:10:00'],
            'location': ['Taipei'],
            'violation': [False]}
    df = pd.DataFrame(data)
    

    # SQL插入語句
    add_violation = ("INSERT INTO testapp_car "
                    "(license_plate, date_time, location, violation) "
                    "VALUES (%s, %s, %s, %s)")

    # 將DataFrame中的每一行數據插入數據庫中
    for index, row in df.iterrows():
        data_violation = (row['license_plate'], row['date_time'], row['location'], row['violation'])
        cursor.execute(add_violation, data_violation)

def com(c):
    # 提交
    c.commit()

