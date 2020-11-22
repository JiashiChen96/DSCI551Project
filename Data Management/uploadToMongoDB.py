import os
import re

import pymongo
import pandas as pd

def uploadToMongoDB():
    myclient = pymongo.MongoClient(
        "mongodb+srv://Jason:admin123@cluster0.3ne24.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = myclient.DSCI551Project
    myCollect = mydb.TrueCar

    regex = re.compile(r'part*')
    base_path = '../Data/TrueCar/SparkOutput/'
    data_files = [m for m in os.listdir(base_path) if regex.match(m)]

    cars = pd.read_csv(base_path + data_files[0], index_col=0).to_dict(orient='records')

    myCollect.delete_many({})
    myCollect.insert_many(cars)


if __name__ == '__main__':
    uploadToMongoDB()