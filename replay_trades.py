import pandas, pathlib, sys, math

# get path to file
# for windows vscode terminal - pandas.read_csv(str(pathlib.Path().parent.absolute()) + "\\trading_data\\Replays\\5-20-2020\\INO\\replay_INO_5-20-2020.csv")

# Make sure you go into Excel and sort your trades by Time before running this script

path = str(pathlib.Path(__file__).parent.absolute())
month, day, ticker, size_per_trade = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
# month, day, ticker = '5', '14', 'INO'

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
# exec_orders.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020--altered.csv", index=False, header=True)

# Implement Profit/Loss
completed = {
    'order_type': [],
    'ticker': [],
    'size': [],
    'price_filled': [],
    'route': [],
    'time_filled': [],
    'net_pl': [],
}

# this section of code calculates the net profits of each trade
# it assumes that you aren't adding into any of your trades in terms of additional shares and that you get rid of all your shares you initially purchased/sold
# num_orders = len(exec_orders.values)
order = 0
num_trades = 0
while order < len(exec_orders.values):
    # set the order type to Buy or Sell (or Shrt for live_trades)
    order_type = exec_orders.values[order][0]
    price_filled = exec_orders.values[order][3]
    shares_left = size_per_trade
    net_profits = 0
    order += 1 # increment iterator to next row
    completed['net_pl'].append(0)
    num_trades += 1
    if order == len(exec_orders.values):
        break
    # net_pl.append(0)
    while shares_left > 0:
        # print(f'order: {order}')
        if exec_orders.values[order][0] == 'Sell' and order_type == 'Buy': # assuming order_type is of 'Buy', A.K.A. 'Going Long'
            completed['net_pl'].append(round(exec_orders.values[order][2]*(exec_orders.values[order][3] - price_filled), 3)) # A ( C - B)
        if exec_orders.values[order][0] == 'Buy' and order_type == 'Sell': # assuming order_type is of 'Sell', A.K.A. 'Shorting'
            completed['net_pl'].append(round(exec_orders.values[order][2]*(price_filled - exec_orders.values[order][3]), 3)) # A ( B - C)
        shares_left -= exec_orders.values[order][2] # decrement size of order
        order += 1
        if order == len(exec_orders.values):
            break

# calculate net profits for the day (gross and w/ commissions)
net_profit = 0
completed['gross_pl'], completed['commissioned_pl'], completed['num_trades'] = [], [], []

print(completed['net_pl'])

for sum in completed['net_pl']:
    net_profit += sum
    completed['gross_pl'].append(0)
    completed['commissioned_pl'].append(0)
    completed['num_trades'].append(0)

completed['gross_pl'][0], completed['commissioned_pl'][0], completed['num_trades'][0] = net_profit, net_profit - len(exec_orders)//2, num_trades

# copy over exec_orders to completed
for order in exec_orders.values:
    completed['order_type'].append(order[0])
    completed['ticker'].append(order[1])
    completed['size'].append(order[2])
    completed['price_filled'].append(order[3])
    completed['route'].append(order[4])
    completed['time_filled'].append(order[5])

completed = pandas.DataFrame(completed, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled", "net_pl", 'gross_pl', 'commissioned_pl', 'num_trades'])

completed.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020--altered_complete.csv", index=False, header=True)

# completed.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020.csv")