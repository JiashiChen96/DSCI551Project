#测试文件，对功能没影响
import pymysql
import pandas
from help_functions import __get_tags
import datetime
#from helper_functions import __get_tags
import base64
import requests
import json
import collections
from help_functions import __get_sources
import os
import sys

def __write_data(path, data_ALL):
    df = pandas.DataFrame()
    df.to_excel(path)
    writer = pandas.ExcelWriter(path)
    data = pandas.DataFrame(data_ALL).set_index(["id"])
    data.to_excel(writer, sheet_name='test1')
    writer.save()

def __db_access(source:str):

    connect_luoma_kc = pymysql.connect(
    host='bj-cdb-fu5gl04c.sql.tencentcdb.com',
    port=63665,
    user='OperGuest', password='GuestLuoma!@#12',
    database='luoma_kc',
    charset='utf8', use_unicode=True)

    sql = "select * from kc_clues where source=" + "'" + source+"'"
    data = pandas.read_sql(sql, con=connect_luoma_kc)
    connect_luoma_kc.close()
    return data
"""
source='淘金'
url='http://192.168.1.91:2333/clue_analysis'
raw_file = 'F:\我的坚果云\日常工作/10-12/'+source+'/' + source +'_raw.xlsx'
target_picture = 'F:\我的坚果云\日常工作/10-12/'+source+'/' + source +'.png'
#_temp_picture='test1111.jpg'
if __name__ == '__main__':
    _data=pandas.read_excel(raw_file)
    _data=_data.to_json(orient='records')
    _headers = {'Content-Type': 'application/json'}

    response=requests.post(url,data=_data,headers=_headers).content
    response=base64.b64decode(response)
    with open(target_picture, 'wb') as f:
        f.write(response)
        f.close()
"""
if __name__ == "__main__":
    source='淘金'
    _data=__db_access(source)
    #__write_data(_temp_file,_data)
    _data=_data[_data['city']=='北京']
    _tags=__get_tags(_data)
    _id=[]
    for item in _data.values:
        date=item[_tags['create_date']]
        date=pandas.to_datetime(date)
        if date.month==datetime.datetime.now().month and date.day==datetime.datetime.now().day-7:
            _id.append(item[_tags['id']])
    #_data=_data['id']
    #_temp=_data.values
    #print(_data.values)
    #_data=_data.to_json(orient='records')
    #_headers = {'Content-Type': 'application/json'}
    url1 = 'http://49.233.202.104:8090/data'
    #url1 = 'http://127.0.0.1:5124/data?id=1,2,3,4,5'
    #url = 'http://127.0.0.1:23333/clue_analysis'
    url = 'http://152.136.163.201:2333/clue_analysis'
    body={

        'source':'淘金',
        #'id':'13697'
    }
    if len(_id)==0:
        print('todays data is not ready\n')
        sys.exit()
    _ids = ''
    for item in _id[0:-1]:
        _ids += str(item) + ','
    _ids += str(_id[-1])
    url = url+_ids
    #print(url)
    #response = requests.post(url, data=_data, headers=_headers)
    response=requests.post(url=url1,json=body)
    if response.status_code==200:
        print(str(response.content))
        #json_1=response.content
        #data=json.loads(json_1)
        #print(data)
        #f1 = open('F:\我的坚果云\日常工作/11-01/'+source+'/' + 'test.txt', 'wb')
        #f1.write(response.content)
        #response = base64.b64decode(response.content)
        #month=str(datetime.datetime.now().month)
        #day=str(datetime.datetime.now().day)
        #_date=month+'_'+day
        #target_picture = 'F:\我的坚果云\日常工作/11-01/'+source+'/' + source+'_苏州' +'_test'+_date+'_.png'
        #if os.path.isfile(target_picture):
            #os.remove(target_picture)
        #with open(target_picture, 'wb') as f:
            #f.write(response)
            #f.close()
    elif response.status_code==404:
        print(response.text)

