import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import fxcmpy as fx
import datetime as dt
import socketio
import statistics as stats
from IPython.display import display
from scipy.signal import argrelextrema
#---------------------------------Connections------------------------------

#------------------Mathematical Functions ----------------------------------
def discreteDerivative(array):
    derArray = []
    for i in range(len(array) - 1):
        derArray.appned(array[i] - array[i + 1])
    return derArray


#------------------Indicators-----------------------------------------------
def simple_moving_average(vals = [], diam = 1):
    width = len(vals)
    print(width)
    if width == 0:
        print("Your values are empty or you didn't supply any")
    elif width < diam:
        print("Your diameter is too large")
    else:
        sma = [vals[0]]
        for i in range(1,width):
            if i <= diam:
                new_point = stats.mean(vals[0:i])
            else:
                new_point = stats.mean(vals[i-diam:i])
            sma.append(new_point)
    return sma

def exponential_moving_average(vals = [], span = 1):
    if len(vals) == 0:
        return "You didn't provide any values"
    num_series = pd.Series(vals)
    moving_averages = round(num_series.ewm(span).mean(), 5)
    return moving_averages.tolist()

def exp_ribbon(vals = [], length_list = []):
    if len(vals) == 0:
        return "You didn't provide any values"
    if len(length_list) == 0:
        return "You didn't provide any lengths for the moving averages"
    MA_list = []
    for n in length_list:
        MA_list.append(exponential_moving_average(vals,n))
        
    return MA_list

def sim_ribbon(vals = [], length_list = []):
    if len(vals) == 0:
        return "You didn't provide any values"
    if len(length_list) == 0:
        return "You didn't provide any lengths for the moving averages"
    MA_list = []
    for n in length_list:
        MA_list.append(simple_moving_average(vals,n))
    return MA_list

def gen_MACD(vals, a = 26, b = 12):
    return [exponential_moving_average(vals, a)[i] - exponential_moving_average(vals, b)[i] for i in range(len(vals))]

def signal_line(vals):
    return exponential_moving_average(gen_MACD(vals), 9)

def RS(opens, closes):
    ups_list = [closes[i] - opens[i] for i in range(len(opens)) if closes[i] - opens[i] > 0]
    downs_list = [closes[i] - opens[i] for i in range(len(opens)) if closes[i] - opens[i] <= 0]
    return stats.mean(ups_list)/stats.mean(downs_list)

def RSI(opens, closes):
    
    return 100 - 100/(1 + RS(opens,closes))

def createTrendDataFrame(df):
    '''Finds the local extrema of the data and creates a trend column of the alternating composition of the minima and maxima columns.
    Assumes the trend is built from the close column heading.
    '''
    n = 1
    df['min'] = df.iloc[argrelextrema(df.Close.values, np.less_equal, order=n)[0]]['Close']
    df['max'] = df.iloc[argrelextrema(df.Close.values, np.greater_equal, order=n)[0]]['Close']
    min_list = df['min'].values.tolist()
    max_list = df['max'].values.tolist()
    trend_dict = {}
    for i in range(len(min_list)):
        if pd.Series(min_list[i]).notna().values.tolist()[0] == True:
            trend_dict[i] = min_list[i]
        elif pd.Series(max_list[i]).notna().values.tolist()[0] == True:
            trend_dict[i] = max_list[i]
            
    trend_df = pd.DataFrame(data = [trend_dict[key] for key in trend_dict.keys()], index = trend_dict.keys(), columns = ['trend'])

    return trend_df

def isTrend(trend_df):
    '''
    isTrend(trend_df)

    
    Given your data as a Pandas trend dataframe, it finds the largest trend and returns +1 if positive trending, -1 if negative trending and 0 if no trend is found
    '''
    L = len(trend_df)
    bull = True
    bear = True
    if bull:
        swing_low = min(trend_df.iloc[0].values[0],trend_df.iloc[1].values[0])
        swing_high = max(trend_df.iloc[0].values[0],trend_df.iloc[1].values[0])
        for i in range(2, L):
            current = trend_df.iloc[i].values[0]
            if current <= swing_high and current >= swing_low:
                swing_low = current
            elif current >= swing_high:
                swing_high = current
            else:
                bull = False
    if bear:
        swing_low = min(trend_df.iloc[0].values[0],trend_df.iloc[1].values[0])
        swing_high = max(trend_df.iloc[0].values[0],trend_df.iloc[1].values[0])
        for i in range(2, L):
            current = trend_df.iloc[i].values[0]
            if current <= swing_high and current >= swing_low:
                swing_high = current
            elif current <= swing_low:
                swing_low = current
            else:
                bear = False
    if bull:
        return 1
    elif bear:
        return -1
    else:
        return 0

def getRecentTrend(trend_df, n):
    '''Given your data as a Pandas trend dataframe and some interval length, it finds the largest trend that it can identify in the most recent n data points.
    The trend that it finds could be truncated by the n that you give, in which case, it returns a pm 2 to indicate the trend is longer.
    The sign of the value it returns indicates the direction that the trend works in. Positive is uptrending, negative is downtrending.
    The data you give must at least contain 3 rows and, similarly, n must be at least 3. 
    '''
    bear = False
    bull = False
    plat = False
    L = len(trend_df)
    for k in range(3, n):
        iden = isTrend(trend_df.iloc[L - k:])
        if iden == 1:
            bull = True
            bear = False
        elif iden == -1:
            bear = True
            bull = False
        else:
            plat = True
            if bull:
                return [1, k-1]
            elif bear:
                return [-1, k-1]
            else:
                return 'You messed up'
            
    if bull:
            return [2, k-1]
    elif bear:
            return [-2, k-1]
    else:
            return 'You messed up'


def trendAnalysis(df, n):
    '''Returns the strength of the largest, most recent trend in fewer than n data points.
    The parameters are (pandas dataframe as data, n).
    It returns [sign of your trend, size of trend, the trend strength]'''
    trend_df = createTrendDataFrame(df, n)
    ret = getRecentTrend(trend_df,n)
    if type(ret) == list:
        [iden, width] = ret
        sign = int(iden/abs(iden))
        return [sign, width, sign*float(round(trend_df.iloc[-1] - trend_df.iloc[-width - 1], 6))]
    elif type(ret) == str:
        return 'Youve messed up at getting the trend'
    else:
        return 'Youve really messed up'
    


