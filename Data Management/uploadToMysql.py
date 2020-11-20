import os
import re

import mysql.connector
import pandas as pd

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DB = 'DSCI551Project'

def getConnection(host, user, pwd, db):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        passwd=pwd,
        database=db
    )
    return connection, connection.cursor()

def closeConnection(connection, cursor):
    cursor.close()
    connection.close()

def upload(connection, cursor):
    regex = re.compile(r'part*')
    base_path = '../Data/Craigslist/SparkOutput/'
    data_files = [m for m in os.listdir(base_path) if regex.match(m)]
    # print(data_files)
    cars = pd.read_csv(base_path + data_files[0])
    # print(cars)
    for index, row in cars.iterrows():
        temp = (row.region, row.year, row.manufacturer, row.model, row.price, row.mileage, row.transmission)
        # print(temp)
        cursor.execute("INSERT INTO Craigslist (region, year, manufacturer, model, price, mileage, transmission) values(%s,%s,%s,%s,%s,%s,%s)",
                       temp)
    connection.commit()
if __name__ == '__main__':
    connection, cursor = getConnection(HOST, USER, PASSWORD, DB)
    upload(connection, cursor)
    closeConnection(connection, cursor)