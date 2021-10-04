import pandas as pd
import requests
import json
import plotly.graph_objs as go
from plotly.offline import plot
from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.bollinger_bands import lower_bollinger_band as lbb
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Binance import Binance
from tabulate import tabulate


import datetime


class TredingModel:
    def __init__(self, symbol):
        exchange = Binance()
        self.symbol = symbol
        self.df = exchange.GetSymbolData(symbol, '4h')
        self.last_price = self.df['Close'][len(self.df['Close']) - 1]
        self.buy_signals = []
        self.buy_signalsB = []
        try:
            self.df['fast_sma'] = sma(self.df['Close'].tolist(), 10)
            self.df['slow_sma'] = sma(self.df['Close'].tolist(), 30)
            self.df['low_boll'] = lbb(self.df['Close'].tolist(), 14)
        except Exception as e:
            print(" Exception raised when trying to compute indicators on " + self.symbol)
            return None
        # while i < len(self.df['close']):
        # print('Close', self.df['Close'].head(), '-slow sma ', self.df['slow_sma'].head())
        for index, name in enumerate(self.df):
            print('Close', self.df['Close'][index], '-slow sma ', self.df['slow_sma'][index])
            self.maStrategy(index)
            self.bollStrategy(index)

    def maStrategy(self, i: int):
        ''' If price is 10% below the Slow MA, return True'''
        df = self.df
        buy_price = 0.8 * df['slow_sma'][i]
        if buy_price >= df['Close'][i]:
            print("ma", self.df['Base Asset'][i], "-",self.df['Quote Asset'][i], 'Close', self.df['Close'][index], '-slow sma ', self.df['slow_sma'][index])
            self.buy_signals.append([df['Time'][i], df['Close'][i], df['Close'][i] * 1.045])
            return True
        return False

    def bollStrategy(self, i: int):
        ''' If price is 5% below the Lower Bollinger Band, return True'''
        buy_price = 0.98 * self.df['low_boll'][i]
        df = self.df
        if buy_price >= df['Close'][i]:
            print("Ball ", self.df['Base Asset'][i], "-",self.df['Quote Asset'][i])
            self.buy_signalsB.append([df['time'][i], df['Close'][i], df['Close'][i] * 1.045])
            return True
        return False

    #     self.df = self.getData()
    #
    # def getData(self):
    #     base = 'https://api.binance.com'
    #     endpoint = '/api/v3/klines'
    #     params = '?symbol=' + self.symbol + '&interval=1h'
    #     url = base + endpoint + params
    #     data = requests.get(url)
    #     dictionary = json.loads(data.text)
    #     df = pd.DataFrame.from_dict(dictionary)
    #     df = df.drop(range(6, 12), axis=1)
    #     col_names = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    #     df.columns = col_names
    #     for col in col_names:
    #         df[col] = df[col].astype(float)
    #
    #     df['Fast_sma'] = sma(df['Close'].tolist(), 10)
    #     df['Slow_sma'] = sma(df['Close'].tolist(), 30)
    #
    #     return df

    # def strategy(self):
    #     df = self.df
    #     buy_signals = []
    #
    #     for i in range(1, len(df['Close'])):
    #         if df['Slow_sma'][i] > df['Low'][i] and (df['Slow_sma'][i] - df['Low'][i]) > 0.03 * df['Low'][i]:
    #             buy_signals.append([df['Time'][i], df['Low'][i]])

        #self.plotData(buy_signals=buy_signals)

    def plotData(self, buy_signals=False):
        df = self.df
        # plot candlestick chart
        candle = go.Candlestick(
            x=df['Time'],
            open=df['Open'],
            close=df['Close'],
            high=df['High'],
            low=df['Low'],
            name="Candlesticks")
        # plot MAs
        fsma = go.Scatter(
            x=df['Time'],
            y=df['fast_sma'],
            name="Fast SMA",
            line=dict(color='rgba(102, 207, 255, 50)'))
        ssma = go.Scatter(
            x=df['Time'],
            y=df['slow_sma'],
            name="Slow SMA",
            line=dict(color='rgba(255, 207, 102, 50)'))

        lowbb = go.Scatter(
            x=df['Time'],
            y=df['low_boll'],
            name="Lower Bollinger Band",
            line=dict(color=('rgba(255, 102, 207, 50)')))


        if len(self.buy_signals)>0:
            buys = go.Scatter(
                x=[item[0] for item in self.buy_signals],
                y=[item[1] for item in self.buy_signals],
                name="Buy Signals",
                mode="markers",
                marker_size=700
            )

            sells = go.Scatter(
                x=[item[0] for item in self.buy_signals],
                y=[item[1] * 1.05 for item in self.buy_signals],
                name="Sell Signals",
                mode="markers",
                marker_size=80
            )
        data = [candle, ssma, fsma, lowbb]
        # data = [candle, ssma, fsma, buys, sells]

        # style and display
        layout = go.Layout(title=self.symbol)
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.symbol)

    def liveChart(self):
        exchange = Binance()
        plt.style.use('fivethiryteight')
        symbols = exchange.GetTradingSymbols()
        for symbol in symbols[0:5]:
            dataValues = exchange.GetSymbolData(symbol, '4h')
            xData = [range(1, len(dataValues))]
            print(symbol)
            print(dataValues)
            print(xData)
            plt.cla()
            plt.plot(dataValues['Time'], dataValues['Close'])

            exchange = Binance()
            plt.style.use('fivethiryteight')
            symbols = exchange.GetTradingSymbols()
            for symbol in symbols[0:5]:
                dataValues = exchange.GetSymbolData(symbol, '1m')

