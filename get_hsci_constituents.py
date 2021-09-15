
import requests

### URL
HSCI_URL = "https://www.hsi.com.hk/data/chi/rt/index-series/hsci/constituents.do"

### Yahoo symbol extension
YAHOO_SYMBOL_EXTENSION = ".HK"


def get_json() -> dict:
    """ Get requests json """
    r = requests.session()
    return r.get(HSCI_URL).json()


def code_to_yahoo_symbol(code: str) -> str:
    """
    Return the yahoo symbol given the number of stock code

    Args:
        code: Stock number
    """
    return "0" * (4-len(code)) + code + YAHOO_SYMBOL_EXTENSION


def get_constituents(res_json: dict) -> list:
    """
    Return all constituents symbol (in Yahoo format)

    Args:
        res_json: response json got from requests
    """
    constituents = []

    index_series_list = res_json["indexSeriesList"][0]
    index_list = index_series_list["indexList"][0]
    constituent_content = index_list["constituentContent"]
    
    for constituent in constituent_content:
        constituents.append(code_to_yahoo_symbol(constituent["code"]))

    return constituents


if __name__ == "__main__":
    res_json = get_json()
    constituents = get_constituents(res_json=res_json)
    print(constituents)