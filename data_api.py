# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import time
import os
import datetime
import json

data_path = 'Y:/'
# 记录临时
all_trading_days = []
future_contract_info = None
future_instruments = None

# 各种路径
tradingday_path = 'warehouse/rawdata/china/universe/tradingdays.csv'
future_d1_path = 'warehouse/data/china/futures/d1/'
future_m1_path = 'warehouse/rawdata/china/futures/m1/'
stock_none_day_path = 'warehouse/rawdata/china/stock/none/day/'
stock_none_m1_path = 'warehouse/rawdata/china/stock/none/m1/'
stock_post_day_path = 'warehouse/rawdata/china/stock/post/day/'
stock_post_m1_path = 'warehouse/rawdata/china/stock/post/m1/'
stock_money_flow_path = 'warehouse/rawdata/china/stock/money_flow/'
stock_valuation_path = 'warehouse/rawdata/china/stock/valuation/'
stock_index_path = 'warehouse/rawdata/china/stock/index/'
future_contract_info_path = 'warehouse/rawdata/china/futures/universe/ContractInfo.txt'
future_trading_session_path = 'warehouse/rawdata/china/futures/universe/trading_session.json'
future_instruments_path = 'warehouse/rawdata/china/futures/universe/ctp_instruments.csv'
future_tick_path = 'warehouse/rawdata/china/futures/tick/'

# 获取所有的交易日


def get_all_tradingdays():
    global all_trading_days
    dates = all_trading_days
    if(len(dates) == 0):
        td_path = data_path+tradingday_path
        file = open(td_path)
        lines = file.readlines()
        file.close()
        for i in range(len(lines)-1):
            cols = lines[i+1].split('\n')[0].split(',')
            if(len(cols) == 2):
                dates.append(datetime.datetime.strptime(
                    cols[1], '%Y-%m-%d').date())
        all_trading_days = dates
    return dates

# shift=0时，如果传入参数是交易日，那就返回该日期。若不是，返回此日期之后的第一个交易日


def get_tradingday_after(tradingday, shift):
    dates = get_all_tradingdays()
    for i in range(len(dates)):
        if(dates[i] >= tradingday):
            break
    return dates[i+shift]

# 获取某个时间点的交易日


def get_tradingday(t):
    # 周六的话，返回周一
    date = t.date()
    if(t.weekday() == 5):
        date = t.date() + datetime.timedelta(days=2)
    elif(t.hour < 19):  # 上午的话返回当天
        date = t.date()
    elif(t.weekday() == 4):  # 周五晚上的话返回周一
        date = t.date() + datetime.timedelta(days=3)
    else:
        date = t.date() + datetime.timedelta(days=1)
    # 看是否是节假日，如果是的话向后顺延一天
    date = get_tradingday_after(date, 0)
    return date

# 解析某天的tick数据


def parse_tick_data(buffer, tradingday, symbol_names):
    lines = buffer.split('\n')
    data_to_append = []
    for i in range(len(lines)-1):  # 最后一行写进buffer
        line = lines[i]
        cols = line.split(',')
        if(len(cols) != 31):
            continue
        if not cols[1] in symbol_names:
            continue
        # 这里要算出准确的日期
        t = datetime.datetime.strptime(tradingday.strftime(
            '%Y-%m-%d') + ' ' + cols[2], '%Y-%m-%d %H:%M:%S')
        if(t.hour > 19):  # 如果是晚上，那看tradingday是不是周一，周一的话准确日期就是周五，否则就是前一天
            if(t.weekday() == 0):
                t = t + datetime.timedelta(days=-3)
            else:
                t = t + datetime.timedelta(days=-1)
        elif(t.hour < 6 and t.weekday() == 0):  # 如果是凌晨，那要看tradingday是不是周一，周一的话准确日期应该是周六
            t = t + datetime.timedelta(days=-2)
        '''
        a = {"updatetime":t.strftime("%Y-%m-%d %H:%M:%S"),"updatemillisec":cols[3],
                                           "lastPrice":cols[4],"volume":cols[5],
                                           "bidPrice":cols[6],"askPrice":cols[8]}
        '''
        dirty = False
        if((t.hour == 15 and t.minute > 15) or (t.hour == 8 and t.minute < 30) or (t.hour == 20 and t.minute < 30) or (t.hour >= 16 and t.hour < 20) or (t.hour >= 3 and t.hour < 8)):
            dirty = True
        if(dirty == False):
            a = [t.strftime("%Y-%m-%d %H:%M:%S"), cols[3],
                 cols[4], cols[5], cols[6], cols[8], cols[7], cols[9]]
            data_to_append.append(a)
    buffer = lines[-1]
    return buffer, data_to_append

