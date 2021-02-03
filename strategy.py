#买入价为基础，中信证券有预期，坚决逢低买入，做T区间看市场热度。加仓：逢2%加仓。
# 做T:持仓6万元以下不低于1.5%（40分钱），以上逢2%加仓，0.8%做T。
def sell_total(sell,sell_num):
    l = len(sell)
    if(len(sell)!=len(sell_num)):
        print("卖出程序错误")
        return 0
    else:
        sum=0
        for i in range(l):
            sum+=sell[i]*sell_num[i]
        return sum
def hold(sell_num,close,endrow,buy_total):
    st_tmp=0
    for i in sell_num:
        st_tmp+=i
    hold_num=len(buy_total)-st_tmp
    hold=close[endrow]
    return [hold,hold_num]

def asset(sell,sell_num,close,endrow,buy_total):
    sl=sell_total(sell, sell_num)
    st_tmp=0
    for i in sell_num:
        st_tmp+=i
    hold_num=len(buy_total)-st_tmp
    hold=close[endrow]
    ass=sl+hold*hold_num
    return ass



import pandas as pd
df=pd.read_excel('中信证券.xlsx',usecols=[3,4,5,6,7],engine='openpyxl')
   #取某列第i行数据  df[col_name][i]


##############################设置初始参数#########################################

startrow=276
endrow=332   #最大值为row row=len(df['low'])
buy0=df['high'][startrow]
goal_price=buy0*1.1

##############################设置初始参数##############################

buy=list()
buy.append(buy0)
buy_total=list()
buy_total.append(buy0)
buy_sum=buy0
sell=list()
sell.append(0)
sell_num=list()
sell_num.append(0)
sell_flag=0
sell_sum=0
buy_gap=0.03   #买入卖出gap
sell_gap=0.03
sp_rate=1
end_index=endrow
for i in range(startrow,endrow):

    high=df['high'][i]
    low =df['low'][i]
    leng = len(buy) - 1  # 变量不能设置为len，在len = dataSet.__len__()中，定义了一个名为len的变量与len()方法重名，后期再遇到len时，python将其认为是len这个int类型的变量，而不是len()方法
    a = buy[leng] * (1 - buy_gap)
    b = round(a, 2)
    if (low < b):
        if (high < b):
            b = high
        buy.append(b)
        buy_total.append(b)
        buy_sum += b
        if (len(buy) > sp_rate):
            sp_rate = len(buy)
            print("加杠杆", buy, "日期索引", i, "即时杠杆", sp_rate, "买入T", buy_gap, "卖出T", sell_gap)
        else:
            print("买入价格", b, "日期索引", i, "即时杠杆", len(buy), "买入T", buy_gap, "卖出T", sell_gap)
    leng = len(buy) - 1
    if (leng > 0):
        if (leng < 3):
            a = buy[leng] * (1 + sell_gap * leng)
            sell[sell_flag] = round(a, 2)
            if (high > sell[sell_flag]):
                del buy[1:]
                a = sell[sell_flag]
                buy[0] = a
                sell_num[sell_flag] = leng
                print("卖出价格", a, "卖出数量", leng, "卖出日期索引", i)
                sell_flag += 1
                sell.append(0)  # 每次要append，否则会超出内存
                sell_num.append(0)
        else:
            a = buy[leng] * (1 + sell_gap * 2)
            sell[sell_flag] = round(a, 2)
            if (high > sell[sell_flag]):
                tmp_fl = leng - 1
                del buy[tmp_fl:]
                # a=sell[sell_flag]
                # buy[tmp_fl-1]=a
                sell_num[sell_flag] = 2
                print("卖出价格", sell[sell_flag], "卖出数量", 2, "卖出日期索引", i)
                sell_flag += 1
                sell.append(0)  # 每次要append，否则会超出内存
                sell_num.append(0)
    else:
        if (high > goal_price):
            sell[sell_flag] = goal_price
            sell_num[sell_flag] = leng + 1
            print("达到目标价格，全部卖出：", sell[sell_flag], "卖出数量", sell_num[sell_flag], "卖出日期索引", i)
            sell_flag += 1
            sell.append(0)
            sell_num.append(0)
            break


fee=0
fee=0.005*len(buy_total)+0.00102*asset(sell,sell_num,df['close'],endrow,buy_total)

print("买入T",buy_gap,"   卖出T",sell_gap)
print("买入总计",buy_sum)
print("资产总计",asset(sell,sell_num,df['close'],endrow,buy_total))
print("持仓情况",hold(sell_num,df['close'],endrow,buy_total))

intrest=(asset(sell,sell_num,df['close'],endrow,buy_total)-buy_sum)/(30*sp_rate*0.5)
intrest=round(intrest,4)
end_index=end_index-startrow
print("fee:",fee)
print("夏普比例",sp_rate,"和利润率",intrest,"周期",end_index,"年化利率",round((intrest*365/end_index),4))
