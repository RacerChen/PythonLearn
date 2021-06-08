import pandas as pd
import numpy as np
from tqdm import tqdm

from SetUp import *
import warnings
import os

warnings.filterwarnings('ignore')


def main_func(df, volume_multiple, price_tick):
    df['last_ask1'] = df['AskPrice1'].shift(1)
    df['last_bid1'] = df['BidPrice1'].shift(1)

    df['last_ask1'].iloc[0] = df['AskPrice1'].iloc[0]
    df['last_bid1'].iloc[0] = df['BidPrice1'].iloc[0]

    df['high_bite'] = int(0.)
    df['low_bite'] = int(0.)

    df_temp = df[df['LastVolume'] != 0]

    df_temp['avg_price'] = df_temp['LastTurnover'] / volume_multiple / df_temp['LastVolume']

    df_temp['price_high'] = np.ceil(df_temp['avg_price'] / price_tick) * price_tick  # 向上取整
    df_temp['price_low'] = np.floor(df_temp['avg_price'] / price_tick) * price_tick  # 向下取整

    df_temp['pt_multi'] = \
        np.maximum(np.sign(df_temp['avg_price'] - df_temp['last_ask1']), 0) + 1 - np.abs(np.sign(df_temp['avg_price'] - df_temp['last_bid1']))

    df_temp['price_high_after'] = df_temp['price_high']
    df_temp['price_high_after'][df_temp['price_high'] == df_temp['price_low']] = df_temp['avg_price'] + df_temp['pt_multi'] * price_tick
    df_temp['price_low'][df_temp['price_high'] == df_temp['price_low']] = df_temp['price_high_after'] - price_tick
    df_temp['price_high'] = df_temp['price_high_after']

    df_temp['high_bite'] = round((df_temp['LastTurnover'] / volume_multiple - df_temp['LastVolume'] * df_temp['price_low']) / price_tick)
    df_temp['low_bite'] = round((df_temp['LastVolume'] * df_temp['price_high'] - df_temp['LastTurnover'] / volume_multiple) / price_tick)

    df_temp['last_middle'] = (df_temp['last_ask1'] + df_temp['last_bid1']).astype(float) / 2
    df_temp['price_high'] = round(df_temp['price_high'], 3)
    df_temp['price_low'] = round(df_temp['price_low'], 3)
    df_temp['last_middle'] = round(df_temp['last_middle'], 3)

    df_temp['high_bite'][df_temp['price_low'] > df_temp['last_middle']] = df_temp['high_bite'] + df_temp['low_bite']
    df_temp['low_bite'][df_temp['price_low'] > df_temp['last_middle']] = 0
    df_temp['low_bite'][df_temp['price_high'] < df_temp['last_middle']] = df_temp['high_bite'] + df_temp['low_bite']
    df_temp['high_bite'][df_temp['price_high'] < df_temp['last_middle']] = 0

    df_temp['high_bite'] = (df_temp['high_bite']).astype(int)
    df_temp['low_bite'] = (df_temp['low_bite']).astype(int)

    df_ans = pd.concat([df_temp, df[df['LastVolume'] == 0]]).sort_values(by=['UpdateTime', 'UpdateMillisec'])

    return df_ans[['TradingDay', 'InstrumentID', 'UpdateTime', 'UpdateMillisec', 'high_bite', 'low_bite']]


trade_all_day = []
all_day = aqu.get_all_tradingdays()
all_type = ["AP", "CF", "CJ", "CY", "FG", "MA", "OI", "RM", "SM", "SR", "TA", "a",
            "ag", "al", "au", "b", "bu", "c", "cs", "cu", "hc", "j", "jm", "l", "m",
            "ni", "p", "pb", "pg", "pp", "rb", "rr", "ru", "sn", "sp", "ss", "v", "y",
            "zn", "ZC", "eg", "fu", "i", "jd", "sc"]

sym_info = aqu.get_contract_info()

for i in range(len(all_day)):
    if start_date <= all_day[i] <= end_date:
        trade_all_day.append(all_day[i])

for future_type in all_type:
    vm = sym_info[future_type]['multi']
    pt = sym_info[future_type]['tick']

    if os.path.exists('D:/tick_after_processed/' + future_type):
        pass
    else:
        os.makedirs('D:/tick_after_processed/' + future_type)

    for day in tqdm(trade_all_day):
        main_temp = aqu.get_main_symbol(future_type, day)[0]
        if main_temp != '':
            df_processed = main_func(aqu.get_tick_data(main_temp, day), vm, pt)
            df_processed.to_csv('D:/tick_after_processed/'
                                + future_type + '/' +
                                main_temp + '.' + day.strftime('%Y%m%d') + '.csv')
