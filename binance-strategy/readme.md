# Description
Welcome to Binance Auto MA Bot !

This project include Binance Automated Bot Algorithm and web interface to interact with him.
Point is that you can run bot 24/7 and control him from web interface of when to trade and what parameter`s must be used.

Currently bot can trade only BTC-USDT pair on M5 TimeFrame.
Bot parameters:
```
1. MA Period
2. MA Up
3. MA Dn
4. Risk
```
## Screenshot
Below is screenshot of web interface that you must see.

P.S. Feed chart is looking strange, because binance gives test-feed like you see :)

![Alt text](application/static/Web-interface.png?raw=true)

System signal was created on Simple Moving Average, constructed on bid close prices,
channel is simply distance measured in raw price-points of BTCUSDT, risk is measured in fixed amount.

Latest orders you can find in a table bottom.

# Installation
Kindly reminder!

You need API KEY and API SECRET KEY from your binance account to execute trades.

## Configure
Set up your keys and choose trading environment from live to demo in config.py
When you done with it, change the socket string in file chart.js, according to chosen in config:

```JavaScript
var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_5m");
```

You can open this file using grip:
```bash
grip -b readme.md
```

## Installation steps

1. Install python 3.9.2

2. Create virtual_env
    ```bash
    python3 -m venv env
    ```

3. Activate virtual environment

    PROJECT_DIR == is your project folder.

    ```bash
    source PROJECT_DIR/env/bin/activate
    ```

4. Install packages from requirements.txt
    ```Python
    pip3 install -r requirements.txt
    ```

# Launch

1. First run strategy:

```bash
cd application/python3 mastrategy.py
```

2. Then launch flask app:

```bash
python3 runserver.py
```
