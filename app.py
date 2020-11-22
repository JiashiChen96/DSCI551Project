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
    print("*****************************************")
    print(request.get_json(force=True).get("city"))
    return request.get_json(force=True),200

    Craigslist = query()
    TrueCar = connectMongoDb()
    limit = 10
    
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(Craigslist) > page * limit else len(Craigslist)
    pagination = Pagination(page, per_page=10,total=len(Craigslist), css_framework='bootstrap4')
    Craigslist = Craigslist[start: end]
    TrueCar = TrueCar[start: end]

    # print(cars)
    return render_template("compare.html", data = Craigslist, TrueCar=TrueCar, pagination=pagination)

@app.route('/filter.html', methods=['get'])
def filter():
    return render_template("filter.html")

@app.route('/index.html', methods=['get'])
def index_html():
    return render_template("index.html")
if __name__ == "__main__":
    # query()
    app.run(host='127.0.0.1', port=8080)