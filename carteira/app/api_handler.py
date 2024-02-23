from .models import *
import requests
import datetime

endpoint = 'https://query1.finance.yahoo.com/v8/finance/chart/'

# Some headers to make the request work
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'A1=d=AQABBKvW12UCEGdVLONEo8IrKYEuq4uT2hkFEgEBAQEo2WXhZR6exyMA_eMAAA&S=AQAAAq7CPuax_T6AxzQFNwQ9gqM; A3=d=AQABBKvW12UCEGdVLONEo8IrKYEuq4uT2hkFEgEBAQEo2WXhZR6exyMA_eMAAA&S=AQAAAq7CPuax_T6AxzQFNwQ9gqM; A1S=d=AQABBKvW12UCEGdVLONEo8IrKYEuq4uT2hkFEgEBAQEo2WXhZR6exyMA_eMAAA&S=AQAAAq7CPuax_T6AxzQFNwQ9gqM; cmp=t=1708644246&j=0&u=1---; gpp=DBAA; gpp_sid=-1; PRF=t%3DPETR4.SA%26newChartbetateaser%3D0%252C1709853846889',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

def is_ticker_valid(ticker):
    url = endpoint + ticker + '.SA'
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['chart']['error'] is not None:
        return False
    return True

def retrieve_cache(ticker, date, allow_older=False):
    cache = TickerCache.objects.filter(ticker=ticker, date=date)
    if cache.exists():
        return cache[0].price
    elif allow_older:
        cache = TickerCache.objects.filter(ticker=ticker, date__lt=date).order_by('-date')
        if cache.exists():
            return cache[0].price
    return None

def get_current_price(ticker):
    # Check if result is in cache
    
    # Or fetch it
    url = endpoint + ticker + '.SA'
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['chart']['error'] is not None:
        return None
    try:
        return data['chart']['result'][0]['meta']['regularMarketPrice']
    except:
        return None

def get_historical_data(ticker, date):
    # Check if result is in cache
    print('------')
    res = retrieve_cache(ticker, date)
    print("trying cached data for " + ticker + " on ", date, '=', res)
    if res is not None:
        return res

    # Otherwise fetch it and try again
    print('cache miss')
    print("Fetching historical data for " + ticker)
    fetch_historical_data(ticker)
    res = retrieve_cache(ticker, date, allow_older=True)
    print("trying again " + ticker + " on ", date, '=', res)
    if res is not None:
        return res

    print('UNABLE')
    return None

def fetch_historical_data(ticker):
    url = endpoint + ticker + '.SA?metrics=high?&interval=1d&range=3mo'
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['chart']['error'] is not None:
        return None
    
    timestamps = data['chart']['result'][0]['timestamp']
    timestamps = [datetime.datetime.fromtimestamp(timestamp) for timestamp in timestamps]
    indicators = data['chart']['result'][0]['indicators']['quote'][0]['close']
    
    for i in range(len(indicators)-1):
        if not TickerCache.objects.filter(ticker=ticker, date=timestamps[i]).exists():
            TickerCache.objects.create(ticker=ticker, date=timestamps[i], price=indicators[i])
