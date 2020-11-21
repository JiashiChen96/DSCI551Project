from clues_filter import __get_tags
import pandas
import requests
import json
from numpy import nan
import os
from write_data import __write_data

def __get_city_dic():
    city_api = 'http://api.che300.com/service/getAllCity?token=69f6adb19f1663e52eb62d3240a8e0e4'
    _dic = {}
    response = requests.get(city_api)
    jsonstr = json.loads(response.text)
    _list = jsonstr['city_list']

    for item in _list:
        _dic.update({item['city_name']: item['city_id']})

    return _dic


def __get_city_id_helper(source_file):
    data=pandas.read_excel(source_file)
    _column_tags=__get_tags(data)
    data=data.values
    _column=list(_column_tags.keys())
    _column.append('city_id')
    _list=[]
    _city_dic=__get_city_dic()

    for item in data:
        _temp=list(item)
        try:
            _city_id=_city_dic[_temp[_column_tags['city']]]
            _temp.append(_city_id)
        except:
            _temp.append(nan)
        _list.append(_temp)
    return pandas.DataFrame(_list,columns=_column)

def __get_city_id(source_file):
    data=__get_city_id_helper(source_file)
    if os.path.isfile(source_file):
        os.remove(source_file)
    __write_data(source_file,data)




