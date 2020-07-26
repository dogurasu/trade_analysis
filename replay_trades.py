import pandas, pathlib, sys, math

# get path to file
# for windows vscode terminal - pandas.read_csv(str(pathlib.Path().parent.absolute()) + "\\trading_data\\Replays\\5-20-2020\\INO\\replay_INO_5-20-2020--altered.csv")

# Make sure you go into Excel and sort your trades by Time before running this script

path = str(pathlib.Path(__file__).parent.absolute())
month, day, ticker = sys.argv[1], sys.argv[2], sys.argv[3]
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

# TODO
# - Implement P&L Calculation after each trade
#     - keep track of a flag for whether a new trade was started or not(buy or sell of 50 shares)
#     - keep a counter for how many shares have been covered so far
#     - reset the counter and flag after calculating total profits or losses
# - Calculate commissions for each trade (using CMEG's $0.50 minimum)

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
for order in range(len(exec_orders.values)):
    # set the order type to Buy or Sell (or Shrt for live_trades)
    order_type = exec_orders.values[order][0]
    # record the total that the trade was initiated (100 shares * the price)
    price_filled = exec_orders.values[order][3]
    shares_left = 100
    net_profits = 0
    order += 1 # increment iterator to next row
    completed['net_pl'].append(0)
    # net_pl.append(0)
    while shares_left > 0:
        if exec_orders.values[order][0] == 'Sell': # and assuming order_type is of 'Buy', A.K.A. 'Going Long'
            completed['net_pl'].append(round(exec_orders.values[order][2]*(exec_orders.values[order][3] - price_filled), 3)) # A ( C - B)
            # net_pl.append(round(exec_orders.values[order][2]*(exec_orders.values[order][3] - price_filled), 3))
        if exec_orders.values[order][0] == 'Buy': # and assuming order_type is of 'Sell', A.K.A. 'Shorting'
            completed['net_pl'].append(round(exec_orders.values[order][2]*(price_filled - exec_orders.values[order][3]), 3)) # A ( B - C)
            # net_pl.append(round(exec_orders.values[order][2]*(price_filled - exec_orders.values[order][3]), 3))
        shares_left += -exec_orders.values[order][2] # decrement size of order
        order += 1
    if order == 39:
        break

# copy over exec_orders to completed
for order in exec_orders.values:
    completed['order_type'].append(order[0])
    completed['ticker'].append(order[1])
    completed['size'].append(order[2])
    completed['price_filled'].append(order[3])
    completed['route'].append(order[4])
    completed['time_filled'].append(order[5])

completed = pandas.DataFrame(completed, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled", "net_pl"])

completed.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020--altered.csv", index=False, header=True)

# completed.to_csv(path + f"\\trading_data\\Replays\\{month}-{day}-2020\\{ticker}\\replay_{ticker}_{month}-{day}-2020.csv")