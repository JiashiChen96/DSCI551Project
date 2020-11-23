from help_functions import __get_tags
import pandas
from numpy import nan

def __deal_price_process(deal_price):  #筛掉包含特殊字符或者空字符串的用户心理价格
    _ans=""
    deal_price.strip()
    for i in deal_price:
        if i.isdigit():
            _ans+=i
        else:
            break
    return _ans

def __convert_str_to_float(_str):   #转换价格变量类型
    _ans=0
    try:
        _ans=float(_str)

    except:
        _temp=''
        #print('error ones: '+_str)
        for i in _str:
            if i.isdigit():
                _temp.append(i)
        _ans=float(_temp)

    finally:
        return _ans

def __get_price_difference(data):  #计算用户心里价格和实际估价的差距(百分比)，并返回添加完成的 dataframe
    _column_tag=__get_tags(data)  #获取列名并储存对应的index
    _column=list(_column_tag.keys())#列名保存为字典
    _column.append('price_differ')
    _list=[]
    data=data.values
    for item in data:
        _temp=list(item)
        price=_temp[_column_tag['valuation']]
        deal_price=_temp[_column_tag['deal_price']]
        if pandas.isna(price) or pandas.isna(deal_price) or not price or not deal_price:
            _temp.append(nan)
            continue

        price = float(price)
        try:
            deal_price = float(deal_price)       #个别的价格是个区间或者带汉字
        except:
            deal_price=__deal_price_process(deal_price)

        if deal_price=='':
            continue
        else:
            deal_price=float(deal_price)
        price_differ=(deal_price-price)/price

        price_differ=round(price_differ*100,2)  #这个是差价的百分比
        _temp.append(price_differ)
        _list.append(_temp)
    _data=pandas.DataFrame(_list,columns=_column)
    return _data