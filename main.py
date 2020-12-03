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
