from flask import Flask, flash, redirect, render_template, request, session, abort
from get_stock_prices import get_price, get_many_prices, convert_price, convert_many_prices
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


# GET PRICES ####################################################################


@app.route("/get_price")
def get_price_item_submit():
    return render_template('submit_item_form.html')


@app.route("/get_price", methods=['POST'])
def render_price():
    result = get_price(request.form['text'])
    if result == '404 - page not found':
        return render_template('404.html', missing_items=request.form['text'])
    else:
        return render_template('prices.html', result=result)


@app.route("/get_many_prices")
def get_multi_price_item_submit():
    return render_template('submit_multi_items_form.html')


@app.route("/get_many_prices", methods=['POST'])
def render_price_list():
    missing_items = []
    result = get_many_prices(request.form['text'])
    for i in result.items():
        if i[1] == '404 - page not found':
            missing_items.append(i)
    if len(missing_items) > 0:
        return render_template('404.html', missing_items=missing_items)
    else:
        return render_template('prices.html', result=result)


# CONVERT PRICES ################################################################


@app.route("/convert_price")
def get_price_submit():
    return render_template('submit_price_form.html')


@app.route("/convert_price", methods=['POST'])
def render_convert_price():
    print(request.form)
    result = convert_price(request.form['quantity'], request.form['source currency'],
                           request.form['target currency'])
    if result == '404 - page not found':
        return render_template('404.html', missing_items=request.form)
    else:
        return render_template('convert_price.html', result=result)


@app.route("/convert_many_prices")
def get_multi_price_submit():
    return render_template('submit_multi_price_form.html')


@app.route("/convert_many_prices", methods=['POST'])
def render_convert_price_list():
    missing_items = []
    result = convert_many_prices(request.form)
    for i in result.items():
        if i[1] == '404 - page not found':
            missing_items.append(i)
    if len(missing_items) > 0:
        return render_template('404.html', missing_items=missing_items)
    else:
        return render_template('convert_price.html', result=result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
