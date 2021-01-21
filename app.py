# Server Address: ec2-18-191-214-3.us-east-2.compute.amazonaws.com
import flask
from flask import jsonify,request
import pickle
from typing import List
from operator import attrgetter
from company import Company
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

DATA_FILE = 'processed_companies.pkl'


@app.route("/", methods=["GET"])
def home():
    return {"message": "Hello World"}


@app.route('/minmax', methods=["GET"])
def limits():
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    minmax_properties = {
        'Price': {'Min': None, 'Max': None},
        'Volume': {'Min': None, 'Max': None},
        'AverageVolume': {'Min': None, 'Max': None},
        'PERatio': {'Min': None, 'Max': None },
        'MarketCap': {'Min': None, 'Max': None},
        'EPS': {'Min': None, 'Max': None}
    }
    for c in companies:
        print(c.is_valid)
        if c.is_valid():
            for prop in minmax_properties:
                current_value = getattr(c, prop)
                if isinstance(current_value, float):
                    if not minmax_properties[prop]['Min']:
                        minmax_properties[prop]['Min'] = current_value
                    if not minmax_properties[prop]['Max']:
                        minmax_properties[prop]['Max'] = current_value
                    if current_value < minmax_properties[prop]['Min']:
                        minmax_properties[prop]['Min'] = current_value
                    if current_value > minmax_properties[prop]['Max']:
                        minmax_properties[prop]['Max'] = current_value
    return jsonify(minmax_properties)


@app.route("/filter", methods=['POST', 'GET'])
def filter_stock():
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    filtered_companies = []
    for company in companies:
        if company.is_valid():
            if request.json['Price']['Min'] and company.Price < request.json['Price']['Min']:
                continue
            if request.json['Price']['Max'] and company.Price > request.json['Price']['Max']:
                continue
            if company.PERatio:
                if request.json['PERatio']['Min'] and company.PERatio < request.json['PERatio']['Min']:
                    continue
                if request.json['PERatio']['Max'] and company.PERatio > request.json['PERatio']['Max']:
                    continue
            if request.json['Volume']['Min'] and company.Volume < request.json['Volume']['Min']:
                continue
            if request.json['Volume']['Max'] and company.Volume > request.json['Volume']['Max']:
                continue
            if request.json['MarketCap']['Min'] and company.MarketCap < request.json['MarketCap']['Min']:
                continue
            if request.json['MarketCap']['Max'] and company.MarketCap > request.json['MarketCap']['Max']:
                continue
            if request.json['AverageVolume']['Min'] and company.AverageVolume < request.json['AverageVolume']['Min']:
                continue
            if request.json['AverageVolume']['Max'] and company.AverageVolume > request.json['AverageVolume']['Max']:
                continue
            if request.json['EPS']['Min'] and company.EPS < request.json['EPS']['Min']:
                continue
            if request.json['EPS']['Max'] and company.EPS > request.json['EPS']['Max']:
                continue
            if 'min_revenue' in request.json and company.RevenueHistory and company.RevenueHistory[0] < request.json['min_revenue']:
                continue
            if 'max_revenue' in request.json and company.RevenueHistory and company.RevenueHistory[0] > request.json['max_revenue']:
                continue
            if 'min_profit' in request.json and company.ProfitHistory and company.ProfitHistory[0] < request.json['min_profit']:
                continue
            if 'max_profit' in request.json and company.ProfitHistory and company.ProfitHistory[0] > request.json['max_profit']:
                continue
            if 'min_interest_expense' in request.json and company.InterestExpenseHistory and company.InterestExpenseHistory[0] < request.json['min_profit']:
                continue
            if 'max_interest_expense' in request.json and company.InterestExpenseHistory and company.InterestExpenseHistory[0] > request.json['max_profit']:
                continue
            if 'min_liabilities' in request.json and company.Liabilities and company.Liabilities[0] < request.json['min_liabilities']:
                continue
            if 'max_liabilities' in request.json and company.Liabilities and company.Liabilities[0] > request.json['max_liabilities']:
                continue
            if 'industry' in request.json and company.Industry and company.Industry not in request.json['industry']:
                continue
            if 'sector' in request.json and company.Sector and company.Sector not in request.json['sector']:
                continue
            filtered_companies.append(vars(company))
        else:
            continue
    # print(vars(filtered_companies[0]))
    return jsonify({"List": filtered_companies,
                    "Count": len(filtered_companies)})


if __name__ == '__main__':
    app.run(host='192.168.0.214')
    # with open(DATA_FILE, 'rb') as f:
    #     companies = pickle.load(f)
    # print(len(companies))
    # for c in companies:
    #     # if c.SYM == 'AZO' or c.SYM == "NVR":
    # #     if c.SYM == "HCLP":
    #     if c.SYM == "ZAZZT" or c.SYM == "ZBZZT":
    #         companies.remove(c)
    # with open("processed_companies.pkl", 'wb') as f:
    #     pickle.dump(companies, f)
