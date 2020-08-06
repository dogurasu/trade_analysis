import pandas, pathlib, sys, math

# TODO
# - Implement P&L Calculation after each trade
#     - keep track of a flag for whether a new trade was started or not(buy or sell of 50 shares)
#     - keep a counter for how many shares have been covered so far
#     - reset the counter and flag after calculating total profits or losses
# - Calculate commissions for each trade (using CMEG's $0.50 minimum)

# get path to file
# for windows vscode terminal - pandas.read_csv(str(pathlib.Path().parent.absolute()) + "\\trading_data\\7-24-2020\\7-24-2020.csv")
path = str(pathlib.Path(__file__).parent.absolute())
month, day, ticker, size_per_trade = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
txt_path = path + f"\\trading_data\\{month}-{day}-2020\\{ticker}\\{ticker}_{month}-{day}-2020.csv"

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

for arr in reversed(data.values):
    if arr[0] == 'Execute':
        exec_orders['order_type'].append(arr[1])
        exec_orders['ticker'].append(arr[2])
        exec_orders['size'].append(arr[3])
        exec_orders['price_filled'].append(arr[4])
        exec_orders['route'].append(arr[5])
        exec_orders['time_filled'].append(arr[6])

exec_orders = pandas.DataFrame(exec_orders, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled"])
exec_orders.to_csv(path + f"\\trading_data\\{month}-{day}-2020\\{ticker}\\{ticker}_{month}-{day}-2020_altered.csv", index=False, header=True)

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

order = 0
num_trades = 0
while order < len(exec_orders.values):
    # set the order type to Buy or Sell (or Shrt for live_trades)
    order_type = exec_orders.values[order][0]
    # record the total that the trade was initiated (100 shares * the price)
    price_filled = exec_orders.values[order][3]
    # print(exec_orders.values[order])
    # print(f'Order_type: {order_type}, Shares left: {shares_left}, price_filled: {price_filled}')
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
            # net_pl.append(round(exec_orders.values[order][2]*(exec_orders.values[order][3] - price_filled), 3))
        if exec_orders.values[order][0] == 'Buy' and order_type == 'Sell': # assuming order_type is of 'Sell', A.K.A. 'Shorting'
            completed['net_pl'].append(round(exec_orders.values[order][2]*(price_filled - exec_orders.values[order][3]), 3)) # A ( B - C)
            # net_pl.append(round(exec_orders.values[order][2]*(price_filled - exec_orders.values[order][3]), 3))
        shares_left -= exec_orders.values[order][2] # decrement size of order
        order += 1
        if order == len(exec_orders.values):
            break
    # print(f'after \'while\', order: {order}')
    # if order == len(exec_orders.values):
    #     break
# print(f'num trades: {len(exec_orders.values)}')
# print(f'exec_orders: {exec_orders.values}')
# print(f"len(completed['net_pl']): {completed['net_pl']}")
# print(len(completed['net_pl']))

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

# print(f"net_pl: {len(completed['net_pl'])}")
# print(f"gross_pl: {len(completed['gross_pl'])}")
# print(f"commissioned_pl: {len(completed['commissioned_pl'])}")
# print(f'num_trades: {num_trades}')

# copy over exec_orders to completed
for order in exec_orders.values:
    completed['order_type'].append(order[0])
    completed['ticker'].append(order[1])
    completed['size'].append(order[2])
    completed['price_filled'].append(order[3])
    completed['route'].append(order[4])
    completed['time_filled'].append(order[5])

print(f'len of order_type: {len(completed["order_type"])}')
print(f'len of net_pl: {len(completed["net_pl"])}')
print(f'len of gross_pl: {len(completed["gross_pl"])}')
print(f'len of commissioned_pl: {len(completed["commissioned_pl"])}')
print(f'len of num_trades: {len(completed["num_trades"])}')
print(f'len of ticker: {len(completed["ticker"])}')
# print(f'ticker: {completed["ticker"]}')
print(f'len of price_filled: {len(completed["price_filled"])}')
print(f'len of time_filled: {len(completed["time_filled"])}')

# for i in completed:
#     print(i)

completed = pandas.DataFrame(completed, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled", "net_pl", 'gross_pl', 'commissioned_pl', 'num_trades'])

completed.to_csv(path + f"\\trading_data\\{month}-{day}-2020\\{ticker}\\{ticker}_{month}-{day}-2020--altered_complete.csv", index=False, header=True)