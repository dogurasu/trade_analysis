import os, requests, json, csv, pandas
from os.path import join, dirname
from dotenv import load_dotenv

# grab the dir path
path = join(dirname(__file__))#, '.env')
load_dotenv(path + '.env')

AV_KEY = os.environ.get("AVKEY1")
print(AV_KEY)

# call AlphaVantage API
payload = {
    'apikey': AV_KEY,
    'outputsize': 'full',
    'interval': '1min',
    'symbol': 'CBAT',
    'function': 'TIME_SERIES_INTRADAY',
    'datatype': 'csv',
    'adjusted': 'false'
    }

# payload = {
#     'function': 'TIME_SERIES_INTRADAY',
#     'symbol': 'IBM',
#     'interval': '5min',
#     'outputsize': 'full',
#     'apikey': "demo",
#     'datatype': 'csv'
#     }
# JSON: https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo
# CSV: https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv
info = {}
try:
    response = requests.get("https://www.alphavantage.co/query?", params=payload)
    # print(response.url)
    # if (response.status_code == 200):
        # print(f'Status: {response.status_code}, continuing program.')
        # json.dumps(response.json(), indent=4)
except:
    print(f'Exception caught. Exiting program...')
    exit()

# response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv")
decoded_content = response.content.decode('utf-8')
csv_obj = csv.reader(decoded_content.splitlines(), delimiter=',')
data = list(csv_obj)
df = pandas.DataFrame(data)
df.reset_index(drop=True, inplace=True)
df.to_csv('CBAT.csv', index=None)

# with open('IBM.csv', 'w', newline='') as f:
#     ibm_writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     r = []
#     for elem in data[0]:
#         r.append(elem)
#     print(r)
    # ibm_writer.writerow(r)
    # ibm_writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    # ibm_writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    # ibm_writer.writerow(['John Smith', 'Accounting', 'November'])
    # ibm_writer.writerow(['Erica Meyers', 'IT', 'March'])

# write data to csv file


# print(info.keys())
# print(len(info['Time Series (5min)']))

# with open("books.csv", "r", newline="") as csvfile:
#     bookreader = csv.reader(csvfile, delimiter=',')
#     for row in bookreader:
#         # print(", ".join(row))
#        print(row)

# with open(path + "data.txt", "w") as out:
#     out.write()


# turn json data into csv