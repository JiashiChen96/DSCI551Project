import os
import json
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination
from flask import make_response
from search import query, connectMongoDb

app = Flask(__name__)
app.debug=False
# bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/compare', methods=['get', 'post'])
def search():
    # print("*****************************************")
    filter = request.get_json(force=True)
    # return request.get_json(force=True),200
    # {manufacturer: "", year: "1234"}
    # city = request.get_json(force=True).get("city")

    print(filter)

    Craigslist = query({})
    TrueCar = connectMongoDb({})

    page = int(request.args.get("page", 1))
    print(page)
    limit = 10
    start = (page - 1) * limit
    end = page * limit if min(len(TrueCar), len(Craigslist)) > page * limit else min(len(TrueCar), len(Craigslist))
    pagination = Pagination(page=page, per_page=limit, total=min(len(TrueCar), len(Craigslist)), css_framework='bootstrap3')
    print(pagination.page)
    Craigslist = Craigslist[start: end]
    TrueCar = TrueCar[start: end]

    return render_template("compare.html", page = page, data = Craigslist, TrueCar=TrueCar, pagination=pagination)

@app.route('/filter.html', methods=['get'])
def filter():

    return render_template("filter.html")

@app.route('/index.html', methods=['get'])
def index_html():
    return render_template("index.html")
if __name__ == "__main__":
    # query()
    app.run(host='127.0.0.1', port=8080)