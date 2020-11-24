import os
import re

import mysql.connector
import pandas as pd

HOST = 'us-cdbr-east-02.cleardb.com'
USER = 'ba989908699a00'
PASSWORD = 'e0812ffe'
DB = 'heroku_32dc5f0ec6f7b30'

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
    print(cars)
    cursor.execute("TRUNCATE TABLE vehicles")

    for index, row in cars.iterrows():
        temp = (row.state, row.city, row.year, row.manufacturer, row.model, row.price, row.mileage, row.cylinders, row.drive, row.transmission, row.fuel, row.url, row.image_url)
        print(temp)
        cursor.execute("INSERT INTO vehicles (state, city, year, manufacturer, model, price, mileage, cylinders, drive_type, transmission, fuel, url, image_url) "
                       "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       temp)
    connection.commit()
if __name__ == '__main__':
    connection, cursor = getConnection(HOST, USER, PASSWORD, DB)
    upload(connection, cursor)
    closeConnection(connection, cursor)