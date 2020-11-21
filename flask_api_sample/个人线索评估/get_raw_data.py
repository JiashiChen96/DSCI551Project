import pandas
import pymysql

def __DB_access_helper(_id):
    connect_luoma_kc = pymysql.connect(
        host='bj-cdb-fu5gl04c.sql.tencentcdb.com',
        port=63665,
        user='OperGuest', password='GuestLuoma!@#12',
        database='luoma_kc',
        charset='utf8', use_unicode=True)

    sql = "select * from kc_clues where id ="+"'"+str(_id)+"'"
    data = pandas.read_sql(sql, con=connect_luoma_kc)
    connect_luoma_kc.close()
    return data

def __DB_access(_id_list):
    data=__DB_access_helper(_id_list[0])
    for id in _id_list[1:]:
        data=data.append(__DB_access_helper(id))
    return data
