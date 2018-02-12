from flask import Flask, flash, redirect, render_template, request, session, abort
from get_stock_prices import get_price, get_many_prices, convert_price, convert_many_prices
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


# GET PRICES ####################################################################


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


# CONVERT PRICES ################################################################


@app.route("/convert_price")
def get_price_submit():
    return render_template('submit_price_form.html')


@app.route("/convert_price", methods=['POST'])
def render_convert_price():
    print(request.form)
    result = str(convert_price(request.form['quantity'], request.form['source currency'],
                               request.form['target currency']))
    return render_template('prices.html', result=result)


@app.route("/convert_many_prices")
def get_multi_price_submit():
    return render_template('submit_multi_price_form.html')


@app.route("/convert_many_prices", methods=['POST'])
def render_convert_price_list():
    result = str(convert_many_prices(request.form))
    return render_template('prices.html', result=result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
