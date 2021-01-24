#如果发现历史大概率均线策略有效，是否可以以此构造随机均线策略？？？

#单只股票以时间段T频率  判断是否调仓  T=49表现最好
# 下面的数字表示unit(总资产的1%)
# 调仓信号：
# 微上穿+1，中上穿+4，高度上穿满仓
# 微下穿-1，中下穿-4，高度下穿空仓
# coding=utf-8

import math
import tushare as ts
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import numpy as np
import talib

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus']=False
ts.set_token('8031035535f8e89792cfc111867fefe422380dade4f134e736f7df1d')#网址 https://tushare.pro/register?reg=385920
pro = ts.pro_api()
#读取数据
df = pro.query('daily', ts_code='000002.SZ', start_date='20110801', end_date='20200810')
df=df.sort_index()
df.index=pd.to_datetime(df.trade_date,format='%Y-%m-%d')#设置日期索引

T=24
atr1 = talib.ATR(df['high'].values, df['low'].values, df['close'].values,timeperiod=T)
atr = pd.DataFrame(atr1)
atr=atr.sort_index()
atr.index=pd.to_datetime(df.trade_date,format='%Y-%m-%d')#设置日期索引
atr=atr.fillna(0)
mv=talib.MA(np.array(df.close), timeperiod=T)
close10=mv+0.5*atr1
close100=mv+atr1
close1000=mv+1.5*atr1
unit=10000/(100*atr1[-1])
close10_=mv-0.5*atr1
close100_=mv-atr1
close1000_=mv-1.5*atr1
unit=10000/(100*atr1[-1])
#收市股价
close= df.close
#每天的股价变动百分率
ret=df.change/df.close

# 10日的移动均线为目标

#处理信号
SmaSignal=pd.Series(0,index=close.index)
s=0
k=0
for i in range(T,len(close)):
    if all(  [  close[i]>close10[i], SmaSignal[i-1]<100, close[i]<close100[i]  ]  ):
        SmaSignal[i]=1+SmaSignal[i-1]
        #print("买一次")
    elif all ([close[i]>close100[i],SmaSignal[i-1]<=96,close[i]<close1000[i]]):
            SmaSignal[i]=4+SmaSignal[i-1]
    elif all ([close[i]>close100[i],SmaSignal[i-1]<=100,close[i]<close1000[i]]):
            SmaSignal[i]=100
    elif all ([ close[i]>close1000[i],SmaSignal[i-1]<=100 ]):
            SmaSignal[i]=100
    elif all([close[i]<close10_[i],SmaSignal[i-1]>0,close[i]>close100_[i]]):
            SmaSignal[i]=SmaSignal[i-1]-1
    elif all ([close[i]<close100_[i],SmaSignal[i-1]>=4,close[i]<close1000_[i]]):
            SmaSignal[i]=SmaSignal[i-1]-4
    elif all ([close[i]<close100_[i],SmaSignal[i-1]>=0,close[i]<close1000_[i]]):
            SmaSignal[i]=0
    elif all ([close[i]<close1000_[i],SmaSignal[i-1]<=100]):
            SmaSignal[i]=0
    else:
        SmaSignal[i]=SmaSignal[i-1]
SmaTrade=SmaSignal.shift(1).dropna()/100#shift(1)整体下移一行
#SmaBuy=SmaTrade[SmaTrade==1]
#SmaSell=SmaTrade[SmaTrade==-1]
SmaRet=ret*SmaTrade.dropna()

#累积收益表现
#股票累积收益率
cumStock=np.cumprod(1+ret[SmaRet.index[0:]])-1
#策略累积收益率
cumTrade=np.cumprod(1+SmaRet)-1
plt.plot(cumTrade,label="海龟策略",color='r',linestyle=':')
plt.plot(cumStock,label="直接持有",color='k')
plt.title("49日平均线调仓策略收益率")
plt.legend()

plt.show()

f=cumTrade[-2]*250/len(close)
f1=100*f
print("年化收益率：{:.2f}%,总收益{:.2f}%".format(f1,f1*len(close)/250))