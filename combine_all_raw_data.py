from yahoo_data.yahoo_data import YahooData
from yahoo_data.symbols import HSI_SYMBOL, HSCI_SYMBOL

import os
import pandas as pd
import time

### Excel file
COMBINE_EXCEL = "combine.xlsx"
LOCAL_PATH = os.path.abspath("")
COMBINE_EXCEL_PATH = os.path.join(LOCAL_PATH, COMBINE_EXCEL)
### Symbols
SYMBOLS = ["hsi", "hhi"] + HSCI_SYMBOL
SYMBOLS = ["hsi", "hhi", "0669.HK"]
### MA
MA1 = 10
MA2 = 20

def get_csv_file_path(symbol: str) -> str:
    """
    Return symbol csv path

    Args:
        symbol: symbol name
    """
    return os.path.join(YahooData.CSV_PATH, f"{symbol}.csv")

def get_cross_date(df: pd.DataFrame) -> int:
    """
    Return the number of cross date.
    If haven't cross then return 0

    Args:
        df: symbol Dataframe
    """
    cross = 0
    values = df.values
    idx = len(values) - 1
    while values[idx][-1] == True:
        cross += 1
        idx -= 1
    return cross

if __name__ =="__main__":
    start_time = time.time()

    dfs = []

    for symbol in SYMBOLS:
        csv_file_path = get_csv_file_path(symbol)
        
        tdf = pd.read_csv(csv_file_path)
        tdf = tdf.dropna()
        tdf["MA1"] = tdf["Adj Close"].rolling(window=MA1).mean()
        tdf["MA2"] = tdf["Adj Close"].rolling(window=MA2).mean()
        tdf["Cross"] = tdf["MA1"]>tdf["MA2"]
        print(get_cross_date(tdf))
        dfs.append(tdf)

    # with pd.ExcelWriter(path=COMBINE_EXCEL_PATH) as writer:
    #     for idx in range(len(SYMBOLS)):
    #         dfs[idx].to_excel(writer, sheet_name=SYMBOLS[idx], index=False)
        
    print(f"Time used {time.time() - start_time} second(s)")