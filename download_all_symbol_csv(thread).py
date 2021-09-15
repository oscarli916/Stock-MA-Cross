from yahoo_data.yahoo_data import YahooData
from yahoo_data.symbols import HSCI_SYMBOL

import threading
import time

"""
Time used 3.9047341346740723 second(s)
"""

if __name__ == "__main__":
    start_time = time.time()

    symbols = ["^hsi", "^hsce"] + HSCI_SYMBOL
    threads = []

    for symbol in symbols:
        y = YahooData(symbol)
        thread = threading.Thread(target=y.download_data, name=symbol)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    print(f"Time used {time.time() - start_time} second(s)")