from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination

from search import query

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/compare', methods=['GET', 'POST'])
def search():
    cars = query()
    limit = 5

    page = int(request.args.get("page", 1))
    start = (page - 1) * 5
    end = page * limit if len(cars) > page * limit else len(cars)
    pageinate = Pagination(page, total=len(cars))
    cars = cars[start: end]

    # print(cars)
    return render_template("compare.html", data = cars, paginate=pageinate)


if __name__ == "__main__":
    # query()
    app.run(host='127.0.0.1', port=8080)