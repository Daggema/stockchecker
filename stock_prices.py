import requests, bs4


def get_price(item, type):
    if type == 'stock':
        page = requests.get('https://www.marketwatch.com/investing/stock/{}'.format(item.lower()))
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        selector = 'body > div.container.wrapper.clearfix.j-quoteContainer.stock > div.content-region.region--' \
                   'fixed > div.template.template--aside > div > div > div.intraday__data > h3 > bg-quote'
    elif type == 'crypto':
        page = requests.get('https://www.coingecko.com/en/price_charts/{}/usd'.format(item.lower()))
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        selector = '#wrapper > div.container.price_charts > div.coingecko.row > div > div.coin-details.row > ' \
                   'div.col-md-5.market-value > div.coin-value > span'
    elements = soup.select(selector)
    price = elements[0].text.strip()
    price = float(price.strip('$'))
    return price


def get_many_prices(dictionary):
    prices = {}
    for i in dictionary.items():
        prices[i[0]] = get_price(i[0], i[1])
    return prices


def convert_price(price, source_currency, target_currency):
    page = requests.get('http://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}'
                        .format(source_currency.lower(), target_currency.lower()))
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    elements = soup.select('#ucc-container > span.uccAmountWrap > span.uccResultAmount')
    conversion_rate = float(elements[0].text.strip())
    converted_price = price * conversion_rate
    return converted_price


def convert_many_prices(pricelist):
    converted_prices = {}
    for i in pricelist:
        converted_prices['{0} {1} to {2} conversion'.format(i['price'], i['source_currency'], i['target_currency'])] \
            = convert_price(i['price'], i['source_currency'], i['target_currency'])
    return converted_prices










'''items = {'AAPL': 'stock','ripple': 'crypto'}
itemlist = get_many_prices(items)

dollars = convert_price(1, 'USD', 'GBP')
#print(dollars)

prices = [{'price': 1, 'source_currency': 'USD', 'target_currency': 'GBP'},
          {'price': 10, 'source_currency': 'GBP', 'target_currency': 'USD'},
          {'price': 1, 'source_currency': 'USD', 'target_currency': 'EUR'}]

#print(convert_many_prices(prices))

print(get_price('AAPL', 'stock'))
print(convert_price(154.7, 'USD', 'GBP'))
convert_price(get_price('AAPL', 'stock'), 'USD', 'GBP')'''