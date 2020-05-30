import json
from bs4 import BeautifulSoup
import requests
import pprint
import pickle

HOME_URL = "https://finance.yahoo.com/quote/"
FINANCIALS = "/financials"
PROFILE = "/profile"
ANALYSIS = "/analysis"
BALANCE_SHEET = "/balance-sheet"
COMPANIES = []
DATA_FILE = "processed_companies.pkl"


class Company:
    def __init__(self, **kwargs):
        self.SYM = kwargs['SYM']
        self.Name = kwargs['Name']
        self.Price = kwargs['Price']
        self.Volume = kwargs['Volume']
        self.AverageVolume = kwargs['Average Volume']
        self.PERatio = kwargs['P/E Ratio']
        self.MarketCap = kwargs['Market Cap']
        self.EPS = kwargs['EPS']
        self.Industry = kwargs['Industry']
        self.Sector = kwargs['Sector']
        self.RevenueHistory = kwargs['Revenue History']
        self.ProfitHistory = kwargs['Profit History']
        self.InterestExpenseHistory = kwargs['Interest Expense History']
        self.Liabilities = kwargs['Liabilities']


def filter(
        min_price: int = None,
        max_price: int = None,
        min_peratio: int = None,
        max_peratio: int = None,
        min_volume: int = None,
        max_volume: int = None,
        min_market_cap: int = None,
        max_market_cap: int = None,
        min_ebitda: int = None,
        max_ebitda: int = None,
        min_avg_volume: int = None,
        max_avg_volume: int = None,
        min_revenue: int = None,
        max_revenue: int = None,
        min_profit: int = None,
        max_profit: int = None,
        min_interest_expense: int = None,
        max_interest_expense: int = None,
        min_liabilities: int = None,
        max_liabilities: int = None,
        industry: list = None,
        sector: list = None
):
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    filtered_companies = []
    for company in companies:
        company = Company(company)
        if min_price and company.Price < min_price:
            continue
        if max_price and company.Price > max_price:
            continue
        if min_peratio and company.PERatio and company.PERatio < min_peratio:
            continue
        if max_peratio and company.PERatio and company.PERatio > max_peratio:
            continue
        if min_volume and company.Volume and company.Volume < min_volume:
            continue
        if max_volume and company.Volume > max_volume:
            continue
        if min_market_cap and company.MarketCap and company.MarketCap < min_market_cap:
            continue
        if max_market_cap and company.MarketCap and company.MarketCap < max_market_cap:
            continue
        if min_avg_volume and company.AverageVolume and company.AverageVolume < min_avg_volume:
            continue
        if max_avg_volume and company.AverageVolume and company.AverageVolume > max_avg_volume:
            continue
        if min_revenue and company.RevenueHistory and company.RevenueHistory[0] < min_revenue:
            continue
        if max_revenue and company.RevenueHistory and company.RevenueHistory[0] > max_revenue:
            continue
        if min_profit and company.ProfitHistory and company.ProfitHistory[0] < min_profit:
            continue
        if max_profit and company.ProfitHistory and company.ProfitHistory[0] > max_profit:
            continue
        if min_interest_expense and company.InterestExpenseHistory and company.InterestExpenseHistory[0] < min_profit:
            continue
        if max_interest_expense and company.InterestExpenseHistory and company.InterestExpenseHistory[0] > max_profit:
            continue
        if min_liabilities and company.Liabilities and company.Liabilities[0] < min_liabilities:
            continue
        if max_liabilities and company.Liabilities and company.Liabilities[0] > max_liabilities:
            continue
        if industry and company.Industry and company.Industry not in industry:
            continue
        if sector and company.Sector and company.Sector not in sector:
            continue

        filtered_companies.append(company)
    return filtered_companies


if __name__ == '__main__':
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    print(companies[0].SYM)
    print(companies[0].RevenueHistory)
    # x = filter()
    # print(len(x))
