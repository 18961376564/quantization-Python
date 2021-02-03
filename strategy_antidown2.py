#####
# 低点买入交易策略：买入点 达到前45日低点买入  涨6%卖出或跌3%卖出
# 1 中改进改进： 未来3天有2%上浮的买入
# 2 (本文档)未来3天有2%上浮的买入，再涨2%加一倍仓（看成功率决定是否放大倍数），盈利归零卖出。如没有出现买入点的，视为无效点

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
fair=0
win_point=1.06
add_point=1.024
####
# 关于win、add设置多种组合
# 1、高波动：中信证券、广发证券、美诺华等   1.15  1.06
# 2、中高波动：万科A等   1.10  1.04
# 3、中波动： 1.08  1.03
# 4、低波动：春秋航空、德邦股份等 1.06  1.024

# 列好股票仓（漂亮100、蓝筹股等）。
# step1：自动获取数据并按时间排列
# step2：自动计算1、2、3组合哪种更适合，将结果保存
# step3：自动推荐买点

#不适合加仓操作、适合一锤子买卖的：中国银行、农业银行 等

#####
lose_point=0.98
fair_point=(add_point+1)/2
for i in range(gap,lenth-4):
    if(i>breakgap):
        sell_flag=0
        tmp_low=low[i-gap:i]    ##list[a,b] 含a不含b
        verylow=min(tmp_low)
        # if(low[i-1]>verylow and low[i]<verylow and close[i+1]>close[i]):
        if(low[i-1]>verylow and low[i]<verylow ):
            for k in range(i+1,i+4):     ##一定是i+1  数据测试结果的经验，还未查明原因
                ########### 假低点测试
                if (low[k-1] < verylow * 0.97):   #继续下探，则为假低点
                    break
                ############
                if(high[k]>verylow*1.02):
                    buy_signal=round(verylow*1.02,2)
                    buy.append(buy_signal)
                    buy_date=date[k]
                    print("buy",buy_date,"price",buy_signal)
                    #########
                    #开始分情况：1、止损卖出  2、上涨2%加一仓
                    #  2.1 回撤至保本卖出  2.2 继续上涨6%（4%）卖出
                    #
                    #########
                    while(sell_flag==0):
                        if(k<lenth-3):
                            mode=0
                            for j in range(k+1,lenth-1):
                                if(mode==0 and low[j]<buy[-1]*lose_point):
                                    sell_flag=1
                                    sell.append(round(buy[-1]*lose_point,2))
                                    sell_date = date[j]
                                    print("sell",sell_date,"price",sell[-1])
                                    breakgap = j
                                    lose+=1
                                    break

                                elif(mode==0 and high[j]>buy[-1]*add_point):    #  2.1 回撤至保本卖出  2.2 继续上涨6%（4%）卖出
                                    buy.append(round(buy[-1]*add_point,2))
                                    buy_date = date[j]
                                    print("加仓", buy_date, "price", buy[-1])
                                    mode=1
                                elif(mode==1 and low[j]<buy[-2]*fair_point):
                                    sell_flag=1
                                    sell.append(round(buy[-2]*fair_point,2))
                                    sell.append(round(buy[-2] * fair_point, 2))
                                    sell_date = date[j]
                                    print("平仓双仓",sell_date,"price",sell[-1])
                                    breakgap = j
                                    fair+=1
                                    break
                                elif(mode==1 and high[j]>buy[-2]*win_point):
                                    sell_flag = 1
                                    sell.append(round(buy[-2] * win_point, 2))
                                    sell.append(round(buy[-2] * win_point, 2))
                                    sell_date = date[j]
                                    print("止盈双仓", sell_date, "price",sell[-1])
                                    breakgap = j
                                    win += 1
                                    break

                            if(sell_flag==0):
                                if(mode==0):
                                    breakgap=lenth-1
                                    tmp_hold=buy[-1]
                                    sell.append(tmp_hold)
                                    print("单仓没能卖出",buy[-1])
                                elif(mode==1):
                                    breakgap=lenth-1
                                    tmp_hold=buy[-2]
                                    sell.append(tmp_hold)
                                    tmp_hold=buy[-1]
                                    sell.append(tmp_hold)
                                    print("单仓没能卖出",sell[-2:-1])
                            break
                        else:
                            break
                    break




print('win:',win,'lose:',lose,'fair',fair)
print("buy",buy,"sum",Sum(buy))
print("sell",sell,"sum",Sum(sell))
print("利润率",(Sum(sell)-Sum(buy))/(buy[0]*len(buy)))

