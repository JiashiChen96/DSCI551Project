#生产入口文件
import os
from flask import Flask,request
import base64
from plot_figure import __plot
from get_ages import __get_ages
from get_price_difference import __get_price_difference
from flask import make_response
from help_functions import __get_data
from get_data_list import __make_answer
import json
import logging

server = Flask(__name__)#创建一个服务
server.debug=False

@server.route('/data',methods=['get','post'])
def data():    #返回数据
    if request.method == 'GET':

        source=request.values.get('source')
        id_list=request.values.get('id')
        if id_list:
            id_list=id_list.strip()
        id_list_flag = False
        if id_list and not id_list=='':
            id_list_flag=True

        data,data_flag = __get_data(id_list_flag,id_list,source,False)

        if not data_flag:
            result = make_response('无有效数据',404)
            return result

    elif request.method== 'POST':
        source=request.json.get('source')
        #print(source)
        id_list=request.json.get('id')
        if id_list:
            id_list=id_list.strip()
        id_list_flag = False
        if id_list and not id_list=='':
            id_list_flag=True

        data,data_flag = __get_data(id_list_flag,id_list,source,False)  #根据传进来的id获取数据

        if not data_flag:  #data_flag=False说明无有效数据
            result = make_response('无有效数据',404)
            return result
    else:
        result = make_response('仅支持GET和POST请求',404)
        return result

    print("start processing...\n")

    _data=__get_ages(data)       #获取车龄
    _data=__get_price_difference(_data)  #获取差价偏离度
    if _data.empty:
        result = make_response('无有效数据', 404)
        return result
    ans_dic=__make_answer(_data)       #生成最终字典的方法

    return json.dumps(ans_dic,ensure_ascii=False) , 200


@server.route('/figure',methods=['get','post'])
def figure():  #返回base64图片
    if request.method == 'GET':
        source=request.values.get('source')
        id_list=request.values.get('id')  #一堆id
        if id_list:
            id_list=id_list.strip()
        id_list_flag = False
        if id_list and not id_list=='':  #判断有没有id传进来
            id_list_flag=True

        data,data_flag = __get_data(id_list_flag,id_list,source,False)

        if not data_flag:
            result = make_response('无有效数据',404)
            return result

    elif request.method== 'POST':
        source=request.json.get('source')
        id_list=request.json.get('id')
        if id_list:
            id_list=id_list.strip()
        id_list_flag = False
        if id_list and not id_list=='':
            id_list_flag=True

        data,data_flag = __get_data(id_list_flag,id_list,source,False)

        if not data_flag:
            result = make_response('无有效数据',404)
            return result

    else:
        result = make_response('仅支持GET和POST请求',404)
        return result

    print("start processing...\n")
    n_total = len(data)
    if n_total==0:
        result = make_response('无有效数据', 404)
        return result
    _data=__get_ages(data)       #获取车龄
    _data=__get_price_difference(_data)  #获取差价偏离度
    if _data.empty:
        result = make_response('无有效数据', 404)
        return result
    __plot(n_total,_data)       #画图函数，保存临时图片到本地当前路径

    with open(r'_test_reference_analysis_'+str(n_total)+'.png','rb') as f:
        res = base64.b64encode(f.read())    #读取临时图片转成base64
    os.remove('_test_reference_analysis_'+str(n_total)+'.png')  #删除临时图片
    result=make_response(res,200)
    return result

if __name__ == "__main__":
    #server.run(port=8090)
    server.run(host='0.0.0.0',port=8090)
