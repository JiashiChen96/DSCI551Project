####返回数据（列表套字典）
import numpy
import copy
from help_functions import __get_tags
import pandas

def __get_date(_date_info):  #根据不同日期格式，获得具体日期的年月日，返回日期字符串
    if isinstance(_date_info,numpy.datetime64):
        data = pandas.to_datetime(_date_info)
        return str(data.year)+'-'+str(data.month)+'-'+str(data.day)
    elif isinstance(_date_info,pandas.Timestamp):
        data=_date_info
        return str(data.year)+'-'+str(data.month)+'-'+str(data.day)
    else:
        print(type(_date_info))
        return ''

def __update_dic(date,_date_dic,ages,price,miles,price_differ):  #根据日期，更新字典
    if not date in _date_dic:  # 新日期
        _date_dic.update({date: {}})
        _temp = _date_dic[date]
        _temp.update({'ages': [ages]})
        _temp.update({'price': [price]})
        _temp.update({'miles': [miles]})
        _temp.update({'price_differ': [price_differ]})
        if price >= 15:
            _temp.update({'over15': [price]})
        else:
            _temp.update({'over15': []})
        _temp.update({'total_score': 0})

    else:  # 日期存在
        _temp = _date_dic[date]
        _temp['ages'].append(ages)
        _temp['price'].append(price)
        _temp['miles'].append(miles)
        _temp['price_differ'].append(price_differ)
        if price >= 15:
            _temp['over15'].append(price)

    return _date_dic

def __get_scores(_sub_dic):   #计算分数并返回，输入：根据日期分好组，并计算出中位数/占比 的字典
                                #输出：计算好各项分数的字典
    ages=float(4-_sub_dic['ages'])/6.0*100+100      #车龄满分4年，0分10年
    price=float(_sub_dic['price']-10.0)/10*100+100    #价格满分10W，0分0W
    miles=float(4-_sub_dic['miles'])/16.0*100+100     #里程0分20W公里，满分4W公里                #生成各项分数（都是越高越好）
    over15=float(_sub_dic['over15']-0.1)/0.1*100+100   #高于15W车，满分10%，0分0%
    price_differ=float(0-_sub_dic['price_differ'])*100+100 #差价偏离度，满分0分100%

    total_score=round((ages+price+miles+over15+price_differ)/5,2) #总分

    _sub_dic.update({'ages_score':round(ages,2)})
    _sub_dic.update({'price_score': round(price,2)})
    _sub_dic.update({'price_differ_score': round(price_differ,2)})  #将分数打包到socre_dic里面
    _sub_dic.update({'miles_score': round(miles,2)})
    _sub_dic.update({'over15_score':round(over15,2)})
    _sub_dic.update({'total_score':round(total_score,2)})
    return _sub_dic

def __anslysis_by_date_helper(_temp_dic):  #计算各项中位数/占比，并写入原字典返回
    _temp = _temp_dic
    _temp['over15'] = round(float(len(_temp['over15'])) / float(len(_temp['price'])), 2)
    _temp['ages'] = round(numpy.median(_temp['ages']), 2)
    _temp['price'] = round(numpy.median(_temp['price']), 2)
    _temp['miles'] = round(numpy.median(_temp['miles']), 2)
    _temp['price_differ'] = round(numpy.median(_temp['price_differ']), 2)
    _temp = __get_scores(_temp)
    return _temp

def __analysis_by_date(_date_dic):  #根据日期分析数据，输入：根据日期分好组的数据字典
                                    #输出： 根据各项数据计算好中位数/占比的数据字典

    dates=list(_date_dic.keys())
    if len(dates)>=2:
        for date in dates:
            _temp=_date_dic[date]
            _temp = __anslysis_by_date_helper(_temp)
    else:
        _temp = _date_dic[dates[0]]
        _temp=__anslysis_by_date_helper(_temp)

    return _date_dic

def __get_special_deal_price(_str): #一些心理价是‘4-5’或者‘5点多’这种，包含特殊字符需要特殊处理
    _ans=''
    for i in _str:
        if i.isdigit():
            _ans+=i
        else:
            break
    return round(float(_ans),2)

def __group_data_by_date(_data):  #根据日期对数据进行分组，输入：原始数据
                                #输出：根据日期分好组的数据字典
    _tags = __get_tags(_data)
    _data = _data.values
    _date_dic = {}
    for item in _data:
        date = __get_date(item[_tags['create_date']])
        if len(date) == 0:
            continue
        ages = float(item[_tags['car_ages']])
        try:
            miles = float(item[_tags['miles']])
        except:
            miles = 3.0

        if miles > 1000:
            miles = miles / 10000  # 一些不到一万公里的车，单位不是万公里，需要换成万公里
        price = float(item[_tags['valuation']])
        try:
            deal_price = float(item[_tags['deal_price']])
        except:
            deal_price = __get_special_deal_price(item[_tags['deal_price']])

        price_differ = 0
        try:
            price_differ = (float(deal_price) - float(price)) / price
            price_differ = round(price_differ, 2)
        except:
            price_differ = 0

        _date_dic = __update_dic(date, _date_dic, ages, price, miles, price_differ) #根据日期更新字典

    return _date_dic

def __make_answer(_data):  #文件总入口，主文件调这个方法，返回包含一个个字典的列表

    _date_dic=__group_data_by_date(_data)
    _date_dic=__analysis_by_date(_date_dic)
    _date_list = []

    for date in list(_date_dic.keys()):
        _temp_dic=copy.deepcopy(_date_dic[date])
        _temp_dic.update({'time':date})
        _date_list.append(_temp_dic)

    return _date_list