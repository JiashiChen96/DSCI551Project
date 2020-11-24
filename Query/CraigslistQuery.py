import mysql.connector

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

def sql_clause(request):
    cleaned_request = {}
    for k, v in request.items():
        if v != "":
            if type(v) is int:
                cleaned_request[k.lower()] = v
            else:
                cleaned_request[k.lower()] = v.lower()

    where_clause = ""
    att = ""

    for k, v in cleaned_request.items():
        print(k, "and", v)
        if k == "inputlocation":
            if v == "new york city, ny":
                where_clause = where_clause + " state = 'ny' AND "

            if v == "los angeles, ca":
                where_clause = where_clause + " state = 'ca' AND "

        elif k == "manufacturer":
            where_clause = where_clause + " manufacturer " + f"LIKE '%{v}%' AND "

        elif k == "model":
            where_clause = where_clause + " model " + f"LIKE '%{v}%' AND "

        elif k == "drive_type":
            where_clause = where_clause + " drive_type " + f"LIKE '%{v}%' AND "

        elif k == "fuel":
            where_clause = where_clause + " fuel = " + f"'{v}' AND "

        elif k == "transmission":
            where_clause = where_clause + " transmission " + f"LIKE '%{v}%' AND "

        elif k == "min_price":
            where_clause = where_clause + " price >= " + f"{v} AND "

        elif k == "max_price":
            where_clause = where_clause + " price <= " + f"{v} AND "

        elif k == "min_year":
            where_clause = where_clause + " year >= " + f"{v} AND "

        elif k == "max_year":
            where_clause = where_clause + " year <= " + f"{v} AND "
        elif k == "minimum mileage":
            where_clause = where_clause + " mileage >= " + f"{v} AND "

        elif k == "max_mileage":
            where_clause = where_clause + " mileage <= " + f"{v} AND "

        if k == "sort_by":
            att = v

    where_clause = where_clause[:-5]
    if att != "":
        where_clause = where_clause + " order by " + att +  " asc"

    return where_clause


def query_craigslist(request):
    connection, cursor = getConnection(HOST, USER, PASSWORD, DB)
    clause = sql_clause(request).strip()

    if clause == "":
        q = "select * from vehicles"
        cursor.execute(q)
    elif clause.startswith("order"):
        q = "select * from vehicles" + clause
        cursor.execute(q)
    else:
        q = "select * from vehicles where " + clause
        print(q)
        cursor.execute(q)

    myresult = cursor.fetchall()

    closeConnection(connection, cursor)
    return myresult

if __name__ == '__main__':
    filter = {'inputLocation': '', 'manufacturer': '', 'model': '', 'drive_type': '4wd', 'fuel': '', 'transmission': '', 'sort_by': '', 'min_price': '', 'max_price': '', 'min_year': '', 'max_year': ''}
    # print(sql_clause(filter))
    print(query_craigslist(filter))