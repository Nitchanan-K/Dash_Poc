from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import xlsxwriter
import openpyxl
import csv

# api key 
# e42bce31-6572-47c5-8579-86745e8390cc
      
# FUNCTION (GET DATA FROM API)
def get_data():

    # SETUP
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

    # GET DATA 
    try:
        response = session.get(url, params=parameters)


        #data = (json.loads(response.text)['data'],['1'],['symbol'])
        data = (json.loads(response.text))


        return data

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
   


# FUNCTION (GET SYMBOL FROM DATA)

def print_symbol(data):
    print(data)
    lst = []

    for i in data['data']:
        print(i['symbol'])

        lst.append(i['symbol']+'-USD')
    
    return lst

# FUNCTION (SAVE SYMBOL TO XLSX FROM DATA) 
def save_to_xlsx(data):
    
    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Define the string you want to save

    data_for_save = data


    # Iterate over the data and write it to the worksheet
    for row in data_for_save:
        worksheet.append([row])

    # Save the workbook
    workbook.save("crypto_ticker_list.xlsx")

# RUN 
#save_to_xlsx(print_symbol(get_data()))

def save_to_csv(my_list):
    # Open a file for writing
    with open('list.csv', 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        
        # Write the rows of the list to the CSV file
        for row in my_list:
            writer.writerow(row)


# RUN not work
#save_to_csv(print_symbol(get_data()))