import threading

from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from yahooquery import Ticker

from service.LoadBalancerRegister import LoadBalancerRegister

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

metrics = PrometheusMetrics(app, group_by='endpoint')

balancer = LoadBalancerRegister()


def schedule_job():
    balancer.register_service('yahoofinance')


t1 = threading.Thread(target=schedule_job, args=())
t1.start()


@app.route('/price/<ticker>')
def global_price(ticker):
    ticker_info = Ticker(ticker.upper())
    summary = ticker_info.summary_detail[ticker]
    price = ticker_info.price[ticker]
    ret = {
        'price': price
    }
    ticker_info = ticker_info.history(period='1d', interval="15m")
    return ret


@app.route('/price-br/<ticker>')
def br_price(ticker):
    ticker_info = Ticker(ticker.upper() + ".SA")
    summary = ticker_info.summary_detail[ticker + '.SA']
    price = ticker_info.price[ticker + '.SA']
    ret = {
        'price': price
    }
    return ret

@app.route('/info-br/<ticker>')
def br_info(ticker):
    ticker_info = Ticker(ticker.upper() + ".SA")
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
    ticker_info = Ticker(ticker.upper())
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
    ticker_info = Ticker(ticker.upper())
    ticker_info = ticker_info.history(period=period, interval=interval)
    return ticker_info['open'].to_json(orient="table"), 200, {'Content-Type': 'application/json'}


@app.route('/prices-br/<ticker>/<period>/<interval>')
def br_prices(ticker, period, interval):
    ticker_info = Ticker(ticker.upper() + ".SA")
    ticker_info = ticker_info.history(period=period, interval=interval)
    return ticker_info['open'].to_json(orient="table"), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
