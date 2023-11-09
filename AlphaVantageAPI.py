import requests
import pandas as pd
import csv
import json

class AVFinance:
    
    symbols = []
    apikey = ''
    url = 'https://www.alphavantage.co/query?'

    def __init__(self, symbols, apikey):
        self.symbols = symbols
        self.apikey = apikey

    @staticmethod    
    def generate_id(columns):
        return abs(hash(columns)) % (10 ** 10)
    
    def get_timeseries(self, timespan='daily', adjusted=0, intraday_interval='60min'):
        
        data = []
        functions = {}

        if timespan == 'intraday' or adjusted == 0:
            functions = {
                'intraday':'TIME_SERIES_INTRADAY',
                'daily':'TIME_SERIES_DAILY',
                'weekly':'TIME_SERIES_WEEKLY',
                'monthly':'TIME_SERIES_MONTHLY' 
            }
        else:
            functions = {
                'daily':'TIME_SERIES_DAILY_ADJUSTED',
                'weekly':'TIME_SERIES_WEEKLY_ADJUSTED',
                'monthly':'TIME_SERIES_MONTHLY_ADJUSTED' 
            }

        for item in self.symbols:
            parameters = {
                'function' : functions[timespan],
                'symbol' : item,
                'interval' : intraday_interval,
                'apikey' : self.apikey,
                'datatype' : 'csv'            
            }
            response = requests.get(self.url, params=parameters).content.decode('utf-8')   
            iterator = list(csv.reader(response.splitlines(), delimiter=','))

            for row in iterator[1:]:
                row = [item] + row
                data.append(row)
        
        headers = ['symbol'] + iterator[0]
        return pd.DataFrame(data, columns=headers)
    
    def get_lastquote(self):
        
        data = []
        for stock in self.symbols:
            parameters = {
                'function' : 'GLOBAL_QUOTE',
                'symbol' : stock,
                'apikey' : self.apikey,
                'datatype' : 'csv'            
            }
            response = requests.get(self.url, params=parameters).content.decode('utf-8')
            iterator = list(csv.reader(response.splitlines(), delimiter=','))

            for row in iterator[1:]:
                data.append(row)

        headers = iterator[0]
        return pd.DataFrame(data, columns=headers)
         
    def get_marketsentiment(self, sort='relevance', limit=50):
        data = []
        for stock in self.symbols:
            parameters = {
                'function' : 'NEWS_SENTIMENT',
                'tickers' : stock,
                'apikey' : self.apikey,
                'sort' : sort,
                'limit' : limit             
            }
            response = requests.get(self.url, params=parameters).content.decode('utf-8')
            jsondata = json.loads(response)['feed']

            rootdf = pd.json_normalize(jsondata, max_level=0).drop(['authors', 'topics', 'ticker_sentiment'], axis=1) 
            rootdf['uniqueid'] = rootdf[['title','source','time_published']].agg(''.join, axis=1).apply(self.generate_id)
            rootdf.drop_duplicates(keep='first', subset=['uniqueid'], inplace=True)
            rootdf.set_index(
                keys='uniqueid',
                append=False, 
                verify_integrity=True,
                inplace=True
            )

            tickerdf = pd.json_normalize(
                jsondata, 
                record_path='ticker_sentiment', 
                meta=['title', 'source', 'time_published']
            ).query('ticker == "GOOG"')

            tickerdf['uniqueid'] = tickerdf[['title','source','time_published']].agg(''.join, axis=1).apply(self.generate_id)
            tickerdf.drop_duplicates(keep='first', subset=['uniqueid'], inplace=True)
            tickerdf.set_index(
                keys='uniqueid',
                verify_integrity=True,
                append=False,
                inplace=True
            )
            tickerdf.drop(['title','source','time_published'], axis=1, inplace=True)

            dflist = [rootdf, tickerdf]
            outputdf = pd.concat(dflist, axis=1)
            iterator = outputdf.values.tolist()
            
            for row in iterator[1:]:
                data.append(row)
        
        headers = iterator[0]
        return pd.DataFrame(data, columns=headers)
    
fetcher = AVFinance(['goog', 'ibm'], '')
data = fetcher.get_marketsentiment()



