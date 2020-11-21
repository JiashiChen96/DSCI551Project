import pymysql
import pandas
import Levenshtein
from numpy import nan
from clues_filter import __get_tags
from write_data import __write_data
import os

def __get_model_data(year:str,brand:str,model,series:str):

    if not pandas.isna(model):
        _string=str(model)
    else:
        _string=str(series)

    _string='%'+_string+'%'

    connect_luoma = pymysql.connect(
        host='bj-cdb-fu5gl04c.sql.tencentcdb.com',
        port=63665,
        user='OperGuest', password='GuestLuoma!@#12',
        database='luoma',
        charset='utf8', use_unicode=True)

    sql = "select * from che300model where model_name like "+"'"+_string+"'"+';'
    data = pandas.read_sql(sql, con=connect_luoma)
    connect_luoma.close()
    #print(data)
    #print('found data!!!')
    return data

def __get_model_id(brand,model,series,year):

    if year:
        data=__get_model_data(year,brand,model,series)
    else:
        data=__get_model_data(None,brand,model,series)

    data_dic=__data_filter(data)
    _string1=__string_match(data_dic,str(series),year)

    if _string1=='not found':
        return nan

    model_id=data_dic[_string1]
    return model_id[0]


def __string_match(_dic:dict,_series:str,year)->str:

    if _series.find('20')>=0:
        _string=_series
    else:
        _string=str(year)+_series

    _list=list(_dic.keys())
    try:
        _max=Levenshtein.jaro_winkler(_list[0],_series)
    except:
        #print('Ooop, not found\n')
        #print(_series)
        return 'not found'
    _max_string=_list[0]

    for _string in _list[1:]:
        _temp=Levenshtein.jaro(_series,_string)
        if _temp>=_max:
            _max=_temp
            _max_string=_string

    return _max_string

def __data_filter(data):

    data=data[['model_name','model_id']]
    data=data.set_index('model_name').T.to_dict('list')

    return data


def __add_model_id(source_file):


    data = pandas.read_excel(source_file)
    _column_tags=__get_tags(data)
    _column=list(_column_tags.keys())
    _column.append('model_id')
    _list=[]
    data=data.values

    for item in data:
        _temp=list(item)
        _list.append(_temp)

    for item in _list:
        year=item[_column_tags['license_date']].year
        brand=item[_column_tags['brand']]
        series=item[_column_tags['series']]
        model = item[_column_tags['model']]

        item.append(__get_model_id(brand, model, series, year))

    _data = pandas.DataFrame(_list, columns=_column)
    if os.path.isfile(source_file):
        os.remove(source_file)
    __write_data(source_file,_data)
    return
