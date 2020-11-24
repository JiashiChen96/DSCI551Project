from flask import Flask, render_template, request, session
from flask_paginate import Pagination

from Query.CraigslistQuery import query_craigslist
from Query.TrueCarQuery import query_TrueCar

app = Flask(__name__)
app.debug= False
app.secret_key = 'DSCI551'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/filter', methods=['get'])
def filter():
    return render_template("filter.html")

@app.route('/compare', methods=['get', 'post'])
def search():
    if request.method == "POST":
        filter = {}
        for k, v in request.form.to_dict().items():
            if v != "" and v != "Choose...":
                filter[k] = v
            else:
                filter[k] = ""
        session['filter'] = filter

    if request.method == "GET":
        filter = session['filter']
    print(filter)
    Craigslist = query_craigslist(filter)
    TrueCar = query_TrueCar(filter)
    print(Craigslist)
    print(TrueCar)
    if (len(Craigslist) == 0 or len(TrueCar) == 0):
        return render_template("error.html")

    page = int(request.args.get("page", 1))
    limit = 10
    start = (page - 1) * limit
    end = page * limit if min(len(TrueCar), len(Craigslist)) > page * limit else min(len(TrueCar), len(Craigslist))
    pagination = Pagination(page=page, per_page=limit, total=min(len(TrueCar), len(Craigslist)), css_framework='bootstrap3')
    Craigslist = Craigslist[start: end]
    TrueCar = TrueCar[start: end]

    print(Craigslist)
    print(TrueCar)

    return render_template("compare.html", filter = filter, page = page, data = Craigslist, TrueCar=TrueCar, pagination=pagination)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)