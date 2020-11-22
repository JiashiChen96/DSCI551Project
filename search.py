import mysql.connector
import pymongo

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

def query():
    connection, cursor = getConnection(HOST, USER, PASSWORD, DB)
    cursor.execute("SELECT * FROM vehicles")

    myresult = cursor.fetchall()
    # print(type(myresult))
    # for x in myresult:
    #     print(x)
    closeConnection(connection, cursor)
    return myresult

def connectMongoDb():
    myclient = pymongo.MongoClient(
        "mongodb+srv://Jason:admin123@cluster0.3ne24.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = myclient.DSCI551Project
    myCollect = mydb.TrueCar

    myresult = []
    for x in myCollect.find():
        myresult.append(x)
    return myresult

if __name__ == '__main__':
    print(connectMongoDb())