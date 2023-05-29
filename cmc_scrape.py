from requests import Session
from datetime import date
import pandas as pd
import json
import cmcapikey # to get API key from another file

def make_request(start, limit):
  """Makes the API Call."""
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'start':f'{start}',
    'limit':f'{limit}',
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': cmcapikey.KEY,
  }
  session = Session()
  session.headers.update(headers)
  response = session.get(url, params=parameters)
  response.raise_for_status()
  return json.loads(response.text)

def make_dict(data):
  """Parsing the Data."""
  return {
      "Name" : [coin['name'] for coin in data['data']],
      "Symbol" : [coin['symbol'] for coin in data['data']],
      "Market Cap (in $)" : [coin['quote']['USD']['market_cap'] for coin in data['data']],
      "Age (in years)" : [date.today().year - int(coin['date_added'].split("-")[0]) for coin in data['data']],
      "Hourly Price Change" : [coin['quote']['USD']['percent_change_1h'] for coin in data['data']],
      "Daily Price Change" : [coin['quote']['USD']['percent_change_24h'] for coin in data['data']],
      "Weekly Price Change" : [coin['quote']['USD']['percent_change_7d'] for coin in data['data']],
      "Monthly Price Change" : [coin['quote']['USD']['percent_change_30d'] for coin in data['data']],
      "Quaterly Price Change" : [coin['quote']['USD']['percent_change_90d'] for coin in data['data']],
      "Daily Volume" : [coin['quote']['USD']['volume_24h'] for coin in data['data']],
      "Circulating Supply" : [coin['circulating_supply'] for coin in data['data']],
      "Markets" : [', '.join(coin['tags']) for coin in data['data']]
  }

def main():
  """Making two API calls for getting all 9K+ records (as the limit is 5K at once)"""
  start = 1
  limit = 5000
  dfs = []

  for _ in range(2):
    data = make_request(start, limit)
    dfs.append(make_dict(data))
    start = limit + 1
  
  df1 = pd.DataFrame(dfs[0])
  df2 = pd.DataFrame(dfs[1])

  return pd.concat([df1, df2], axis=0)
  
if __name__ == '__main__':
  df = main()
  df.to_csv('CMC_Index.csv', index=False)
  print('All Done')