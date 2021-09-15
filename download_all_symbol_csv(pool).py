from yahoo_data.yahoo_data import YahooData
from yahoo_data.symbols import HSCI_SYMBOL

import concurrent.futures
import time

"""
Time used 10.519225597381592 second(s)

64 Thread: Time used 3.2545955181121826 second(s)
"""
def func(symbol):
    y = YahooData(symbol)
    y.download_data()

if __name__ == "__main__":
    start_time = time.time()

    symbols = ["^hsi", "^hsce"] + HSCI_SYMBOL
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        executor.map(func, symbols)
    
    print(f"Time used {time.time() - start_time} second(s)")