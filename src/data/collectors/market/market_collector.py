# Market Data Collector

import time
import json
import requests
from datetime import datetime
from ..base_collector import BaseCollector

class MarketCollector(BaseCollector):
    """
    市场数据采集器基类
    """

    def __init__(self, config=None):
        """
        初始化市场数据采集器

        Args:
            config: 配置参数，包含 API 密钥等
        """
        super().__init__(config)
        self.api_keys = config.get('api_keys', {})
        self.rate_limit_delay = config.get('rate_limit_delay', 1)

class CryptoMarketCollector(MarketCollector):
    """
    加密货币市场数据采集器
    """

    def __init__(self, config=None):
        """
        初始化加密货币市场采集器

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.data_source = "crypto_market"
        self.api_base_urls = {
            'binance': 'https://api.binance.com',
            'coinbase': 'https://api.coinbase.com/v2',
            'kraken': 'https://api.kraken.com/0',
            'coingecko': 'https://api.coingecko.com/api/v3'
        }

    def collect_price_data(self, symbol, exchange='binance', interval='1h', limit=100, **kwargs):
        """
        采集加密货币价格数据

        Args:
            symbol: 交易对符号
            exchange: 交易所
            interval: 时间间隔
            limit: 数据点数量
            **kwargs: 其他参数

        Returns:
            采集的价格数据
        """
        try:
            if exchange == 'binance':
                return self._collect_binance_price(symbol, interval, limit)
            elif exchange == 'coinbase':
                return self._collect_coinbase_price(symbol)
            elif exchange == 'kraken':
                return self._collect_kraken_price(symbol)
            elif exchange == 'coingecko':
                return self._collect_coingecko_price(symbol, days=limit)
            else:
                print(f"Unsupported exchange: {exchange}")
                return []

        except Exception as e:
            print(f"Error collecting crypto price data: {str(e)}")
            return []

    def collect_trading_volume(self, symbol, exchange='binance', **kwargs):
        """
        采集交易量数据

        Args:
            symbol: 交易对符号
            exchange: 交易所
            **kwargs: 其他参数

        Returns:
            采集的交易量数据
        """
        try:
            if exchange == 'binance':
                return self._collect_binance_volume(symbol)
            elif exchange == 'coingecko':
                return self._collect_coingecko_volume(symbol)
            else:
                print(f"Unsupported exchange: {exchange}")
                return {}

        except Exception as e:
            print(f"Error collecting trading volume: {str(e)}")
            return {}

    def collect_market_summary(self, symbols, **kwargs):
        """
        采集市场摘要数据

        Args:
            symbols: 交易对符号列表
            **kwargs: 其他参数

        Returns:
            采集的市场摘要数据
        """
        try:
            return self._collect_coingecko_market_summary(symbols)
        except Exception as e:
            print(f"Error collecting market summary: {str(e)}")
            return []

    def _collect_binance_price(self, symbol, interval, limit):
        """
        从 Binance 采集价格数据
        """
        url = f"{self.api_base_urls['binance']}/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Binance API error: {response.status_code} - {response.text}")
            return []

        data = response.json()

        # 转换数据格式
        price_data = []
        for item in data:
            price_data.append({
                'timestamp': item[0],
                'open': float(item[1]),
                'high': float(item[2]),
                'low': float(item[3]),
                'close': float(item[4]),
                'volume': float(item[5]),
                'quote_asset_volume': float(item[7]),
                'number_of_trades': int(item[8]),
                'exchange': 'binance',
                'symbol': symbol,
                'collected_at': datetime.utcnow().isoformat()
            })

        return price_data

    def _collect_coinbase_price(self, symbol):
        """
        从 Coinbase 采集价格数据
        """
        url = f"{self.api_base_urls['coinbase']}/prices/{symbol}/spot"

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Coinbase API error: {response.status_code} - {response.text}")
            return []

        data = response.json()

        # 转换数据格式
        price_data = [{
            'price': float(data['data']['amount']),
            'currency': data['data']['currency'],
            'exchange': 'coinbase',
            'symbol': symbol,
            'collected_at': datetime.utcnow().isoformat()
        }]

        return price_data

    def _collect_kraken_price(self, symbol):
        """
        从 Kraken 采集价格数据
        """
        url = f"{self.api_base_urls['kraken']}/public/Ticker"
        params = {
            'pair': symbol
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Kraken API error: {response.status_code} - {response.text}")
            return []

        data = response.json()

        if data['error']:
            print(f"Kraken API error: {data['error']}")
            return []

        # 转换数据格式
        price_data = []
        for pair, pair_data in data['result'].items():
            price_data.append({
                'symbol': pair,
                'ask': float(pair_data['a'][0]),
                'bid': float(pair_data['b'][0]),
                'last': float(pair_data['c'][0]),
                'high': float(pair_data['h'][0]),
                'low': float(pair_data['l'][0]),
                'volume': float(pair_data['v'][0]),
                'exchange': 'kraken',
                'collected_at': datetime.utcnow().isoformat()
            })

        return price_data

    def _collect_coingecko_price(self, symbol, days=7):
        """
        从 CoinGecko 采集价格数据
        """
        url = f"{self.api_base_urls['coingecko']}/coins/{symbol}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'hourly'
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"CoinGecko API error: {response.status_code} - {response.text}")
            return []

        data = response.json()

        # 转换数据格式
        price_data = []
        for i, timestamp in enumerate(data['prices']):
            price_data.append({
                'timestamp': timestamp[0],
                'price': timestamp[1],
                'volume': data['total_volumes'][i][1],
                'market_cap': data['market_caps'][i][1],
                'exchange': 'coingecko',
                'symbol': symbol,
                'collected_at': datetime.utcnow().isoformat()
            })

        return price_data

    def _collect_binance_volume(self, symbol):
        """
        从 Binance 采集交易量数据
        """
        url = f"{self.api_base_urls['binance']}/api/v3/ticker/24hr"
        params = {
            'symbol': symbol
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Binance API error: {response.status_code} - {response.text}")
            return {}

        data = response.json()

        # 转换数据格式
        volume_data = {
            'symbol': data['symbol'],
            'volume': float(data['volume']),
            'quote_volume': float(data['quoteVolume']),
            'price_change_percent': float(data['priceChangePercent']),
            'high_price': float(data['highPrice']),
            'low_price': float(data['lowPrice']),
            'open_price': float(data['openPrice']),
            'last_price': float(data['lastPrice']),
            'exchange': 'binance',
            'collected_at': datetime.utcnow().isoformat()
        }

        return volume_data

    def _collect_coingecko_volume(self, symbol):
        """
        从 CoinGecko 采集交易量数据
        """
        url = f"{self.api_base_urls['coingecko']}/coins/{symbol}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false',
            'sparkline': 'false'
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"CoinGecko API error: {response.status_code} - {response.text}")
            return {}

        data = response.json()

        # 转换数据格式
        market_data = data.get('market_data', {})
        volume_data = {
            'symbol': data.get('symbol', '').upper(),
            'name': data.get('name'),
            'current_price': market_data.get('current_price', {}).get('usd'),
            'market_cap': market_data.get('market_cap', {}).get('usd'),
            'total_volume': market_data.get('total_volume', {}).get('usd'),
            'high_24h': market_data.get('high_24h', {}).get('usd'),
            'low_24h': market_data.get('low_24h', {}).get('usd'),
            'price_change_24h': market_data.get('price_change_24h'),
            'price_change_percentage_24h': market_data.get('price_change_percentage_24h'),
            'exchange': 'coingecko',
            'collected_at': datetime.utcnow().isoformat()
        }

        return volume_data

    def _collect_coingecko_market_summary(self, symbols):
        """
        从 CoinGecko 采集市场摘要数据
        """
        url = f"{self.api_base_urls['coingecko']}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'ids': ','.join(symbols),
            'order': 'market_cap_desc',
            'per_page': 250,
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"CoinGecko API error: {response.status_code} - {response.text}")
            return []

        data = response.json()

        # 转换数据格式
        market_summary = []
        for item in data:
            market_summary.append({
                'id': item['id'],
                'symbol': item['symbol'].upper(),
                'name': item['name'],
                'current_price': item['current_price'],
                'market_cap': item['market_cap'],
                'market_cap_rank': item['market_cap_rank'],
                'total_volume': item['total_volume'],
                'high_24h': item['high_24h'],
                'low_24h': item['low_24h'],
                'price_change_24h': item['price_change_24h'],
                'price_change_percentage_24h': item['price_change_percentage_24h'],
                'market_cap_change_24h': item['market_cap_change_24h'],
                'market_cap_change_percentage_24h': item['market_cap_change_percentage_24h'],
                'circulating_supply': item['circulating_supply'],
                'total_supply': item['total_supply'],
                'max_supply': item['max_supply'],
                'exchange': 'coingecko',
                'collected_at': datetime.utcnow().isoformat()
            })

        return market_summary

    def collect(self, **kwargs):
        """
        通用采集方法

        Args:
            **kwargs: 采集参数

        Returns:
            采集的数据
        """
        if 'symbol' in kwargs:
            if 'data_type' in kwargs and kwargs['data_type'] == 'volume':
                return self.collect_trading_volume(kwargs['symbol'], **kwargs)
            elif 'data_type' in kwargs and kwargs['data_type'] == 'summary':
                return self.collect_market_summary([kwargs['symbol']], **kwargs)
            else:
                return self.collect_price_data(kwargs['symbol'], **kwargs)
        elif 'symbols' in kwargs:
            return self.collect_market_summary(kwargs['symbols'], **kwargs)
        else:
            print("No symbol or symbols provided")
            return []
