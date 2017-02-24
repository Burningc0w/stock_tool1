import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

import bs4 as bs
import pickle
import requests

def GetStockData(stock):

    today = dt.date.today()
    start = dt.date((today.year - 2), today.month, today.day)
    end = today
    stock = web.DataReader(stock, "yahoo", start, end)

    print(stock.head())

    return stock

def PlotCandleStickGraph(ticker, dataframe, samples):
    # ticker represents the stock ticker
    # dataframe is a panda.dataframe and samples is the number of days to resample

    # make plots look pretty 
    style.use('ggplot')

    # setup sample
    if (samples > 1):
        interval = str(samples) + 'd'

        df_ohlc = dataframe['Adj Close'].resample(interval).ohlc()
        df_volume = dataframe['Volume'].resample(interval).sum()

    elif (samples == 1):
        df_ohlc = dataframe.drop('Volume', 1)
        df_volume = dataframe['Volume']

    else:
        return

    # make "date" a column 
    df_ohlc.reset_index(inplace=True)

    # Convert dates into mdates 
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    # Setup plt
    plt.figure(1)

    ax1 = plt.subplot2grid((7,1), (0,0), rowspan=5, colspan=1 )
    ax1.xaxis_date()
    plt.title(ticker)
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

    ax2 = plt.subplot2grid((7,1), (6,0), rowspan=1, colspan=1, sharex = ax1)
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

    plt.show()

    return 

def save_sp500_ticker():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class':'wikitable sortable'})

    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('sp500tickerlist.pickle', 'wb') as f:
        pickle.dump(tickers,f)

    return

ticker = "AMD"

# stock = GetStockData(ticker)

# PlotCandleStickGraph(ticker, stock, 4)

save_sp500_ticker()