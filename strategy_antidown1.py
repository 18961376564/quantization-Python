#####
# 低点买入交易策略：买入点 达到前45日低点买入  涨6%卖出或跌3%卖出
# 1（本文档）中改进改进： 未来3天有2%上浮的买入
# 2 未来3天有2%上浮的买入，再涨2%加一倍仓（看成功率决定是否放大倍数），盈利归零卖出。如没有出现买入点的，视为无效点

#####

def Sum(list):
    sum=0
    for i in list:
        sum+=i
    return sum



import pandas as pd
df=pd.read_excel('春秋航空.xlsx',usecols=[2,3,4,5,6,7],engine='openpyxl')

gap=50   #约定的计算周期 取gap天最低点

buy=[]
sell=[]
close=df['close']
low=df['low']
high=df['high']
date=df['trade_date']
lenth=len(close)
buy_date=0
sell_date=0
breakgap=0
win=0
lose=0
for i in range(gap,lenth-4):
    if(i>breakgap):
        sell_flag=0
        tmp_low=low[i-gap:i]
        verylow=min(tmp_low)
        # if(low[i-1]>verylow and low[i]<verylow and close[i+1]>close[i]):
        if(low[i-1]>verylow and low[i]<verylow ):
            for k in range(i+1,i+4):
                if(high[k]>verylow*1.02):
                    buy_signal=round(verylow*1.02,2)
                    buy.append(buy_signal)
                    buy_date=date[k]
            ###加入一个条件  且第二天收盘价高于前一天收盘价的
            #close[i] > close[i - 1]
            ###加入一个条件  且第二天收盘价高于前一天收盘价的
                    print("buy",buy_date,"price",buy_signal)
                    while(sell_flag==0):
                        if(k<lenth-3):
                            for j in range(k+1,lenth-1):
                                if(high[j]>buy[-1]*1.08):
                                    sell_flag=1
                                    sell.append(round(buy[-1]*1.08,2))
                                    sell_date = date[j]
                                    print("sell",sell_date,"price",sell[-1])
                                    breakgap=j
                                    win+=1
                                    break
                                elif(low[j]<buy[-1]*0.98):
                                    sell_flag=1
                                    sell.append(round(buy[-1]*0.98,2))
                                    sell_date = date[j]
                                    print("sell",sell_date,"price",sell[-1])
                                    breakgap = j
                                    lose+=1
                                    break
                            if(sell_flag==0):
                                breakgap=lenth-1
                                tmp_hold=buy[-1]
                                sell.append(tmp_hold)
                                print("没能卖出",buy[-1])
                            break
                        else:
                            break
                    break




print('win:',win,'lose:',lose)
print("buy",buy,"sum",Sum(buy))
print("sell",sell,"sum",Sum(sell))
print("利润率",(Sum(sell)-Sum(buy))/(buy[0]*len(buy)))

