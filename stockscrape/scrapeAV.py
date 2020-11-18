import os, requests, json, csv
from os.path import join, dirname
from dotenv import load_dotenv

# grab the dir path
path = join(dirname(__file__))#, '.env')
load_dotenv(path + '.env')

AV_KEY = os.environ.get("AVKEY1")
print(AV_KEY)

# call AlphaVantage API
# payload = {
#     'apikey': AV_KEY,
#     'outputsize': 'full',
#     'interval': '1min',
#     'symbol': 'CBAT',
#     'function': 'TIME_SERIES_INTRADAY'
#     }

payload = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': 'IBM',
    'interval': '5min',
    'outputsize': 'full',
    'apikey': "demo",
    }
# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo
info = {}
try:
    response = requests.get("https://www.alphavantage.co/query?", params=payload)
    print(response.url)
    if (response.status_code == 200):
        # print(f'Status: {response.status_code}, continuing program.')
        json.dumps(response.json(), indent=4)
except:
    print(f'Exception caught. Exiting program...')
    exit()

info = response.json()
print(info.keys())
print(len(info['Time Series (5min)']))

with open("books.csv", "r", newline="") as csvfile:
    bookreader = csv.reader(csvfile, delimiter=',')
    for row in bookreader:
        # print(", ".join(row))
        print(row)

# with open(path + "data.txt", "w") as out:
#     out.write()


# turn json data into csv