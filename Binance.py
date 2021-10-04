import requests
import json
import decimal
import hmac
import time
import pandas as pd


binance_keys = {
	'api_key': "z0cTF8RGKwdYLRFlCBwBYCfGWkdTINzkeuht4AD6SggEXiCxh6Xej0j5O93zKXOU",
	'secret_key': "IqRJ5dbirIXrGqk9765LuDFvyS5tjdhFv0unbieyrQdLUgYPuNLh4o7JGRSvrndz"
}

class Binance:
    def __init__(self):
        self.base = 'https://api.binance.com'
        self.endpoints = {
            "order": '/api/v3/order',
            "testOrder": '/api/v3/order/test',
            "allOrders": '/api/v3/allOrders',
            "klines": '/api/v3/klines',
            "exchangeInfo": '/api/v3/exchangeInfo'
        }

    def GetTradingSymbols(self):
        ''' Gets All symbols which are tradable (currently) '''
        url = self.base + self.endpoints["exchangeInfo"]

        try:
            response = requests.get(url)
            data = json.loads(response.text)
        except Exception as e:
            print(" Exception occured when trying to access " + url)
            print(e)
            return []

        symbols_list = []

        for pair in data['symbols']:
            if pair['status'] == 'TRADING':
                symbols_list.append(pair['symbol'])
        return symbols_list

    def GetSymbolData(self, symbol: str, interval: str):
        ''' Gets trading data for one symbol '''

        params = '?&symbol=' + symbol + '&interval=' + interval

        url = self.base + self.endpoints['klines'] + params

        # download data
        data = requests.get(url)
        dictionary = json.loads(data.text)

        # put in dataframe and clean-up
        df = pd.DataFrame.from_dict(dictionary)
        df = df.drop(range(6, 12), axis=1)

        # rename columns
        col_names = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df.columns = col_names

        # transform values from strings to floats
        for col in col_names:
            df[col] = df[col].astype(float)
        df['Base Asset'] = symbol[0:3]
        df['Quote Asset'] = symbol[-3:]
        return df

    def PlaceOrder(self, symbol: str, side: str, type: str, quantity: float, price: float, test: bool = True):

        """
        Symbol: ETHBTC
        ETH - base Asset (what we buy)
        BTC - quote Asset (what we sell for)
        quantity - how much ETH we want
        price - how much BTC we're willing to sell it for
        """
        params = {
            'symbol': symbol,
            'side': side,  # BUY or SELL
            'type': type,  # MARKET, LIMIT, STOP LOSS etc
            'timeInForce': 'GTC',
            'quantity': quantity,
            'price': self.floatToString(price),
            'recvWindow': 5000,
            'timestamp': int(round(time.time() * 1000))
        }
        self.signRequest(params)

    def signRequest(self, params: dict):
        ''' Signs the request to the Binance API '''

        query_string = '&'.join(["{}={}".format(d, params[d]) for d in params])
        print(query_string)
        signature = hmac.new(binance_keys['secret_key'].encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        print(signature)
        params['signature'] = signature.hexdigest()





    # def Main():
    #     model = Binance ()
    #
    #
    # if __name__ == '__main__':
    #     Main()