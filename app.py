from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination

from search import query, connectMongoDb

app = Flask(__name__)
# bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/compare', methods=['GET', 'POST'])
def search():
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


if __name__ == "__main__":
    # query()
    app.run(host='127.0.0.1', port=8080)