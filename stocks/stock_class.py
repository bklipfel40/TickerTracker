"""https://financialmodelingprep.com/api/v3/company/profile/AAPL"""
import requests


class StockProfile:
    symbol: str
    company_name: str
    industry: str
    website: str
    description: str
    ceo: str
    sector: str
    image: str
    price: str
    changes: str
    changes_percentage: str

    def __init__(self, stock_name: str):
        url = "https://financialmodelingprep.com/api/v3/company/profile/"
        url = url + stock_name
        try:
            data = requests.get(url).json()
        except requests.exceptions.RequestException:  # This is the correct syntax
            return None

        self.symbol = data["symbol"]
        data = data["profile"]
        self.company_name = data["companyName"]
        self.industry = data["industry"]
        self.website = data["website"]
        self.description = data["description"]
        self.ceo = data["ceo"]
        self.sector = data["sector"]
        self.image = data["image"]
        self.price = data["price"]
        self.changes = data["changes"]
        self.changes_percentage = data["changesPercentage"]


def get_historical_price(stock_name, num_days):
    url = "https://financialmodelingprep.com/api/v3/historical-price-full/"
    url = url + stock_name + "?serietype=line"
    ret = [[], []]

    try:
        data = requests.get(url).json()
        data = data["historical"]
        length = len(data)
    except requests.exceptions.RequestException:  # This is the correct syntax
        return None
    else:
        for x in range(length-num_days, length):
            ret[0].append(data[x]["close"])
            ret[1].append(data[x]["date"][5:])
        return ret


def get_historical_cash_flow(stock_name):
    url = "https://financialmodelingprep.com/api/v3/company-key-metrics/"
    url = url + stock_name
    ret = [[], []]

    try:
        data = requests.get(url).json()
        data = data["metrics"]
        length = len(data)
    except requests.exceptions.RequestException:  # This is the correct syntax
        return None
    else:
        for x in range(length):
            ret[0].append(data[x]["Free Cash Flow per Share"])
            ret[1].append(data[x]["date"][0:4])
        ret[0].reverse()
        ret[1].reverse()
        return ret
