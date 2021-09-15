from yahoo_data.yahoo_data import YahooData
from yahoo_data.symbols import HSCI_SYMBOL

from datetime import datetime
import os
import pandas as pd
import time



### Symbols

SYMBOLS = ["hsi", "hhi"] + HSCI_SYMBOL

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



def get_last_date_from_csv() -> str:

    """ Return the last date in hsi csv """

    csv_file_path = get_csv_file_path("hsi")
        
    df = pd.read_csv(csv_file_path)
    
    date = df.values[-1][0]

    if date[4] == "/":
        date = date.split("/")
        return f"{date[0]}-{date[1]}-{date[2]}"
    else:
        return date



if __name__ =="__main__":
    start_time = time.time()

    ### Excel file
    LOCAL_PATH = os.path.abspath("#Excel report")
    COMBINE_EXCEL_PATH = os.path.join(LOCAL_PATH, get_last_date_from_csv() + ".xlsx")

    crosses = []

    for symbol in SYMBOLS:

        csv_file_path = get_csv_file_path(symbol)
        
        tdf = pd.read_csv(csv_file_path)
        tdf = tdf.dropna()
        ### Check last date is today or not (Sometimes forget to do last night)
        if datetime.now() > datetime.strptime(tdf["Date"].iloc[-1], "%Y-%m-%d"):
            tdf = tdf.iloc[:-1]

        tdf["MA1"] = tdf["Adj Close"].rolling(window=MA1).mean()
        tdf["MA2"] = tdf["Adj Close"].rolling(window=MA2).mean()
        tdf["Cross"] = tdf["MA1"]>tdf["MA2"]
        
        cross = get_cross_date(tdf)
        crosses.append(cross)

    df = pd.DataFrame(data={"symbol": SYMBOLS, "cross": crosses})

    df.to_excel(COMBINE_EXCEL_PATH, index=False)
    print(df)
        
    print(f"Time used {time.time() - start_time} second(s)")