# 获取历史tick数组


def get_history_ticks(tradingday, symbol_names):
    buffer = ''
    tick_path = data_path+future_tick_path+'/all/'
    # 如果今天是周一，要先读周六的数据，再读今天的数据
    if(tradingday.weekday() == 0 and os.path.exists(tick_path+"tick."+(tradingday+datetime.timedelta(days=-2)).strftime('%Y%m%d')+".txt")):
        tick_file = open(tick_path+"tick." +
                         (tradingday+datetime.timedelta(days=-2)).strftime('%Y%m%d')+".txt")
        buffer += tick_file.read()
        tick_file.close()
    tick_file = open(tick_path+"tick." +
                     tradingday.strftime('%Y%m%d')+".txt")
    buffer += tick_file.read()
    tick_file.close()
    buffer, data = parse_tick_data(buffer, tradingday, symbol_names)
    return data

# 获取当天tick数组


def get_today_ticks(tradingday, symbol_names):
    buffer = ''
    tick_path = data_path+future_tick_path+'/all/'
    # 如果今天是周一，要先读周六的数据，再读今天的数据
    if(tradingday.weekday() == 0 and os.path.exists(tick_path+"tick."+(tradingday+datetime.timedelta(days=-2)).strftime('%Y%m%d')+".txt")):
        tick_file = open(tick_path+"tick." +
                         (tradingday+datetime.timedelta(days=-2)).strftime('%Y%m%d')+".txt")
        buffer += tick_file.read()
        tick_file.close()
    tick_file = open(tick_path+"tick." +
                     tradingday.strftime('%Y%m%d')+".txt")
    buffer += tick_file.read()
    buffer, data = parse_tick_data(buffer, tradingday, symbol_names)
    return buffer, data, tick_file

# 找某一天的主力合约


def get_main_symbol(symbol, origintradingday):
    main = ''
    second = ''
    third = ''

    d1_path = data_path + future_d1_path + symbol
    dir_list = os.listdir(d1_path)
    last_oi = 0
    second_oi = 0
    third_oi = 0
    tradingday = get_tradingday_after(origintradingday, -1)    
    instruments = get_instrument_info()
    for cur_file in dir_list:
        file_path = d1_path+'/'+cur_file
        s = cur_file.split('.')[0]
        if s not in instruments.index.values:
            continue
        if(instruments.loc[s]['expireDate'] <= datetime.date.strftime(origintradingday, '%Y-%m-%d')):
            continue
        if(instruments.loc[s]['openDate'] > datetime.date.strftime(origintradingday, '%Y-%m-%d')):
            continue
        file = open(file_path)
        d1s = file.readlines()
        file.close()
        for i in range(len(d1s)):
            last_day_data = d1s[-i-1]
            last_day = datetime.datetime.strptime(
                last_day_data.split(' ')[0], '%Y-%m-%d').date()
            if(last_day == tradingday):
                break
        if(last_day == tradingday):
            oi = float(last_day_data.split(',')[5].strip('\n'))
            if(oi >= last_oi):
                third = second
                third_oi = second_oi
                second = main
                second_oi = last_oi
                last_oi = oi
                main = s
            elif oi >= second_oi:
                third = second
                third_oi = second_oi
                second_oi = oi
                second = s
            elif oi >= third_oi:
                third = s
                third_oi = oi
    # 如果第一天的明天就要交割了，那么将次主力和次次主力顺位上移
    '''
    if instruments.loc[main]['expireDate'] <= datetime.date.strftime(origintradingday, '%Y-%m-%d'):
        main = second
        second = third
    elif instruments.loc[second]['expireDate'] <= datetime.date.strftime(origintradingday, '%Y-%m-%d'):
        
        second = third
    '''
    return main, second,third


