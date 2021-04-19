from flask import Flask, render_template, redirect, jsonify
from application import binanceclient
from application.forms import SysSettings
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mynewsecretkey'
app.config['CSRF_ENABLED'] = True

#   Main Page
@app.route('/', methods = ['GET'])
def index_page():
    page_title = 'Binance Demo Strategy'
    system = binanceclient.SystemClient('system')
    form = SysSettings()
    with open('application/static/data.json') as json_file:
        data = json.load(json_file)
    settinngs_json = data['sys_config'][-1]

    return render_template('index.html', title=page_title, system=system, form=form, old_set=settinngs_json)

@app.route('/settings', methods=['POST'])
def change_settings():
    form = SysSettings()
    if form.validate_on_submit():
        data = {}
        data['sys_config']=[]
        data['sys_config'].append({
            'ma_period':form.data['ma_period'],
            'ma_up':form.data['ma_up'],
            'ma_dn':form.data['ma_dn'],
            'risk':form.data['risk_vol']
        })
        with open('application/static/data.json', 'w') as outfile:
            json.dump(data, outfile)
        # return 'System parameters changed to new'
        return redirect('/')
    else:
        return '{}'.format(form.errors)

@app.route('/history')
def history():
    system = binanceclient.SystemClient('system')
    candlesticks = system.client.get_historical_klines("BTCUSDT", system.client.KLINE_INTERVAL_5MINUTE, "1 Apr, 2021", "15 Apr, 2022")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2], 
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)