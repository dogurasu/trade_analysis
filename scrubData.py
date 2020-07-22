import pandas, pathlib

txt_path = str(pathlib.Path(__file__).parent.absolute()) + "\\trading_data\\7-22-2020.csv"

print(pandas.read_csv(txt_path))