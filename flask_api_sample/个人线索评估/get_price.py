import pandas
import os
from write_data import __write_data
from clues_filter import __get_tags
import requests
import json
from numpy import nan
from time import sleep

def __get_price(city_id,model_id,miles,reg_date):
    url='http://api.che300.com/service/getUsedCarPrice?token=69f6adb19f1663e52eb62d3240a8e0e4'+\
        '&modelId='+str(int(model_id))+'&regDate='+str(reg_date)+'&mile='+str(miles)+'&'+'zone='+str(city_id)
    #print(model_id)
    response=requests.get(url)
    jsonstr = json.loads(response.text)
    #print(jsonstr)
    try:
        #print(jsonstr)
        _price=jsonstr['eval_price']
    except:
        _price=nan
    #print(_price)
    return _price


def __fetch_data(source_file):
    data=pandas.read_excel(source_file)
    _column_tags=__get_tags(data)
    data=data.values
    _column=list(_column_tags.keys())
    _column.append('eval_price')
    _list=[]

    for item in data:
        sleep(1)
        _temp = list(item)
        model_id = _temp[_column_tags['model_id']]
        city_id = _temp[_column_tags['city_id']]
        if pandas.isna(model_id):
            _temp.append(nan)
            _list.append(_temp)
            continue
        miles = _temp[_column_tags['miles']]
        time = _temp[_column_tags['license_date']]
        reg_date = str(time.year) + '-' + str(time.month)
        if pandas.isna(time):
            reg_date='2013-10'

        _eval_price = __get_price(city_id, model_id, miles, reg_date)
        _temp.append(_eval_price)
        _list.append(_temp)
    _data = pandas.DataFrame(_list, columns=_column)
    return _data

def __get_eval_price(source_file):
    data=__fetch_data(source_file)
    if os.path.isfile(source_file):
        os.remove(source_file)
    __write_data(source_file,data)
    return







