import pandas
from write_data import __write_data
from clues_filter import __get_tags
import datetime
import os
def __get_ages_helper(source_file):
    data=pandas.read_excel(source_file)
    _column_tags=__get_tags(data)
    data=data.values
    _column=list(_column_tags.keys())
    _column.append('age')
    _list=[]
    for item in data:
        _temp=list(item)
        _license_date=_temp[_column_tags['license_date']]
        _age=(datetime.datetime.now()-_license_date).days/365
        _age=round(_age,2)
        _temp.append(_age)
        _list.append(_temp)

    _data=pandas.DataFrame(_list,columns=_column)
    return _data

def __get_ages(source_file):
    data=__get_ages_helper(source_file)
    if os.path.isfile(source_file):
        os.remove(source_file)
    __write_data(source_file,data)
    return

