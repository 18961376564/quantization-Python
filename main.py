# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import tushare as ts
import pandas as pd

ts.set_token('8031035535f8e89792cfc111867fefe422380dade4f134e736f7df1d')
pro = ts.pro_api()
df = pro.daily(ts_code='603538.SH', start_date='20181228', end_date='20210119')
df.to_excel('美诺华.xlsx',startrow=0,startcol=0)


#df=ts.pro_bar(ts_code='600030.SH',adj='qfq', start_date='20210103', end_date='20210110')

# stock='600030.SH'
# start_date='20210103'
# end_date='20210110'
# def acquire_data(stock, start_date, end_date):
#     df = ts.pro_bar(stock,'qfq', start_date, end_date)
#     dates = pd.to_datetime(df["trade_date"])
#     #df = pd.to_execl("zhong.xlsx")
#     df =df[['open','high','low','close','volume']]
#     df.index = dates
#     df.sort_index(ascending=True, implace=True)
#
# df= acquire_data(stock, start_date, end_date)