# Traditional Finance Data Collector

import time
import json
import requests
from datetime import datetime
import pandas as pd
from ..base_collector import BaseCollector

class TraditionalFinanceCollector(BaseCollector):
    """
    传统金融数据采集器
    """

    def __init__(self, config=None):
        """
        初始化传统金融数据采集器

        Args:
            config: 配置参数，包含 API 密钥等
        """
        super().__init__(config)
        self.data_source = "traditional_finance"
        self.api_keys = config.get('api_keys', {})
        self.api_base_urls = {
            'fred': 'https://api.stlouisfed.org/fred',
            'alphavantage': 'https://www.alphavantage.co/query',
            'econdb': 'https://www.econdb.com/api/series'
        }

    def collect_macro_indicators(self, indicators=None, **kwargs):
        """
        采集宏观经济指标数据

        Args:
            indicators: 指标列表
            **kwargs: 其他参数

        Returns:
            采集的宏观经济指标数据
        """
        try:
            if indicators is None:
                indicators = ['GDP', 'CPI', 'UNRATE', 'FEDFUNDS']

            macro_data = []

            for indicator in indicators:
                if indicator in ['GDP', 'CPI', 'UNRATE', 'FEDFUNDS']:
                    data = self._collect_fred_data(indicator)
                    if data:
                        macro_data.extend(data)
                else:
                    print(f"Unsupported indicator: {indicator}")

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return macro_data

        except Exception as e:
            print(f"Error collecting macro indicators: {str(e)}")
            return []

    def collect_institutional_holdings(self, symbol, **kwargs):
        """
        采集机构持仓数据

        Args:
            symbol: 股票代码
            **kwargs: 其他参数

        Returns:
            采集的机构持仓数据
        """
        try:
            # 从 Alpha Vantage 采集机构持仓数据
            holdings_data = self._collect_alphavantage_holdings(symbol)

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return holdings_data

        except Exception as e:
            print(f"Error collecting institutional holdings: {str(e)}")
            return []

    def collect_market_sentiment(self, **kwargs):
        """
        采集市场情绪数据

        Args:
            **kwargs: 其他参数

        Returns:
            采集的市场情绪数据
        """
        try:
            # 从多种来源采集市场情绪数据
            sentiment_data = []

            # 采集 VIX 数据（恐慌指数）
            vix_data = self._collect_fred_data('VIXCLS')
            if vix_data:
                sentiment_data.extend(vix_data)

            # 采集 AAII 投资者情绪数据
            aaii_data = self._collect_aaii_sentiment()
            if aaii_data:
                sentiment_data.append(aaii_data)

            # 更新上次采集时间
            self.set_last_collected(datetime.utcnow().isoformat())

            return sentiment_data

        except Exception as e:
            print(f"Error collecting market sentiment: {str(e)}")
            return []

    def _collect_fred_data(self, series_id):
        """
        从 FRED (Federal Reserve Economic Data) 采集数据

        Args:
            series_id: 系列 ID

        Returns:
            采集的数据
        """
        try:
            fred_api_key = self.api_keys.get('fred_api_key')
            if not fred_api_key:
                # 如果没有 API 密钥，返回模拟数据
                return self._get_mock_fred_data(series_id)

            url = f"{self.api_base_urls['fred']}/series/observations"
            params = {
                'series_id': series_id,
                'api_key': fred_api_key,
                'file_type': 'json',
                'observation_start': '2020-01-01'
            }

            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"FRED API error: {response.status_code} - {response.text}")
                return []

            data = response.json()
            observations = data.get('observations', [])

            # 转换数据格式
            transformed_data = []
            for obs in observations:
                if obs.get('value') != '.':
                    transformed_data.append({
                        'indicator': series_id,
                        'date': obs.get('date'),
                        'value': float(obs.get('value')),
                        'source': 'fred',
                        'collected_at': datetime.utcnow().isoformat()
                    })

            return transformed_data

        except Exception as e:
            print(f"Error collecting FRED data: {str(e)}")
            return self._get_mock_fred_data(series_id)

    def _collect_alphavantage_holdings(self, symbol):
        """
        从 Alpha Vantage 采集机构持仓数据

        Args:
            symbol: 股票代码

        Returns:
            采集的机构持仓数据
        """
        try:
            alpha_api_key = self.api_keys.get('alphavantage_api_key')
            if not alpha_api_key:
                # 如果没有 API 密钥，返回模拟数据
                return self._get_mock_holdings_data(symbol)

            url = self.api_base_urls['alphavantage']
            params = {
                'function': 'INSTITUTIONAL_HOLDERS',
                'symbol': symbol,
                'apikey': alpha_api_key
            }

            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"Alpha Vantage API error: {response.status_code} - {response.text}")
                return []

            data = response.json()
            institutional_holders = data.get('institutionalHolders', [])

            # 转换数据格式
            transformed_data = []
            for holder in institutional_holders:
                transformed_data.append({
                    'symbol': symbol,
                    'holder': holder.get('holder'),
                    'shares': int(holder.get('shares').replace(',', '')),
                    'value': float(holder.get('value').replace(',', '')),
                    'percentage': float(holder.get('percentage').replace('%', '')),
                    'source': 'alphavantage',
                    'collected_at': datetime.utcnow().isoformat()
                })

            return transformed_data

        except Exception as e:
            print(f"Error collecting Alpha Vantage holdings: {str(e)}")
            return self._get_mock_holdings_data(symbol)

    def _collect_aaii_sentiment(self):
        """
        采集 AAII 投资者情绪数据

        Returns:
            采集的 AAII 投资者情绪数据
        """
        try:
            # 注意：AAII 可能没有公开的 API，这里使用模拟数据
            # 实际项目中可能需要使用网页抓取或第三方服务

            # 模拟数据
            sentiment_data = {
                'indicator': 'AAII_SENTIMENT',
                'bullish': 35.2,
                'bearish': 25.8,
                'neutral': 39.0,
                'source': 'aaii',
                'collected_at': datetime.utcnow().isoformat(),
                'date': datetime.now().strftime('%Y-%m-%d')
            }

            return sentiment_data

        except Exception as e:
            print(f"Error collecting AAII sentiment: {str(e)}")
            return {}

    def _get_mock_fred_data(self, series_id):
        """
        获取模拟的 FRED 数据

        Args:
            series_id: 系列 ID

        Returns:
            模拟数据
        """
        # 生成模拟数据
        mock_data = []
        base_value = 0

        if series_id == 'GDP':
            base_value = 20000
        elif series_id == 'CPI':
            base_value = 250
        elif series_id == 'UNRATE':
            base_value = 5
        elif series_id == 'FEDFUNDS':
            base_value = 2
        elif series_id == 'VIXCLS':
            base_value = 20

        # 生成过去 12 个月的数据
        for i in range(12):
            date = (datetime.now().replace(day=1) - pd.DateOffset(months=i)).strftime('%Y-%m-%d')
            # 添加一些随机波动
            value = base_value + (i % 5 - 2) * 0.5

            mock_data.append({
                'indicator': series_id,
                'date': date,
                'value': round(value, 2),
                'source': 'mock',
                'collected_at': datetime.utcnow().isoformat()
            })

        return mock_data

    def _get_mock_holdings_data(self, symbol):
        """
        获取模拟的机构持仓数据

        Args:
            symbol: 股票代码

        Returns:
            模拟数据
        """
        # 生成模拟数据
        mock_holders = [
            {'holder': 'Vanguard Group Inc.', 'shares': 12345678, 'value': 123456789.12, 'percentage': 8.5},
            {'holder': 'BlackRock Inc.', 'shares': 10987654, 'value': 109876543.21, 'percentage': 7.5},
            {'holder': 'State Street Corp.', 'shares': 8765432, 'value': 87654321.98, 'percentage': 6.0},
            {'holder': 'Fidelity Investments', 'shares': 7654321, 'value': 76543210.87, 'percentage': 5.2},
            {'holder': 'JP Morgan Chase & Co.', 'shares': 6543210, 'value': 65432109.76, 'percentage': 4.5}
        ]

        transformed_data = []
        for holder in mock_holders:
            transformed_data.append({
                'symbol': symbol,
                'holder': holder['holder'],
                'shares': holder['shares'],
                'value': holder['value'],
                'percentage': holder['percentage'],
                'source': 'mock',
                'collected_at': datetime.utcnow().isoformat()
            })

        return transformed_data

    def collect(self, **kwargs):
        """
        通用采集方法

        Args:
            **kwargs: 采集参数

        Returns:
            采集的数据
        """
        if 'indicators' in kwargs:
            return self.collect_macro_indicators(kwargs['indicators'])
        elif 'symbol' in kwargs:
            return self.collect_institutional_holdings(kwargs['symbol'])
        elif 'data_type' in kwargs and kwargs['data_type'] == 'sentiment':
            return self.collect_market_sentiment()
        else:
            print("No valid collection type specified")
            return []
