from flask import Flask, flash, redirect, render_template, request, session, abort
from get_stock_prices import get_price, get_many_prices, convert_price, convert_many_prices
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get_price")
@app.route("/get_many_prices")
def get_price_item_submit():
    return render_template('submit_item_form.html')


@app.route("/get_price", methods=['POST'])
def render_price():
    result = str(get_price(request.form['text']))
    return render_template('prices.html', result=result)


@app.route("/get_many_prices", methods=['POST'])
def render_price_list():
    result = str(get_many_prices(request.form['text']))
    return render_template('prices.html', result=result)


@app.route("/convert_price")
def render_convert_price():
    result = str(convert_price(1, 'USD', 'GBP'))
    return render_template('prices.html', result=result)


@app.route("/convert_many_prices")
def render_convert_price_list():
    result = str(convert_many_prices([{'price': 1, 'source_currency': 'USD', 'target_currency': 'GBP'},
          {'price': 10, 'source_currency': 'GBP', 'target_currency': 'USD'},
          {'price': 1, 'source_currency': 'USD', 'target_currency': 'EUR'}]))
    return render_template('prices.html', result=result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
