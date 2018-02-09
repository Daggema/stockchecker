from flask import Flask, flash, redirect, render_template, request, session, abort
from stock_prices import get_price, get_many_prices, convert_price, convert_many_prices

app = Flask(__name__)


@app.route("/get_price")
def render_price():
    result = str(get_price('AAPL', 'stock'))
    return render_template('index.html', result=result)


@app.route("/get_many_prices")
def render_price_list():
    result = str(get_many_prices({'AAPL': 'stock','ripple': 'crypto'}))
    return render_template('index.html', result=result)

@app.route("/convert_price")
def render_convert_price():
    return str(convert_price(1, 'USD', 'GBP'))


@app.route("/convert_many_prices")
def render_convert_price_list():
    return str(convert_many_prices([{'price': 1, 'source_currency': 'USD', 'target_currency': 'GBP'},
          {'price': 10, 'source_currency': 'GBP', 'target_currency': 'USD'},
          {'price': 1, 'source_currency': 'USD', 'target_currency': 'EUR'}]))


@app.route("/hello/<string:name>/")
def hello(name):
    return render_template(
        'index.html', name=name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)