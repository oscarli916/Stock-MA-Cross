import os
import requests
import time

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s",)


class YahooData:

    ### URL
    DOWNLOAD_URL = "https://query2.finance.yahoo.com/v7/finance/download"
    BASE_URL = "https://finance.yahoo.com/quote/"

    ### Requests agent
    USER_AGENT = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')}
    r = requests.session()
    r.headers.update(USER_AGENT)
    COOKIE = r.get(BASE_URL).cookies.get_dict()

    ### CSV file path
    LOCAL_PATH = os.path.abspath("")
    CSV_FOLDER = r"#Raw Data"
    CSV_PATH = os.path.join(LOCAL_PATH, CSV_FOLDER)

    ### Special symbol
    convert_symbol = {
        "^hsi": "hsi",
        "^hsce": "hhi"
    }

    def __init__(self, symbol):
        self.symbol = symbol
    

    @property
    def csv_file_path(self):
        ### symbol CSV file path (str)
        csv_path = self.CSV_PATH
        if self.symbol in self.convert_symbol:
            csv_file_path = os.path.join(csv_path, f"{self.convert_symbol[self.symbol]}.csv")
        else:
            csv_file_path = os.path.join(csv_path, f"{self.symbol}.csv")
        return csv_file_path


    def _get_download_url(self):
        """ Return symbol download url (without param) """
        return f"{self.DOWNLOAD_URL}/{self.symbol}"


    def _save_data_as_csv(self, data: str) -> None:
        """
        Save data to csv file

        Args:
            data: csv data that want to download
        """
        if data == "": return
        with open(self.csv_file_path, "w") as f:
            f.write(data)


    def _get_param(self):
        """
        Return download url param
        All date from beginning and 1 day as interval
        """
        param = {
            "period1": 0,
            "period2": int(time.time()),
            "interval": "1d",
            # "events": "history",
            # "includeAdjustedClose": "true"
        }
        return param


    def download_data(self) -> str:
        """ Download symbol data and save to csv file """
        url = self._get_download_url()
        
        r = self.r.get(url=url, params=self._get_param(), cookies=self.COOKIE)
        r.close()
        # r.connection.close()

        if r.status_code != 200:
            logging.error(f"{self.symbol}: Status Code is not 200.")
            return ""

        self._save_data_as_csv(data=r.text)

    

"""
Method 2:
yfinance

Method 3:
https://query2.finance.yahoo.com/v8/finance/chart/0700.HK?period1=0&period2=1630800000&interval=1d
"""