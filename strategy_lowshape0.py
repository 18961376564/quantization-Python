#以最基本的做T策略出发，降低夏普比率的同时，争取同等收益

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
def hold(sell_num,close,buy_total):
    tl=len(close)-1
    st_tmp=0
    for i in sell_num:
        st_tmp+=i
    hold_num=len(buy_total)-st_tmp
    hold=close[tl]
    return [hold,hold_num]

def asset(sell,sell_num,close,buy_total):
    sl=sell_total(sell, sell_num)
    tl=len(close)-1
    st_tmp=0
    for i in sell_num:
        st_tmp+=i
    hold_num=len(buy_total)-st_tmp
    hold=close[tl]
    ass=sl+hold*hold_num
    return ass


import pandas as pd
stockname='美诺华.xlsx'
df=pd.read_excel(stockname,usecols=[3,4,5,6,7],engine='openpyxl')
   #取某列第i行数据  df[col_name][i]

##############################设置初始参数#########################################
# buy0=41.97    #美诺华下跌周期
# startrow=416
# endrow=497   #最大值为row row=len(df['low'])
# goal_price=45

buy0=50.5
startrow=360
endrow=497   #最大值为row row=len(df['low'])
goal_price=60

buy_gap=0.02   #买入卖出gap
sell_gap=0.02
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




sp_rate=1
def T_strategy(buy,buy_total,buy_sum,sell,sell_num,sell_flag,buygap,sellgap,high,low,goal_price,sp_rate):
    break_flag=0
    leng = len(buy) - 1    #变量不能设置为len，在len = dataSet.__len__()中，定义了一个名为len的变量与len()方法重名，后期再遇到len时，python将其认为是len这个int类型的变量，而不是len()方法
    a = buy[leng] * (1 - buygap)
    b = round(a, 2)
    if (low < b):
        if (high < b):
            b = high
        buy.append(b)
        buy_total.append(b)
        buy_sum += b
        if (len(buy) > sp_rate):
            sp_rate = len(buy)
            print("加杠杆",buy,"日期索引",i,"即时杠杆",sp_rate,"买入T",buygap,"卖出T",sellgap)
        else:
            print("买入价格", b, "日期索引", i, "即时杠杆", len(buy), "买入T", buygap, "卖出T", sellgap)
    leng = len(buy) - 1
    if (leng > 0):
        if (leng < 3):
            a = buy[leng] * (1 + sellgap * leng)
            sell[sell_flag] = round(a, 2)
            if (high > sell[sell_flag]):
                del buy[1:]
                a = sell[sell_flag]
                buy[0] = a
                sell_num[sell_flag] = leng
                print("卖出价格", a , "卖出数量", leng, "卖出日期索引", i)
                sell_flag += 1
                sell.append(0)  # 每次要append，否则会超出内存
                sell_num.append(0)
        else:
            a = buy[leng] * (1 + sellgap * 2)
            sell[sell_flag] = round(a, 2)
            if (high > sell[sell_flag]):
                tmp_fl = leng - 1
                del buy[tmp_fl:]
                # a=sell[sell_flag]
                # buy[tmp_fl-1]=a
                sell_num[sell_flag] = 2
                print("卖出价格",sell[sell_flag],"卖出数量",2,"卖出日期索引",i)
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
            break_flag=1

    return buy,buy_total,buy_sum,sell,sell_num,sell_flag,sp_rate,break_flag

end_index=endrow

for i in range(startrow,endrow):    #range(开始索引，结束索引）
    high=df['high'][i]
    low =df['low'][i]
    break_flag=0
    if(len(buy)<2):
        buy,buy_total,buy_sum,sell,sell_num,sell_flag,sp_rate,break_flag=T_strategy(buy, buy_total, buy_sum, sell, sell_num, sell_flag, buy_gap, sell_gap, high, low, goal_price, sp_rate)
        if(break_flag==1):
            end_index = i
            break
    else:
        # newbuy=buy_gap*(1+(sp_rate-2)*0.5)       #mutishape1，夏普越高，gap越大
        # newsell = sell_gap * (1.2+(sp_rate-2)*0.8)

        ###策略B 中波动 中信证券
        # newbuy=buy_gap*1.5
        # newsell = sell_gap * 1.8

        ###策略C 高波动 万科A、美诺华 夏普5
        newbuy=buy_gap*3.5
        newsell = sell_gap * 2.5


        buy,buy_total,buy_sum,sell,sell_num,sell_flag,sp_rate,break_flag=T_strategy(buy, buy_total, buy_sum, sell, sell_num, sell_flag, newbuy, newsell, high, low, goal_price, sp_rate)
        if(break_flag==1):
            end_index=i
            break


# print(buy_total)
# print(buy)

# print(sell)
# print(sell_num)
#print("卖出总计",sell_total(sell,sell_num))

fee=0
fee=0.005*len(buy_total)+0.00102*asset(sell,sell_num,df['close'],buy_total)
end_index=end_index-startrow

print(stockname,"策略：2级递进T"," 买入T",buy_gap,"   卖出T",sell_gap)
print("买入总计",buy_sum)
print("资产总计",asset(sell,sell_num,df['close'],buy_total))
print("持仓情况",hold(sell_num,df['close'],buy_total))
print("fee:",fee)


intrest_beforefee=(asset(sell,sell_num,df['close'],buy_total)-buy_sum)/(buy0)
intrest_beforefee=round(intrest_beforefee,4)
intrest=(asset(sell,sell_num,df['close'],buy_total)-buy_sum-fee)/(buy0)
ist_weighted=intrest/(sp_rate*0.5)
intrest=round(intrest,4)
ist_weighted=round(ist_weighted,4)
intrest_year=round((intrest*365/end_index),4)
ist_year=round((ist_weighted*365/end_index),4)

print("夏普比例",sp_rate,"和扣费前利润率",intrest_beforefee,"实际利润率",intrest,"加权利润率",ist_weighted,"周期",end_index)
print("年化利率",intrest_year,"加权年化利率",ist_year)