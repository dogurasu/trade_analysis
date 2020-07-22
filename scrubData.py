import pandas, pathlib

# get path to file
# for windows vscode terminal - pandas.read_csv(str(pathlib.Path().parent.absolute()) + "\\trading_data\\7-22-2020\\7-22-2020.csv")
path = str(pathlib.Path(__file__).parent.absolute())
txt_path = path + "\\trading_data\\7-22-2020\\7-22-2020.csv"

# check out the data
data = pandas.read_csv(txt_path)

# create an array with execute orders only
exec_orders = {
    'order_type': [],
    'ticker': [],
    'size': [],
    'price_filled': [],
    'route': [],
    'time_filled': []
}

for arr in data.values:
    if arr[0] == 'Execute':
        exec_orders['order_type'].append(arr[1])
        exec_orders['ticker'].append(arr[2])
        exec_orders['size'].append(arr[3])
        exec_orders['price_filled'].append(arr[4])
        exec_orders['route'].append(arr[5])
        exec_orders['time_filled'].append(arr[6])

df = pandas.DataFrame(exec_orders, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled"])

df.to_csv(path + "\\trading_data\\7-22-2020\\7-22-2020_altered.csv", index=False, header=True)