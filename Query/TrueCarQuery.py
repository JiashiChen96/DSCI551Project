import pymongo

def mongodb_clause(request):
    cleaned_request = {}
    for k, v in request.items():
        if v != "":
            if type(v) is int:
                cleaned_request[k] = v
            else:
                cleaned_request[k.lower()] = v.title()

    myquery = {}
    myquery["$orderby"] = ""
    for k, v in cleaned_request.items():
        print(k, "and", v)
        if k == "inputlocation":
            if v == "New York City, Ny":
                myquery["state"] = "NY"
            if v == "Los Angeles, Ca":
                myquery["state"] = "CA"

        elif k == "manufacturer":
            myquery[k] = {"$regex": v}

        elif k == "model":
            myquery[k] = {"$regex": v}

        elif k == "drive_type":
            myquery[k] = v.upper()

        elif k == "fuel":
            myquery[k] = v

        elif k == "transmission":
            myquery[k] = {"$regex": v}

        elif k == "min_price":
            myquery["min_price"] = {"$gte": int(v)}

        elif k == "max_price":
            myquery["max_price"] = {"$lte": int(v)}

        elif k == "min_year":
            myquery["min_year"] = {"$gte": int(v)}

        elif k == "max_year":
            myquery["max_year"] = {"$lte": int(v)}

        elif k == "min_mileage":
            myquery["min_mileage"] = {"$gte": int(v)}

        elif k == "max_mileage":
            myquery["max_mileage"] = {"$lte": int(v)}

        elif k == "sort_by":
            myquery["$orderby"] = v.lower()

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


def query_TrueCar(request):
    myclient = pymongo.MongoClient(
        "mongodb+srv://Jason:admin123@cluster0.3ne24.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = myclient.DSCI551Project
    myCollect = mydb.TrueCar

    request = mongodb_clause(request)
    print(request)
    result = []
    orderby = request["$orderby"]
    del request["$orderby"]
    if orderby == "":
        for instance in myCollect.find(request):
            result.append(instance)
    else:
        for instance in myCollect.find(request).sort(orderby):
            result.append(instance)
    return result
    #     print("twe")
    # k, v = list(request["$orderby"].items())[0]
    # k = k.lower()
    #
    # del request["$orderby"]
    # result = []
    # for instance in myCollect.find(request).sort(k):
    #     result.append(instance)
    # return result

if __name__ == '__main__':
    filter = {'inputLocation': '', 'manufacturer': '', 'model': '', 'drive_type': '4wd', 'fuel': '', 'transmission': '', 'sort_by': '', 'min_price': '', 'max_price': '', 'min_year': '', 'max_year': ''}
    # print(mongodb_clause(filter))
    print(query_TrueCar(filter))