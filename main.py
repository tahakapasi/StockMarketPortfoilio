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


def update():
    preprocessed = json.load(open("companies.json"))
    pp = pprint.PrettyPrinter(indent=3)
    main_counter = 0
    for entity in preprocessed:
        sym, name = entity['ACT Symbol'], entity['Company Name']
        BASE_URL = HOME_URL + sym
        page = requests.get(f"{BASE_URL}")
        soup = BeautifulSoup(page.content, features='html.parser')
        results = soup.find_all('span', {'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'})
        try:
            price = results[0].get_text()
            price = float(price.replace(',', ''))
        except IndexError:
            price = None
        except ValueError:
            print(f"Value Error {price}")
            price = None
        results = soup.find_all('td', {'class': 'Ta(end) Fw(600) Lh(14px)'})

        volume = None
        avg_volume = None
        peratio = None
        market_cap = None
        eps = None
        i = 0
        for result in results:
            if i == 6:
                volume = result.get_text()
                if volume != 'N/A':
                    volume = float(volume.replace(',', ''))
                else:
                    volume = None
            elif i == 7:
                avg_volume = result.get_text()
                if avg_volume != 'N/A' and avg_volume:
                    avg_volume = float(avg_volume.replace(',', ''))
                else:
                    avg_volume = None
            elif i == 8:
                # TODO: convert this to a number
                market_cap = result.get_text()
                if 'T' in market_cap:
                    market_cap = float(market_cap.replace('T',''))
                    multiplier = 1000000000000
                    market_cap = market_cap * multiplier
                elif 'B' in market_cap:
                    market_cap = float(market_cap.replace('B', ''))
                    multiplier = 1000000000
                    market_cap = market_cap * multiplier
                elif 'M' in market_cap:
                    market_cap = float(market_cap.replace('M', ''))
                    multiplier = 1000000
                    market_cap = market_cap * multiplier
            elif i == 10:
                peratio = result.get_text()
                if peratio != 'N/A':
                    peratio = float(peratio.replace(',', ''))
                else:
                    peratio = None
            elif i == 11:
                eps = result.get_text()
                if eps != 'N/A':
                    eps = float(eps.replace(',', '').replace('%', ''))
                else:
                    eps = None
            i += 1

        profile_page = requests.get(f"{BASE_URL}{PROFILE}")
        soup = BeautifulSoup(profile_page.content, features='html.parser')
        results = soup.find_all('span', {'class': 'Fw(600)'})

        i = 0
        sector = None
        industry = None
        for result in results:
            if i == 0:
                sector = result.get_text()
            elif i == 1:
                industry = result.get_text()
            i += 1

        financial_page = requests.get(f"{BASE_URL}{FINANCIALS}")
        soup = BeautifulSoup(financial_page.content, features='html.parser')
        results = soup.find_all('div', {
            'class': [
                'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) '
                'Miw(140px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)',
                'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(tbc)'
                      ]
        })
        i = 0
        revenue_history = []
        profit_history = []
        interest_expense_history = []
        for result in results:
            data = result.get_text()
            if data == '-' or not data:
                continue
            if i in [0, 1, 2, 3, 4]:
                data = float(data.replace(',', ''))
                revenue_history.append(data)
            elif i in [10, 11, 12, 13, 14]:
                data = float(data.replace(',', ''))
                profit_history.append(data)
            elif i in [40, 41, 42, 43, 44]:
                data = float(data.replace(',', ''))
                interest_expense_history.append(data)
            i += 1

        balance_page = requests.get(f"{BASE_URL}{BALANCE_SHEET}")
        soup = BeautifulSoup(balance_page.content, features='html.parser')
        results = soup.find_all('div', {
            'class': [
                'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(tbc)',
                'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg Bgc($lv1BgColor)'
                ' fi-row:h_Bgc($hoverBgColor) D(tbc)'
            ]
        })
        liabilities = []
        i = 0
        for result in results:
            if i in [128, 129, 130, 131]:
                data = result.get_text()
                if data:
                    data = float(data.replace(',', ''))
                else:
                    data = None
                liabilities.append(data)
            i += 1
        company_dict = {
            'SYM': sym,
            'Name': name,
            'Price': price,
            'Volume': volume,
            'Average Volume': avg_volume,
            'P/E Ratio': peratio,
            'Market Cap': market_cap,
            'EPS': eps,
            'Industry': industry,
            'Sector': sector,
            'Revenue History': revenue_history,
            'Profit History': profit_history,
            'Interest Expense History': interest_expense_history,
            'Liabilities': liabilities
        }
        # pp.pprint(company_dict)
        company = Company(**company_dict)
        COMPANIES.append(company)
        main_counter += 1
        if main_counter % 100 == 0:
            print(main_counter)
    with open(DATA_FILE, "wb") as f:
        pickle.dump(COMPANIES, f)



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
    # TODO: Write code to filter basic filtering
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    filtered_companies = []
    for company in companies:
        if company.Price:
            if min_price and company.Price and company.Price < min_price:
                print("jere")
                continue
            if max_price and company.Price and company.Price > max_price:
                print("jere")
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

        filtered_companies.append(company)
    return filtered_companies

def clean():
    companies = []
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    cleaned_companies = []
    for c in companies:
        if c.Price:
            cleaned_companies.append(c)
        else:
            print(f"{c.Name} : {c.SYM}")
    print(len(cleaned_companies))


if __name__ == '__main__':
    # update()
    clean()
    # x = filter(
    #     min_price=1,
    #     max_price=5
    # )
    # print(len(x))
    # print(x[0].Name
