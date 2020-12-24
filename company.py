# Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
# ACT Symbol|Security Name|Exchange|CQS Symbol|ETF|Round Lot Size|Test Issue|NASDAQ Symbol
class Company:
    def __init__(self, **kwargs):
        self.SYM = kwargs['SYM']
        self.ETF = kwargs['ETF']
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

    def is_valid(self):
        if self.SYM != 'Y' and self.Price and isinstance(self.Price, float) and \
                self.Volume and isinstance(self.Volume, float) and \
                self.AverageVolume and isinstance(self.AverageVolume, float) and \
                self.MarketCap and isinstance(self.MarketCap, float) and \
                self.EPS and isinstance(self.EPS, float):
                if self.EPS < 0:
                    return True
                if self.PERatio and isinstance(self.PERatio, float):
                    return True
                else:
                    return False
        else:
            return False
