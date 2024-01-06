from csctracker_py_core.starter import Starter
from yahooquery import Ticker

starter = Starter()
app = starter.get_app()


@app.route('/price/<ticker>')
def global_price(ticker):
    ticker_info = Ticker(ticker.upper(), country='brazil')
    price = ticker_info.price[ticker]
    ret = {
        'price': price
    }
    return ret


@app.route('/price-br/<ticker>')
def br_price(ticker):
    ticker_info = Ticker(ticker.upper() + ".SA", country='brazil')
    price = ticker_info.price[ticker + '.SA']
    ret = {
        'price': price
    }
    return ret


@app.route('/info-br/<ticker>')
def br_info(ticker):
    ticker_info = Ticker(ticker.upper() + ".SA", country='brazil')
    summary = ticker_info.summary_detail[ticker + '.SA']
    price = ticker_info.price[ticker + '.SA']
    ret = {
        'summary': summary,
        'price': price,
        'financial_data': ticker_info.financial_data[ticker + '.SA'],
        'key_stats': ticker_info.key_stats[ticker + '.SA']
    }
    return ret


@app.route('/info/<ticker>')
def global_info(ticker):
    ticker_info = Ticker(ticker.upper(), country='brazil')
    summary = ticker_info.summary_detail[ticker]
    price = ticker_info.price[ticker]
    ret = {
        'summary': summary,
        'price': price,
        'financial_data': ticker_info.financial_data[ticker],
        'key_stats': ticker_info.key_stats[ticker]
    }
    return ret


@app.route('/prices/<ticker>/<period>/<interval>')
def global_prices(ticker, period, interval):
    ticker_info = Ticker(ticker.upper(), country='brazil')
    ticker_info = ticker_info.history(period=period, interval=interval)
    return ticker_info['open'].to_json(orient="table"), 200, {'Content-Type': 'application/json'}


@app.route('/prices-br/<ticker>/<period>/<interval>')
def br_prices(ticker, period, interval):
    ticker_info = Ticker(ticker.upper() + ".SA", country='brazil')
    ticker_info = ticker_info.history(period=period, interval=interval)
    return ticker_info['open'].to_json(orient="table"), 200, {'Content-Type': 'application/json'}


starter.start()