def Main():
    def liveChart(self):
        exchange = Binance()
        symbols = exchange.GetTradingSymbols()
        index = 1
        i = 0

        for symbol in symbols[0:3]:

            datavalues = exchange.GetSymbolData(symbol, '4h')
            datavalues['TimeFormat'] = pd.to_datetime(datavalues['Time'], unit='ms')
            datavalues['fast_sma'] = sma(datavalues['Close'].tolist(), 10)
            datavalues['slow_sma'] = sma(datavalues['Close'].tolist(), 30)
            datavalues['low_boll'] = lbb(datavalues['Close'].tolist(), 14)
            datavalues['1h_before'] = datavalues['TimeFormat'] - datetime.timedelta(hours=1)
            datavalues['30m_ago'] = datavalues['TimeFormat'] - datetime.timedelta(minutes=30)
            datavalues['30s_before'] = datavalues['TimeFormat'] - datetime.timedelta(seconds=30)
            print(symbol)
            print(tabulate(datavalues[0:1]))
            max_price = datavalues['Close'].max()
            min_price = datavalues['Close'].min()
            max_time = datavalues['Time'].max()
            min_time = max_time - 60
            # ax[i].cla()
            # ax[i].plot(datavalues['Time'], datavalues['Close'], color='blue')
            # ax[i].plot(datavalues['Time'], datavalues['fast_sma'], color='green', linestyle=':')
            # ax[i].plot(datavalues['Time'], datavalues['slow_sma'], color='gray', linestyle='--')
            # ax[i].plot(datavalues['Time'], datavalues['low_boll'], color='black', linestyle='')
            # ax[i].legend(['Prices', 'fast_sma', 'slow_sma', 'low_boll'])
            # ax[0].title(symbol)

            # ax[i].set_xticks(datavalues['TimeFormat'])
            # ax[i].set_xticklabels([value.strftime("%H:%M:%S") for value in datavalues['TimeFormat']])
            # ax[i].set_yticks(datavalues['Close'])
            # ax[i].set_yticklabels(datavalues['Close'])





            #plt.axis([min_price -2 , max_price +3 , 0, max_time+1])
            i = + 1
            if index < 4:
                index = +  1
            else:
                index = 1


    # fig, ax = plt.subplots(3)
    ani = FuncAnimation(plt.gcf(), liveChart, interval=15000)
    plt.show()



if __name__ == '__main__':
    Main()
