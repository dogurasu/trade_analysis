import pandas, pathlib

# TODO
# - Implement P&L Calculation after each trade
#     - keep track of a flag for whether a new trade was started or not(buy or sell of 50 shares)
#     - keep a counter for how many shares have been covered so far
#     - reset the counter and flag after calculating total profits or losses
# - Calculate commissions for each trade (using CMEG's $0.50 minimum)

# get path to file
# for windows vscode terminal - pandas.read_csv(str(pathlib.Path().parent.absolute()) + "\\trading_data\\7-24-2020\\7-24-2020.csv")
path = str(pathlib.Path(__file__).parent.absolute())
month, day = '7', '24'
txt_path = path + f"\\trading_data\\{month}-{day}-2020\\{month}-{day}-2020.csv"

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

exec_orders = pandas.DataFrame(exec_orders, columns=["order_type", "ticker", "size", "price_filled", "route", "time_filled", "net_profit"])

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
pnl = []
net_profit = []

new_trade = True
for order in range(len(exec_orders.values)):
    # check if we're at a new trade
    if new_trade:
        new_trade = False
        shares_left = 50
        base_sum = exec_orders.values[order][2]*50 # (price_filled) * (50_shares)
        order_type = exec_orders.values[order][0] # 'Buy', 'Sell', 'Short'
        pnl.append(0) # add 0 for starting profit
        net = 0

        if order_type == 'Buy':
            while shares_left != 0: # keep calculating net profit
                transact_size = exec_orders.values[order][1]
                sell_sum = exec_orders.values[order][2] * transact_size
                pnl.append(sell_sum - base_sum)
                shares_left -= transact_size
                if shares_left == 0:
                    net_profit.append()
        elif order_type == 'Shrt':
            while shares_left != 0: # keep calculating net profit

        else: # order_type == 'Sell'
            while shares_left != 0: # keep calculating net profit

        # record the total that the trade was initiated (50 shares * the price)
        continue 

df.to_csv(path + f"\\trading_data\\{month}-{day}-2020\\{month}-{day}-2020_altered.csv", index=False, header=True)