import requests, bs4

def get_price(string):
    page = requests.get('https://www.marketwatch.com/investing/stock/{}'.format(string.lower()))
    if 'lookup' in page.url:
        page = requests.get('https://www.coingecko.com/en/price_charts/{}/usd'.format(string.lower()))
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        selector = '#wrapper > div.container.price_charts > div.coingecko.row > div > div.coin-details.row > ' \
                   'div.col-md-5.market-value > div.coin-value > span'
    else:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        selector = 'body > div.container.wrapper.clearfix.j-quoteContainer.stock > div.content-region.region--' \
                   'fixed > div.template.template--aside > div > div > div.intraday__data > h3 > bg-quote'

    if page.status_code == 404 or 'lookup' in page.url:
        return '404 - page not found'
    else:
        elements = soup.select(selector)
        if len(elements) == 0:
            return page.url
        price = elements[0].text.strip()
        price = price.replace(',', '')
        price = float(price.strip('$'))
    return price


def get_many_prices(string):
    items = _splitstring(string)
    return {i: get_price(i) for i in items}


def convert_price(price, source_currency, target_currency):
    page = requests.get('http://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}'
                        .format(source_currency.lower(), target_currency.lower()))
    if page.status_code == 404:
        return '404 - page not found'
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    check_converter = soup.select('#content > div.module.clearfix.quickFixesTopModule.clearfix > '
                            'div.uccResultContainer.quickFixesTopModule-left > h1')
    if str(check_converter[0]) == '<h1>XE Currency Converter: USD to USD</h1>':
        return '404 - page not found'
    elements = soup.select('#ucc-container > span.uccAmountWrap > span.uccResultAmount')
    conversion_rate = float(elements[0].text.strip())
    converted_price = float(price) * conversion_rate
    return converted_price


def convert_many_prices(price_dict):
    converted_prices = {}
    quantities = price_dict['quantities']
    sources = price_dict['sources']
    targets = price_dict['targets']
    args = zip(_splitstring(quantities), _splitstring(sources), _splitstring(targets))
    for i in args:
        converted_prices['{0} {1} to {2} conversion'.format(i[0], i[1], i[2])] = convert_price(i[0], i[1], i[2])
    return converted_prices


def _splitstring(string):
    if ',' in string:
        return string.split(', ')
    else:
        return string.split()
