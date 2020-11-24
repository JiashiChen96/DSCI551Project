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


def sql_clause(request):
    cleaned_request = {}
    for k, v in request.items():
        if v != "":
            if type(v) is int:
                cleaned_request[k.lower()] = v
            else:
                cleaned_request[k.lower()] = v.lower()

    where_clause = ""
    for k, v in cleaned_request.items():
        if k == "city":
            where_clause = where_clause + "city = " + f"'{v}' AND "

        elif k == "state":
            where_clause = where_clause + "state = " + f"'{v}' AND "

        elif k == "manufacturer":
            where_clause = where_clause + "manufacturer " + f"LIKE '%{v}%' AND "

        elif k == "model":
            where_clause = where_clause + "model " + f"LIKE '%{v}%' AND "

        elif k == "cylinders":
            where_clause = where_clause + "cylinders " + f"LIKE '%{v}%' AND "

        elif k == "fuel":
            where_clause = where_clause + "fuel = " + f"'{v}' AND "

        elif k == "transmission":
            where_clause = where_clause + "transmission " + f"LIKE '%{v}%' AND "

        elif k == "min_price":
            where_clause = where_clause + "price >= " + f"{v} AND "

        elif k == "max_price":
            where_clause = where_clause + "price <= " + f"{v} AND "

        elif k == "min_year":
            where_clause = where_clause + "years >= " + f"{v} AND "

        elif k == "max_year":
            where_clause = where_clause + "years <= " + f"{v} AND "
        elif k == "minimum mileage":
            where_clause = where_clause + "odometer >= " + f"{v} AND "

        elif k == "max_mileage":
            where_clause = where_clause + "odometer <= " + f"{v} AND "

        elif k == "sort_by":
            if v == "mileage":
                where_clause = where_clause[:-5]
                where_clause = where_clause + " order by odometer asc"
            elif v == "year": #year is reserved word in sql
                where_clause = where_clause[:-5]
                where_clause = where_clause + " order by years asc"
            else:
                where_clause = where_clause[:-5]
                print(where_clause)
                where_clause = where_clause + " order by price asc"

    return where_clause


def query(request):
    connection, cursor = getConnection(HOST, USER, PASSWORD, DB)
    clause = sql_clause(request)
    if clause == "":
        pass
    elif "order by" in clause and len(clause) <= 22:
        q = "select * from vehicles" + clause
        cursor.execute(q)
    else:
        q = "select * from vehicles where " + clause
        cursor.execute(q)

    myresult = cursor.fetchall()

    closeConnection(connection, cursor)
    return myresult
