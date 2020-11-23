import pandas
from help_functions import __get_tags
import time
import datetime
from numpy import nan

def __get_year_and_month(date): #判断日期时间的类型并返回 年和月

    if date=='' or pandas.isna(date):
        return nan,nan
    elif not type(date)==float: #默认是datetime64，如果后期增加其他类的时间戳再增加判断条件
        year=date.year
        month=date.month
        return year,month

    else:
        timeStamp = float(date / 1000)
        timeArray = time.localtime(timeStamp)
        return timeArray.tm_year, timeArray.tm_mon

def __get_ages(data):  #计算并添加车龄，返回pandas.dataframe格式
    _column_tags = __get_tags(data)  # 获取列名
    _column = list(_column_tags.keys())
    _column.append('car_ages')  # 添加 "车龄" 列
    data = data.values
    _list = []

    for item in data:       #逐行添加车龄
        _temp=list(item)
        _license_date = _temp[_column_tags['license_date']]
        year,month=nan,nan

        year,month =__get_year_and_month(_license_date)
        if pandas.isna(year) or pandas.isna(month):  #有无效的就跳过
            _temp.append(nan)
            _list.append(_temp)
            continue
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        _age = round(now_year - year + float(now_month - month) / 12, 2) #计算车龄
        _temp.append(_age)
        _list.append(_temp)

    _data=pandas.DataFrame(_list,columns=_column)
    return _data