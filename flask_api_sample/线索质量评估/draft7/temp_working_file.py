import pandas
import pymysql
from get_ages import __get_ages
from get_price_difference import __get_price_difference
from help_functions import __get_tags
from get_ages import __get_year_and_month
from numpy import nan
import datetime
import time

def __get_ages_level(data):  #计算并添加车龄，返回pandas.dataframe格式
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    _column.append('car_ages_level')  # 添加 "车龄" 列
    data = data.values
    _list = []

    for item in data:       #逐行添加车龄级别
        _temp=list(item)
        #_license_date = _temp[_column_tags['license_date']]
        _age=_temp[_column_tags['car_ages']]
        if float(_age)<=4:
            _temp.append('A')
        elif float(_age)<=6 and float(_age)>4:
            _temp.append('B')
        elif float(_age)<=10 and float(_age)>6:
            _temp.append('C')
        else:
            _temp.append('D')

        _list.append(_temp)

    _data=pandas.DataFrame(_list,columns=_column)
    return _data

def __get_price_level(data):
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    _column.append('car_price_level')  # 添加 "车龄" 列
    data = data.values
    _list = []

    for item in data:  # 逐行添加车龄级别
        _temp = list(item)
        # _license_date = _temp[_column_tags['license_date']]
        _price = _temp[_column_tags['valuation']]
        if float(_price) >= 15:
            _temp.append('A')
        elif float(_price) < 15 and float(_price) >= 5:
            _temp.append('B')
        elif float(_price) < 5 and float(_price) > 1:
            _temp.append('C')
        else:
            _temp.append('D')

        _list.append(_temp)

    _data = pandas.DataFrame(_list, columns=_column)
    return _data

def __get_miles_level(data):
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    _column.append('car_miles_level')  # 添加 "车龄" 列
    data = data.values
    _list = []

    for item in data:  # 逐行添加车龄级别
        _temp = list(item)
        # _license_date = _temp[_column_tags['license_date']]
        _miles = _temp[_column_tags['miles']]
        try:
            _miles=float(_miles)
        except:
            print('*****'+str(_miles))
            continue
        if float(_miles)>=1000:
            miles=float(miles)/10000

        if float(_miles) <= 4:
            _temp.append('A')
        elif float(_miles) <= 6 and float(_miles) > 4:
            _temp.append('B')
        elif float(_miles) <= 10 and float(_miles) > 6:
            _temp.append('C')
        else:
            _temp.append('D')

        _list.append(_temp)


    _data = pandas.DataFrame(_list, columns=_column)
    return _data

def __get_status_level(data):
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    _column.append('car_status_level')  # 添加 "车龄" 列
    data = data.values
    _list = []

    for item in data:  # 逐行添加车龄级别
        _temp = list(item)
        # _license_date = _temp[_column_tags['license_date']]
        _status = _temp[_column_tags['vehicles']]


        if float(_status) == 10:
            _temp.append('B')
        elif  pandas.isna(_status):
            _temp.append('不确定')
        else:
            _temp.append('A')

        _list.append(_temp)


    _data = pandas.DataFrame(_list, columns=_column)
    return _data



def __get_price_differ_level(data):
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    _column.append('car_price_differ_level')  # 添加 "车龄" 列
    data = data.values
    _list = []

    for item in data:  # 逐行添加车龄级别
        _temp = list(item)
        # _license_date = _temp[_column_tags['license_date']]
        price_differ = _temp[_column_tags['price_differ']]
        if float(price_differ) <= 0:
            _temp.append('A')
        elif float(price_differ) <= 5 and float(price_differ) >0:
            _temp.append('B')
        elif float(price_differ) <= 10 and float(price_differ) > 5:
            _temp.append('C')
        else:
            _temp.append('D')

        _list.append(_temp)

    _data = pandas.DataFrame(_list, columns=_column)
    return _data


def __get_right_dates(data):  #计算并添加车龄，返回pandas.dataframe格式
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    data = data.values
    _list = []

    for item in data:       #逐行添加车龄
        _temp=list(item)
        _create_date = _temp[_column_tags['create_date']]
        #year,month=nan,nan

        year,month,day =__get_year_and_month_and_day(_create_date)
        if pandas.isna(year) or pandas.isna(month):
            continue
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        #_age = round(now_year - year + float(now_month - month) / 12, 2)
        #_temp.append(_age)
        if year==now_year and month == 10:
            #print(str(month) + '-' + str(day))
            _list.append(_temp)

    _data=pandas.DataFrame(_list,columns=_column)
    return _data


def __write_data(path, data_ALL):  #写入数据到excel文件中，测试时候用的
    df = pandas.DataFrame()
    df.to_excel(path)
    writer = pandas.ExcelWriter(path)
    data = pandas.DataFrame(data_ALL).set_index(["id"])
    data.to_excel(writer, sheet_name='test1')
    writer.save()

