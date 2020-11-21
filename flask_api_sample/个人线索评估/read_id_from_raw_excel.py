import pandas

def __get_id(source_file):
    data=pandas.read_excel(source_file)
    data=data.values
    _id_list=[]
    for item in data:
        _id_list.append(item[0])
    return _id_list

if __name__ == '__main__':
    id_list=__get_id('F:\我的坚果云\个人线索评估\温建同.xlsx')
    print(id_list)