def get_main_symbol_series(symbol, start_date, end_date):
    global all_trading_days

    instruments = get_instrument_info()
    ser = []
    oi_dict = dict()
    main_dict = dict()
    second_oi_dict = dict()
    second_dict = dict()
    third_oi_dict = dict()
    third_dict = dict()
    get_all_tradingdays()
    for day in all_trading_days:
        if day < start_date:
            continue
        if day > end_date:
            break
        oi_dict[day] = 0
        second_oi_dict[day] = 0
        third_oi_dict[day] = 0
        main_dict[day] = ''
        second_dict[day] = ''
        third_dict[day] = ''
    d1_path = data_path+future_d1_path+symbol
    dir_list = os.listdir(d1_path)
    for cur_file in dir_list:
        file_path = d1_path+'/'+cur_file
        symbol = cur_file.split('.')[0]
        if symbol not in instruments.index:
            continue
        if(instruments.loc[symbol]['expireDate'] <= datetime.date.strftime(start_date, '%Y-%m-%d')):
            continue
        if(instruments.loc[symbol]['openDate'] > datetime.date.strftime(end_date, '%Y-%m-%d')):
            continue
        file = open(file_path)
        d1s = file.readlines()
        file.close()
        for i in range(len(d1s)):
            data = d1s[i]
            day = datetime.datetime.strptime(
                data.split(' ')[0], '%Y-%m-%d').date()
            nextday = get_tradingday_after(day, 1)
            if instruments.loc[cur_file.split('.')[0]]['expireDate'] <= \
                    datetime.date.strftime(nextday, '%Y-%m-%d'):
                continue
            oi = float(data.split(',')[5].strip('\n'))
            if not nextday in oi_dict:
                continue
            if(oi >= oi_dict[nextday]):
                third_dict[nextday] = second_dict[nextday]
                third_oi_dict[nextday] = second_oi_dict[nextday]
                second_dict[nextday] = main_dict[nextday]
                second_oi_dict[nextday] = oi_dict[nextday]
                oi_dict[nextday] = oi
                main_dict[nextday] = cur_file.split('.')[0]
            elif(oi >= second_oi_dict[nextday]):
                third_dict[nextday] = second_dict[nextday]
                third_oi_dict[nextday] = second_oi_dict[nextday]
                second_dict[nextday] = cur_file.split('.')[0]
                second_oi_dict[nextday] = oi
            elif(oi >= third_oi_dict[nextday]):                
                third_dict[nextday] = cur_file.split('.')[0]
                third_oi_dict[nextday] = oi
    for day in main_dict:
        ser.append([day, main_dict[day],second_dict[day],third_dict[day]])
    
    last = ''
    cur = ''
    for day in ser:
        if(day[1] != cur):
            if(day[1] == last):
                day[1] = cur
                if day[2] == day[1]:
                    day[2] = day[3]
            else:
                last = cur
                cur = day[1]   
                if day[2] == last:
                    day[2] = day[3]
        if day[2] == last:
            day[2] = day[3]
    
    ser = pd.DataFrame(ser)
    ser.columns = ['date', 'main','next','third']
    ser = ser.set_index('date')
    return ser


# 获取某个合约的d1数据


def get_d1_data(symbol):
    d1_path = data_path+future_d1_path + \
        symbol.strip('1234567890')+'/'+symbol+'.d1.txt'
    file = open(d1_path)
    d1s = file.readlines()
    file.close()
    data = []
    for i in range(len(d1s)):
        if(len(d1s[1].split(',')) > 1):
            cols = d1s[i].split('\n')[0].split(',')
            data.append([cols[0], float(cols[1]), float(cols[2]), float(cols[3]),
                         float(cols[4]), float(cols[5]), float(cols[6])])
    return data

# 获取股票的不复权的d1数据


def get_stock_day_none_data(symbol):
    d1_path = data_path + stock_none_day_path +\
        symbol + '.txt'
    data = pd.read_csv(d1_path)
    data.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'money', 'avg',
                    'high_limit', 'low_limit', 'pre_close', 'paused', 'factor']
    return data