def mongo_query(request):
    cleaned_request = {}
    for k, v in request.items():
        if v != "":
            if type(v) is int:
                cleaned_request[k] = v
            else:
                cleaned_request[k.lower()] = v.title()
            #如果将data里面的值转换成小写后，下面将替换上面
            # if type(v) is int:
            #     cleaned_request[k.lower()] = v
            # else:
            #     cleaned_request[k.lower()] = v.lower()

    myquery = {}
    for k, v in cleaned_request.items():
        if k == "city":
            myquery[k] = v

        elif k == "state":
            myquery[k] = v

        elif k == "manufacturer":
            myquery[k] = {"$regex": v}

        elif k == "model":
            myquery[k] = {"$regex": v}

        elif k == "cylinders":
            myquery[k] = {"$regex": v}

        elif k == "fuel":
            myquery[k] = v

        elif k == "transmission":
            myquery[k] = {"$regex": v}

        elif k == "min_price":
            myquery["min_price"] = {"$gte": v}

        elif k == "max_price":
            myquery["max_price"] = {"$lte": v}

        elif k == "min_year":
            myquery["min_year"] = {"$gte": v}

        elif k == "max_year":
            myquery["max_year"] = {"$lte": v}

        elif k == "min_mileage":
            myquery["min_mileage"] = {"$gte": v}

        elif k == "max_mileage":
            myquery["max_mileage"] = {"$lte": v}

        elif k == "sort_by":
            myquery["$orderby"] = {v: 1}

    if "min_price" in myquery.keys():
        if "max_price" in myquery.keys():
            min_price = myquery["min_price"]["$gte"]
            max_price = myquery["max_price"]["$lte"]
            myquery["price"] = {"$gte": min_price, "$lte": max_price}
            del myquery["min_price"]
            del myquery["max_price"]
        else:
            min_price = myquery["min_price"]["$gte"]
            myquery["price"] = {"$gte": min_price}
            del myquery["min_price"]

    if "max_price" in myquery.keys():
        if "min_price" in myquery.keys():
            min_price = myquery["min_price"]["$gte"]
            max_price = myquery["max_price"]["$lte"]
            myquery["price"] = {"$gte": min_price, "$lte": max_price}
            del myquery["min_price"]
            del myquery["max_price"]
        else:
            max_price = myquery["min_price"]["$lte"]
            myquery["price"] = {"$gte": max_price}
            del myquery["max_price"]

    if "min_year" in myquery.keys():
        if "max_year" in myquery.keys():
            min_year = myquery["min_year"]["$gte"]
            max_year = myquery["max_year"]["$lte"]
            myquery["year"] = {"$gte": min_year, "$lte": max_year}
            del myquery["min_year"]
            del myquery["max_year"]
        else:
            min_year = myquery["min_year"]["$gte"]
            myquery["year"] = {"$gte": min_year}
            del myquery["min_year"]

    if "max_year" in myquery.keys():
        if "min_year" in myquery.keys():
            min_year = myquery["min_year"]["$gte"]
            max_year = myquery["max_year"]["$lte"]
            myquery["year"] = {"$gte": min_year, "$lte": max_year}
            del myquery["min_year"]
            del myquery["max_year"]
        else:
            max_year = myquery["max_year"]["$lte"]
            myquery["year"] = {"$lte": max_year}
            del myquery["max_year"]

    if "min_mileage" in myquery.keys():
        if "max_mileage" in myquery.keys():
            min_mileage = myquery["min_mileage"]["$gte"]
            max_mileage = myquery["max_mileage"]["$lte"]
            myquery["mileage"] = {"$gte": min_mileage, "$lte": max_mileage}
            del myquery["min_mileage"]
            del myquery["max_mileage"]
        else:
            min_mileage = myquery["min_mileage"]["$gte"]
            myquery["mileage"] = {"$gte": min_mileage}
            del myquery["min_mileage"]

    if "max_mileage" in myquery.keys():
        if "min_mileage" in myquery.keys():
            min_mileage = myquery["min_mileage"]["$gte"]
            max_mileage = myquery["max_mileage"]["$lte"]
            myquery["mileage"] = {"$gte": min_mileage, "$lte": max_mileage}
            del myquery["min_mileage"]
            del myquery["max_mileage"]
        else:
            max_mileage = myquery["max_mileage"]["$lte"]
            myquery["mileage"] = {"$lte": max_mileage}
            del myquery["max_mileage"]

    return myquery


def connectMongoDb(request):
    request = mongo_query(request)

    k, v = list(request["$orderby"].items())[0]
    k = k.lower()

    del request["$orderby"]

    myclient = pymongo.MongoClient(
        "mongodb+srv://Jason:admin123@cluster0.3ne24.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = myclient.DSCI551Project
    myCollect = mydb.TrueCar

    d = []
    if request != {}:
        for x in myCollect.find(request):
            d.append(x)
        result = sorted(d, key = lambda i: i[k])
        return result
    else:
        for x in myCollect.find():
            d.append(x)
        result = sorted(d, key=lambda i: i[k])
        return result

if __name__ == '__main__':
    # data = {'city': '', 'state': '', 'manufacturer': 'Toyota', 'model': '', 'cylinders': '', 'fuel': '', 'transmission': '', 'min_price': '', 'max_price': '', 'min_year': '', 'max_mileage': '', 'sort_by': 'mileage'}
    # print(connectMongoDb(data))
    # data = {'manufacturer': 'Toyota', 'inputOrder': 'Milage'}
    # print(query(data))
    data = {'inputLocation': '', 'manufacturer': 'Toyota', 'model': '', 'cylinders': '', 'fuel': '', 'transmission': '',
            'inputOrder': '', 'min_price': '', 'max_price': '', 'min_year': '', 'max_year': '',
            'sort_by': 'mileage'}
    filter = {'inputLocation': '', 'manufacturer': 'Toyota', 'model': '', 'cylinders': '',
              'fuel': '', 'transmission': '', 'min_price': '', 'max_price': '', 'min_year': '', 'max_mileage': '',
              'sort_by': 'mileage'}
    print(sql_clause(data))
    print(sql_clause(filter))
    query(filter)
    query(data)