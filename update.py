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
            return {}
        else:
            etf = False
    else:
        etf = False
    BASE_URL = main.HOME_URL + sym
    page = requests.get(f"{BASE_URL}")
    soup = BeautifulSoup(page.content, features='html.parser')
    results = soup.find_all('h1', {'class': 'company__name'})
    if results:
        name = results[0].get_text()
    results = soup.find_all('bg-quote', {'class': 'value'})
    price = None
    try:
        price = results[0].get_text()
        price = float(price.replace(',', ''))
    except IndexError:
        price = None
    except ValueError:
        print(f"Value Error {price}")
        price = None
    results = soup.find_all('li', {'class': 'kv__item'})
    volume = None
    avg_volume = None
    peratio = None
    market_cap = None
    eps = None
    yield_data = None
    dividend = None
    revperemployee = None
    i = 0
    for result in results:
        data = result.get_text()
        data = data.strip().split()
        data = data[len(data) - 1]
        if data == 'N/A':
            data = None
        if i == 3:
            market_cap = data
            if market_cap:
                market_cap = convert_multiplier(market_cap)
        elif i == 7:
            revperemployee = data
            if revperemployee:
                revperemployee = convert_multiplier(revperemployee)
        elif i == 8:
            peratio = data
            if peratio:
                peratio = float(peratio.replace(',', ''))
        elif i == 9:
            eps = data
            if eps:
                eps = float(eps.replace(',', '').replace('$', ''))
        elif i == 10:
            yield_data = data
            if yield_data:
                yield_data = float(yield_data.replace(',', '').replace('%', ''))
        elif i == 11:
            dividend = data
            if dividend:
                dividend = float(dividend.replace(',', '').replace('$', ''))
        elif i == 15:
            avg_volume = data
            if avg_volume:
                avg_volume = convert_multiplier(avg_volume)
        i += 1

    profile_page = requests.get(f"{BASE_URL}{main.PROFILE}")
    soup = BeautifulSoup(profile_page.content, features='html.parser')
    results = soup.find_all('li', {'class': 'kv__item w100'})

    i = 0
    sector = None
    industry = None
    for result in results:
        data = result.get_text().strip().split('\n')
        data = data[len(data) - 1]
        if i == 0:
            sector = data
        elif i == 1:
            industry = data
        i += 1

    financial_page = requests.get(f"{BASE_URL}{main.FINANCIALS}")
    soup = BeautifulSoup(financial_page.content, features='html.parser')

    i = 0
    results = soup.find_all('th', {'class': 'overflow__heading'})
    year_list = []
    revenue_history = {}
    interest_expense_history = {}
    cogs_incl_da = {}
    cogs_excl_da = {}
    gross_profit_margin = {}
    sga_expense = {}
    unusual_expense = {}
    ebit_after_unusual_expense = {}
    net_income = {}
    eps_historical = {}
    ebitda = {}
    ebitda_margin = {}
    for result in results:
        if i > 0:
            data = result.get_text().strip()
            if data != '5-year trend':
                year_list.append(int(data))
        i += 1
    i = 1
    j = 1
    col_count = len(year_list)
    results = soup.find_all('td', {'class': 'overflow__cell'})
    row_data = {}
    for result in results:
        data = result.get_text().strip()
        if 1 < i < len(year_list) + 1:
            if data and data != '-':
                if '(' in data:
                    data = data.replace('(', '').replace(')', '')
                    data = '-' + data
                data = data.replace('%', '')
                data = convert_multiplier(data)
                row_data[year_list[i - 2]] = data
            else:
                row_data[year_list[i - 2]] = None

        if not i % (col_count + 2):
            if j == 1:
                revenue_history = row_data
            elif j == 3:
                cogs_incl_da = row_data
            elif j == 5:
                cogs_excl_da = row_data
            elif j == 11:
                gross_profit_margin = row_data
            elif j == 12:
                sga_expense = row_data
            elif j == 17:
                unusual_expense = row_data
            elif j == 18:
                ebit_after_unusual_expense = row_data
            elif j == 22:
                interest_expense_history = row_data
            elif j == 46:
                net_income = row_data
            elif j == 49:
                eps_historical = row_data
            elif j == 55:
                ebitda = row_data
            elif j == 57:
                ebitda_margin = row_data
            j += 1
            i = 1
            row_data = {}
        else:
            i += 1

    # balance_page = requests.get(f"{BASE_URL}{main.BALANCE_SHEET}")
    # soup = BeautifulSoup(balance_page.content, features='html.parser')
    # results = soup.find_all('div', {
    #     'class': [
    #         'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(tbc)',
    #         'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg Bgc($lv1BgColor)'
    #         ' fi-row:h_Bgc($hoverBgColor) D(tbc)'
    #     ]
    # })
    liabilities = []
    # i = 0
    # for result in results:
    #     if i in [128, 129, 130, 131]:
    #         data = result.get_text()
    #         if data:
    #             data = float(data.replace(',', ''))
    #         else:
    #             data = None
    #         liabilities.append(data)
    #     i += 1
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
        'Profit History': net_income,
        'Interest Expense History': interest_expense_history,
        'Liabilities': liabilities,
        'RevperEmployee': revperemployee,
        'Dividend': dividend,
        'Yield': yield_data,
        'Cogs_incl_DA': cogs_incl_da,
        'Cogs_excl_DA': cogs_excl_da,
        'GrossProfitMargin': gross_profit_margin,
        'SGAExpense': sga_expense,
        'UnusualExpense': unusual_expense,
        'EBITAfterUnusualExpense': ebit_after_unusual_expense,
        'EPSHistorical': eps_historical,
        'EBITDA': ebitda,
        'EBITDAMargin': ebitda_margin
    }
    return company_dict


def convert_multiplier(value) -> float:
    value = value.replace('$', '').replace(',', '')
    if 'T' in value:
        value = float(value.replace('T', ''))
        multiplier = 1000000000000
        value = value * multiplier
    elif 'B' in value:
        value = float(value.replace('B', ''))
        multiplier = 1000000000
        value = value * multiplier
    elif 'M' in value:
        value = float(value.replace('M', ''))
        multiplier = 1000000
        value = value * multiplier
    elif 'K' in value:
        value = float(value.replace('K', ''))
        multiplier = 1000
        value = value * multiplier
    else:
        value = float(value)
    return value


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
failure_count = 0
for entity in PREPROCESSED:
    try:
        company_dict = get_data(entity)
    except Exception as e:
        print(entity)
        failure_count += 1
        continue
    # pp.pprint(company_dict)
    if company_dict:
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
print(f"Failed: {failure_count}")