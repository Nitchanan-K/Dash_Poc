import pprint
import openpyxl



a = {'data': [{'displayTV': 1,
           'first_historical_data': '2013-04-28T18:47:21.000Z',
           'id': 1,
           'is_active': 1,
           'last_historical_data': '2022-12-22T04:19:00.000Z', 
           'name': 'Bitcoin',
           'platform': None,
           'rank': 1,
           'slug': 'bitcoin',
           'symbol': 'BTC'},
          {'displayTV': 1,
           'first_historical_data': '2013-04-28T18:47:22.000Z',
           'id': 2,
           'is_active': 1,
           'last_historical_data': '2022-12-22T04:19:00.000Z', 
           'name': 'Litecoin',
           'platform': None,
           'rank': 14,
           'slug': 'litecoin',
           'symbol': 'LTC'}],
 'status': {'credit_count': 1,
            'elapsed': 18,
            'error_code': 0,
            'error_message': None,
            'notice': None,
            'timestamp': '2022-12-22T04:26:33.758Z'}}


def print_symbol(data):

    lst = []

    for i in data['data']:
        print(i['symbol'])

        lst.append(i['symbol']+'-USD')
    
    return lst

b = print_symbol(a)

print(b) 


# Create a new workbook and add a worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active


# Define the string you want to save


