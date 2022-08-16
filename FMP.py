import requests
import certifi
from urllib.request import urlopen
import json

class FMP:

    def __init__(self, token, symbol):
        self.BASE_URL = 'https://financialmodelingprep.com/api/v3'
        self.token = token
        self.symbol = symbol

    def get_DCF(self):
        url = f'{self.BASE_URL}/company/discounted-cash-flow/{self.symbol}?apikey={self.token}'
        return url

    def get_fundamental_ratios(self):
        url = f'{self.BASE_URL}/ratios/{self.symbol}?apikey={self.token}'
        return url

    def get_company_profile(self):
        url = f'{self.BASE_URL}/profile/{self.symbol}?apikey={self.token}'
        return url

    def get_marketcap(self):
        url = f'{self.BASE_URL}/market-capitalization/{self.symbol}?apikey={self.token}'
        return url

    def get_hourly_stockprice(self):
        url = f'{self.BASE_URL}/historical-chart/1hour/{self.symbol}?apikey={self.token}'
        return url