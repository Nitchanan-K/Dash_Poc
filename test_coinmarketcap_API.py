from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import xlsxwriter


def print_symbol(data):
    for i in data['data']:
        print(i['symbol'])
      


def get_test():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

    parameters = {
    'start':'1',
    'limit':'5000',
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'e42bce31-6572-47c5-8579-86745e8390cc',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)


        #data = (json.loads(response.text)['data'],['1'],['symbol'])
        print_symbol(json.loads(response.text))




    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
   

# e42bce31-6572-47c5-8579-86745e8390cc


get_test()