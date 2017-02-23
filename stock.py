import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

def GetStockData(stock):

    today = dt.date.today()
    start = dt.date((today.year - 2), today.month, today.day)
    end = today
    stock = web.DataReader(stock, "yahoo", start, end)

    print(stock.head())

    return stock

def PlotCandleStickGraph(stock, samples):
    # Stock is a panda.dataframe and samples is the number of days to resample
    # make plots look pretty 
    style.use('ggplot')

    if (samples > 1):
        interval = str(samples) + 'd'

        df_ohlc = stock['Adj Close'].resample(interval).ohlc()
        df_volume = stock['Volume'].resample(interval).sum()

    elif (samples == 1):
        df_ohlc = stock.drop('Volume', 1)
        df_volume = stock['Volume']

    else:
        return

    # make "date" a column 
    df_ohlc.reset_index(inplace=True)

    # Convert dates into mdates 
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    # Setup plt
    ax1 = plt.subplot2grid((7,1), (0,0), rowspan=5, colspan=1 )
    ax1.xaxis_date()
    ax2 = plt.subplot2grid((7,1), (6,0), rowspan=1, colspan=1, sharex = ax1)

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

    plt.show()

    return 

stock = GetStockData("AAPL")

PlotCandleStickGraph(stock, 1)