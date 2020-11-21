import pandas

def __get_tags(data):
    _dic = {}
    _list = data.columns
    #print(_list)
    for i in range(len(_list)):
        _dic.update({_list[i]: i})
    return _dic



def __get_useful_data(source_file):
    data=pandas.read_excel(source_file)
    _column_tags=__get_tags(data)
    data=data.values
    _list=[]
    _column = list(_column_tags.keys())[:]
    for item in data:
        if not int(item[_column_tags['status']])==30:
            _list.append(item)
    _useful_data = pandas.DataFrame(_list, columns=_column)
    return _useful_data

