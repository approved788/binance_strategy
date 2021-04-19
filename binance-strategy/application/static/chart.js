var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 600,
  	height: 400,
	layout: {
		backgroundColor: '#F0F0F0',
		textColor: 'rgb(32, 32, 32)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: false,
	},
});

var areaSeries = chart.addAreaSeries({
    topColor: 'rgba(38, 198, 218, 0.56)',
    bottomColor: 'rgba(38, 198, 218, 0.04)',
    lineColor: 'rgba(38, 198, 218, 1)',
    lineWidth: 1,
    crossHairMarkerVisible: false,
});

var legend = document.createElement('div');
legend.classList.add('legend');
document.body.appendChild(legend);

var firstRow = document.createElement('div');
firstRow.innerText = 'BTC USDT M5 Test-Feed';
firstRow.style.color = 'black';
firstRow.style.marginTop = '4rem';
legend.appendChild(firstRow);

var candleSeries = chart.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000', 
	borderDownColor: 'rgba(255, 144, 0, 1)',
	borderUpColor: 'rgba(255, 144, 0, 1)',
	wickDownColor: 'rgba(255, 144, 0, 1)',
	wickUpColor: 'rgba(255, 144, 0, 1)',
});

fetch('http://127.0.0.1:5000/history')
	.then((r) => r.json())
	.then((response) => {
		console.log(response)

		candleSeries.setData(response);
	})

var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_5m");

binanceSocket.onmessage = function (event) {	
	var message = JSON.parse(event.data);

	var candlestick = message.k;

	console.log(candlestick)

	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}