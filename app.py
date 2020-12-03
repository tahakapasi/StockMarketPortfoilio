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
        for property in minmax_properties:
            current_value = getattr(c, property)
            if isinstance(current_value, float):
                if not minmax_properties[property]['Min']:
                    minmax_properties[property]['Min'] = current_value
                if not minmax_properties[property]['Max']:
                    minmax_properties[property]['Max'] = current_value
                if current_value < minmax_properties[property]['Min']:
                    minmax_properties[property]['Min'] = current_value
                if current_value > minmax_properties[property]['Max']:
                    minmax_properties[property]['Max'] = current_value
    return jsonify(minmax_properties)


@app.route("/filter", methods=['POST', 'GET'])
def filter_stock():
    with open(DATA_FILE, 'rb') as f:
        companies = pickle.load(f)
    filtered_companies = []
    for company in companies:
        if company.Price:
            if request.json['Price']['Min'] and company.Price < request.json['Price']['Min']:
                continue
            if request.json['Price']['Min'] and company.Price > request.json['Price']['Max']:
                continue
        if 'min_peratio' in request.json and company.PERatio and company.PERatio < request.json['min_peratio']:
            continue
        if 'max_peratio' in request.json and company.PERatio and company.PERatio > request.json['max_peratio']:
            continue
        if 'min_volume' in request.json and company.Volume and company.Volume < request.json['min_volume']:
            continue
        if 'max_volume' in request.json and company.Volume > request.json['max_volume']:
            continue
        if 'min_market_cap' in request.json and company.MarketCap and company.MarketCap < request.json['min_market_cap']:
            continue
        if 'max_market_cap' in request.json and company.MarketCap and company.MarketCap < request.json['max_market_cap']:
            continue
        if 'min_avg_volume' in request.json and company.AverageVolume and company.AverageVolume < request.json['min_avg_volume']:
            continue
        if 'max_avg_volume' in request.json and company.AverageVolume and company.AverageVolume > request.json['max_avg_volume']:
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

        filtered_companies.append(company.SYM)

    return jsonify({"List": filtered_companies,
                    "Count": len(filtered_companies)})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
     # with open(DATA_FILE, 'rb') as f:
    #     companies = pickle.load(f)
    # print(len(companies))
    # for c in companies:
    # #     if c.SYM == 'AZO' or c.SYM == "NVR":
    #     if c.SYM == "HCLP":
    #         companies.remove(c)
    # with open("processed_companies.pkl", 'wb') as f:
    #     pickle.dump(companies, f)
