from yahoo_data.yahoo_data import YahooData
from yahoo_data.symbols import HSCI_SYMBOL

import time

"""
Time used 19.84109926223755 second(s)
"""

if __name__ == "__main__":
    start_time = time.time()

    symbols = ["^hsi", "^hsce"] + HSCI_SYMBOL
    
    for symbol in symbols:
        y = YahooData(symbol)
        y.download_data()
    
    print(f"Time used {time.time() - start_time} second(s)")