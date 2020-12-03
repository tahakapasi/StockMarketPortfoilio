#!/usr/bin/python3

# Look at this URL for list data schema
# http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs

import company
import main
import json
import pickle
import requests
from bs4 import BeautifulSoup
import pprint
import datetime


def get_data(row):
    sym, name, etf = row['SYM'], row['Name'], row['ETF']
    if etf:
        if etf == 'Y':
            etf = True
        else:
            etf = False
    else:
        etf = False
    BASE_URL = main.HOME_URL + sym
    page = requests.get(f"{BASE_URL}")
    soup = BeautifulSoup(page.content, features='html.parser')
    results = soup.find_all('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    price = None
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
                market_cap = float(market_cap.replace('T', ''))
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

    profile_page = requests.get(f"{BASE_URL}{main.PROFILE}")
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

    financial_page = requests.get(f"{BASE_URL}{main.FINANCIALS}")
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

    balance_page = requests.get(f"{BASE_URL}{main.BALANCE_SHEET}")
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
        'ETF': etf,
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
    return company_dict

COMPANIES = []
PREPROCESSED = []


# Reading NASDAQ file and adding data to list
def nasdaq_list_loader():
    with open("nasdaqlisted.txt") as f:
        f.readline()
        row = f.readline()
        while row:
            row = row.split('|')
            entry = {
                "SYM": row[0],
                "Name": row[1],
                "ETF": row[6]
            }
            PREPROCESSED.append(entry)
            row = f.readline()
    PREPROCESSED.remove(PREPROCESSED[len(PREPROCESSED) - 1])


def other_list_loader():
    with open("otherlisted.txt") as f:
        f.readline()
        row = f.readline()
        while row:
            row = row.split('|')
            entry = {
                "SYM": row[6],
                "Name": row[1],
                "ETF": row[4]
            }
            PREPROCESSED.append(entry)
            row = f.readline()
    PREPROCESSED.remove(PREPROCESSED[len(PREPROCESSED) - 1])


pp = pprint.PrettyPrinter(indent=3)
main_counter = 0
nasdaq_list_loader()
other_list_loader()
exit()
for entity in PREPROCESSED:
    company_dict = get_data(entity)
    pp.pprint(company_dict)
    cmpny = company.Company(**company_dict)
    COMPANIES.append(cmpny)
    main_counter += 1
    if main_counter % 100 == 0:
        print(main_counter)
    for c in COMPANIES:
        if not c.Price:
            COMPANIES.remove(c)
with open(main.DATA_FILE, "wb") as f:
    pickle.dump(COMPANIES, f)
print(f"Complete: {datetime.datetime.now()}")
