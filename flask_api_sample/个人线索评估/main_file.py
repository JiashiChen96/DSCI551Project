from read_id_from_raw_excel import __get_id
from get_raw_data import __DB_access
from write_data import __write_data
import os
from clues_filter import __get_useful_data
from get_city_id import __get_city_id
from _get_model_id import __add_model_id
from get_price import __get_eval_price
from get_ages import __get_ages



print('请输入合伙人姓名：\n')
_name=input()
raw_data_file='F:\我的坚果云\个人线索评估'+'/'+_name+'_raw'+'.xlsx'
useful_data_file='F:\我的坚果云\个人线索评估'+'/'+_name+'_useful'+'.xlsx'

print('处理中\n')


if not os.path.isfile(raw_data_file):
    source_file = 'F:\我的坚果云\个人线索评估' + '/' + _name + '.xlsx'
    _id_list=__get_id(source_file)
    raw_data=__DB_access(_id_list)
    __write_data(raw_data_file,raw_data)
    os.remove(source_file)

'''
_useful_data=__get_useful_data(raw_data_file)
__write_data(useful_data_file,_useful_data)
__get_city_id(useful_data_file)
__add_model_id(useful_data_file)
'''

#__get_eval_price(useful_data_file)
__get_ages(useful_data_file)