def get_stock_m1_none_data(symbol , date):
    m1_path = data_path + stock_none_m1_path +\
        symbol + '/' + date.strftime('%Y-%m-%d') + '.txt'
    data = pd.read_csv(m1_path)
    data.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'money', 'avg']
    data['time'] = data['time'].apply(lambda x:(datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(minutes=-1)).strftime('%Y-%m-%d %H:%M:%S'))
    return data
    
def get_stock_day_post_data(symbol):
    d1_path = data_path + stock_post_day_path +\
        symbol + '.txt'
    data = pd.read_csv(d1_path)
    data.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'money', 'avg',
                    'high_limit', 'low_limit', 'pre_close', 'paused', 'factor']
    return data

def get_stock_m1_post_data(symbol , date):
    m1_path = data_path + stock_post_m1_path +\
        symbol + '/' + date.strftime('%Y-%m-%d') + '.txt'
    data = pd.read_csv(m1_path)
    data.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'money', 'avg']
    data['time'] = data['time'].apply(lambda x:(datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(minutes=-1)).strftime('%Y-%m-%d %H:%M:%S'))
    return data

# 获取单支股票的资金流序列


def get_stock_money_flow(code):
    money_flow_path = data_path + stock_money_flow_path +\
        code+'.txt'
    return pd.read_csv(money_flow_path)


# 获取单支股票的市值表序列


def get_stock_valuation(code):
    valuation_path = data_path + stock_valuation_path +\
        code+'.txt'
    return pd.read_csv(valuation_path)

# 获取某一天的股指成分股


def get_index_stocks(index, date):
    index_path = data_path + stock_index_path+index
    files = os.listdir(index_path)
    files.sort()
    index = 0
    for idx, f in enumerate(files):
        if date >= datetime.datetime.strptime(f.strip('.txt'),'%Y-%m-%d').date():
            index = idx
    print(files[index])
    data = pd.read_csv(index_path+'/'+files[index])
    return data


# 获取某个合约某天的m1数据


def get_m1_data(symbol, tradingday):
    # 如果今天是周一，要先读周六的数据，再读今天的数据
    m1_path = data_path + future_m1_path + \
        symbol.strip('0123456789')+'/'
    last_two_day = (tradingday+datetime.timedelta(days=-2)).strftime('%Y%m%d')
    td = (tradingday).strftime('%Y%m%d')
    buffer = ''
    if(tradingday.weekday() == 0 and os.path.exists(m1_path+last_two_day +
                                                    '/'+symbol+'.'+last_two_day+".txt")):
        file = open(m1_path+last_two_day +
                    '/'+symbol+'.'+last_two_day+".txt")
        buffer += file.read()
        file.close()
    file = open(m1_path+td+'/'+symbol+'.'+td+".txt")
    buffer += file.read()
    buffer = buffer.split('\n')
    file.close()
    data = []
    for i in range(len(buffer)):
        if(len(buffer[i].split(',')) > 5):
            cols = buffer[i].split('\n')[0].split(',')
            data.append([cols[0], float(cols[1]), float(cols[2]), float(cols[3]),
                         float(cols[4]), float(cols[5]), float(cols[6])])
    return data

# 获取品种的信息


def get_contract_info():
    global future_contract_info
    if future_contract_info is None:
        contract_path = data_path+future_contract_info_path
        session_path = data_path+future_trading_session_path
        file = open(session_path)
        session = file.read()
        file.close()
        session = json.loads(session)
        file = open(contract_path, encoding='utf-8')
        lines = file.readlines()
        infos = dict()
        for line in lines:
            strs = line.strip('\n').split(',')
            if len(strs) > 7:
                infos[strs[0]] = {"exchange": strs[1], 'multi': int(strs[3]), 'tick': float(strs[4]),
                                  'lock': int(strs[5]), 'session': session[strs[7]]}
        future_contract_info = infos
    return future_contract_info

# 获取合约的详细信息


def get_instrument_info():
    global future_instruments
    if future_instruments is None:
        instrument_path = data_path+future_instruments_path
        df = pd.read_csv(instrument_path, index_col=0)
        future_instruments = df
    return future_instruments