def __get_year_and_month_and_day(date): #判断日期时间的类型并返回 年和月
    if date=='' or pandas.isna(date):
        return nan,nan
    elif not type(date)==float: #默认是datetime64，如果后期增加其他类的时间戳再增加判断条件
        year=date.year
        month=date.month
        day=date.day
        return year,month,day

    else:
        timeStamp = float(date / 1000)
        timeArray = time.localtime(timeStamp)
        return timeArray.tm_year, timeArray.tm_mon,timeArray.tm_mday

def __DB_access(source:str,test_flag:bool):   #从mysql爬数据，传入参数为线索源，返回为pandas.dataframe格式，该线索源的全部数据
    connect_luoma_kc = pymysql.connect(
        host='bj-cdb-bly32vza.sql.tencentcdb.com',
        port=62768,
        user='root', password='Roma123o))!@#*)',
        database='luoma_kc_sit',
        charset='utf8', use_unicode=True)

    if not test_flag:
        connect_luoma_kc = pymysql.connect(
            host='bj-cdb-fu5gl04c.sql.tencentcdb.com',
            port=63665,
            user='OperGuest', password='GuestLuoma!@#12',
            database='luoma_kc',
            charset='utf8', use_unicode=True)

    sql = "select * from kc_clues where source="+"'"+source+"'"
    data = pandas.read_sql(sql, con=connect_luoma_kc)
    connect_luoma_kc.close()
    return data

def __1DB_access(test_flag:bool):   #从mysql爬数据，传入参数为线索源，返回为pandas.dataframe格式，该线索源的全部数据
    connect_luoma_kc = pymysql.connect(
        host='bj-cdb-bly32vza.sql.tencentcdb.com',
        port=62768,
        user='root', password='Roma123o))!@#*)',
        database='luoma_kc_sit',
        charset='utf8', use_unicode=True)

    if not test_flag:
        connect_luoma_kc = pymysql.connect(
            host='bj-cdb-fu5gl04c.sql.tencentcdb.com',
            port=63665,
            user='OperGuest', password='GuestLuoma!@#12',
            database='luoma_kc',
            charset='utf8', use_unicode=True)

    sql = "select * from kc_clues where source= '"+"淘金"+"'"
    data = pandas.read_sql(sql, con=connect_luoma_kc)
    connect_luoma_kc.close()
    return data
def __level_helper(data,level):
    data=data[data['car_miles_level']==level]
    data = data[data['car_ages_level'] == level]
    data = data[data['car_price_level'] == level]
    data = data[data['car_price_differ_level'] == level]
    return data

def A__level_helper(data):
    data=data[(data['car_miles_level']=='A') | (data['car_miles_level']=='B')]
    data = data[(data['car_ages_level']=='A') | (data['car_ages_level']=='B')]
    data = data[(data['car_price_level']=='A') | (data['car_price_level']=='B')]
    data = data[(data['car_price_differ_level'] == 'A')|(data['car_price_differ_level'] == 'B')]
    return data

def B__level_helper(data):
    data=data[(data['car_miles_level']=='A') | (data['car_miles_level']=='B')|(data['car_miles_level']=='C')]
    data = data[(data['car_ages_level']=='A') | (data['car_ages_level']=='B')|(data['car_ages_level']=='C')]
    data = data[(data['car_price_level']=='A') | (data['car_price_level']=='B')|(data['car_price_level']=='C')]
    data = data[(data['car_price_differ_level'] == 'A')|(data['car_price_differ_level'] == 'B')|(data['car_price_differ_level']=='C')]
    return data

def C__level_helper(data):
    data=data[(data['car_miles_level']=='A') | (data['car_miles_level']=='B')|(data['car_miles_level']=='C')|(data['car_miles_level']=='D')]
    data = data[(data['car_ages_level']=='A') | (data['car_ages_level']=='B')|(data['car_ages_level']=='C')|(data['car_ages_level']=='D')]
    data = data[(data['car_price_level']=='A') | (data['car_price_level']=='B')|(data['car_price_level']=='C')|(data['car_price_level']=='D')]
    data = data[(data['car_price_differ_level'] == 'A')|(data['car_price_differ_level'] == 'B')|(data['car_price_differ_level']=='C')|(data['car_price_differ_level'] == 'D')]
    return data
if __name__ == '__main__':
    data=__1DB_access(False)
    #print(len(data.values))
    data=__get_right_dates(data)  #日期筛选
    data=__get_ages(data)

    data=__get_price_difference(data)
    print(len(data.values))
    data=__get_ages_level(data)
    data=__get_miles_level(data)
    data=__get_price_level(data)
    data=__get_price_differ_level(data)
    data_S=__level_helper(data,'A')
    data_A=A__level_helper(data)
    data_B=B__level_helper(data)
    data_C=C__level_helper(data)
    print('S:' + str(len(data_S.values)))
    print('A:' + str(len(data_A.values)))
    print('B:' + str(len(data_B.values)))
    print('C:' + str(len(data_C.values)))
    print('D:' + str(len(data_C.values)))
    #print(len(data_S.values))
    print('all:'+str(len(data.values)))

    #data=__get_status_level(data)
    #print(data['vehicles'])
    #target_file=r'F:\我的坚果云\日常工作/11-11/淘金_all.xlsx'
    #__write_data(target_file,data)