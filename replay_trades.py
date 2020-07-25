import pandas, pathlib

# get path to file
# for windows vscode terminal - pandas.read_csv(str(pathlib.Path().parent.absolute()) + "\\trading_data\\Replays\\5-13-2020\\INO\\replay_INO_5-13-2020.csv")

# Make sure you go into Excel and sort your trades by Time before running this script

path = str(pathlib.Path(__file__).parent.absolute())
month, day, ticker = '5', '13', 'INO'

txt_path = path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020.csv"
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
    if arr[2] == 'B':
        exec_orders['order_type'].append('Buy')
    else:
        exec_orders['order_type'].append('Sell')
    exec_orders['ticker'].append(arr[1])
    exec_orders['size'].append(arr[4])
    exec_orders['price_filled'].append(arr[3])
    exec_orders['route'].append(arr[5])
    exec_orders['time_filled'].append(arr[0])

exec_orders = pandas.DataFrame(exec_orders, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled"])

exec_orders.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020--altered.csv", index=False, header=True)

# TODO
# - Implement P&L Calculation after each trade
#     - keep track of a flag for whether a new trade was started or not(buy or sell of 50 shares)
#     - keep a counter for how many shares have been covered so far
#     - reset the counter and flag after calculating total profits or losses
# - Calculate commissions for each trade (using CMEG's $0.50 minimum)

# Implement Profit/Loss
# completed = {
#     'order_type': [],
#     'ticker': [],
#     'size': [],
#     'price_filled': [],
#     'route': [],
#     'time_filled': [],
#     'net_p&l': [],
# }

# new_trade = True
# for order in range(len(exec_orders.values)):
#     # check if we're at a new trade
#     if new_trade:
#         new_trade = False
#         shares_left = 50
#         # set the order type to Buy, Sell or Shrt
#         order_type = exec_orders.values[order][0]
#         # record the total that the trade was initiated (50 shares * the price)
#         total = exec_orders.values[order][3]*50
#         continue 

# completed.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020.csv")