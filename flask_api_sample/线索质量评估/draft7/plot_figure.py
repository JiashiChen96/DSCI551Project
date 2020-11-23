####画图，代码全是粘的，就不写注释了
import numpy
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from pandas import isna
def __get_miles_median(_data):  #获取公里数的中位数
    _data=_data['miles']
    _data=_data.values
    _list=[]
    for item in _data:
        if isna(item):
            continue
        elif not item.isdigit():
            continue
        elif float(item)>800:
            _list.append(float(item)/10000)  #一些不到一万公里的车，公里数录入的是x000四位数，需要特殊处理
        else:
            _list.append(float(item))

    return numpy.median(_list)

def __plot(n_total,_data):

    _price = _data['valuation'].median()  # 估价中位数
    _ages = _data['car_ages'].median()  # 车龄中位数
    _miles=__get_miles_median(_data)   #公里数中位数
    _price_differ = (_data['price_differ'] ).median()/100.0  # 差价偏离度
    _expensive_cars = len(_data[_data['valuation'] > 15]) / n_total  # 高于15W车辆占比

    _value=[(4-_miles)/16.0*100,(_price-10)/10.0*100,(4-_ages)/6.0*100,\
            (0.0-_price_differ)*100,(_expensive_cars-0.1)*1000]    #此列表存储的为扣掉的分数

    for i in range(len(_value)):
        #print(_value[i])
        _value[i]=round(_value[i],2)

    lables = ['公里数(中位数): '+str(round(_miles,2))+'万\n'+'分数',\
              '估价(中位数): '+str(round(_price,2))+'万\n'+'分数',\
              '车龄(中位数): '+str(round(_ages,2))+'年\n'\
              +'分数','差价偏离度: '+str(round(_price_differ*100,2))+'%\n'+'分数',\
              '高于15W占比: '+str(round(_expensive_cars*100,2))+'%\n'+'分数']

    for i in range(len(lables)):        #100加上扣掉的分数为最后各项分数
        _value[i]=100+_value[i]
        lables[i]+=': '+str(round(_value[i],2))

    _total_scores=round((_value[0]*0.3+_value[1]*0.15+_value[2]*0.3+_value[3]*0.1+_value[4]*0.15),2)

    for i in range(len(lables)):
        if _value[i]<0:
            _value[i]=0


    lables=numpy.array(lables)
    _value=numpy.array(_value)
    dataLenth=5

    angles = numpy.linspace(0, 2*numpy.pi, dataLenth, endpoint=False)

    adj_angle = angles[-1] + numpy.pi/2 - 2*numpy.pi
    angles += adj_angle

    _value = numpy.concatenate((_value, [_value[0]])) # 闭合
    angles = numpy.concatenate((angles, [angles[0]])) # 闭合


    X_ticks = angles
    X = numpy.append(X_ticks,X_ticks[0])



    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)# polar参数！！
    ax.plot(angles, _value, 'bo-', linewidth=0.2)# 画线

    ax.set_xticks(X)

    ax.fill(angles, _value, facecolor='r', alpha=0.25)# 填充
    ax.set_thetagrids(angles * 180/numpy.pi, lables, fontproperties="SimHei")
    ax.set_title("车辆线索质量评估: 总分:"+str(_total_scores)+'\n', va='bottom', fontproperties="SimHei")
    ax.set_rlim(0,110)

    ax.set_xticklabels(lables, fontproperties ="SimHei" , fontsize = 'small') # 设置标签
    ax.set_yticklabels([])

    ax.spines['polar'].set_visible(False)
    ax.grid(axis='y')



    n_grids = numpy.linspace(0,110, 12, endpoint=True) # grid的网格数
    grids = [[i] * (len(X)) for i in n_grids] #grids的半径

    for i, grid in enumerate(grids[:-1]): # 给grid 填充间隔色
        ax.plot(X, grid, color='grey', linewidth=0.2)
        if (i>0) & (i % 2 == 0):
            ax.fill_between(X, grids[i], grids[i-1], color='grey', alpha=0.1)

    plt.savefig('_test_reference_analysis_'+str(n_total)+'.png')  #临时图片是动态名字，防止重复访问/删除
    #plt.show()
    plt.close(fig)
