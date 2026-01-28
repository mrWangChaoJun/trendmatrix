# Data Processor Module

import pandas as pd
import numpy as np
from datetime import datetime
import json

class DataProcessor:
    """
    数据处理器基类
    """

    def __init__(self, config=None):
        """
        初始化数据处理器

        Args:
            config: 配置参数
        """
        self.config = config or {}

    def process(self, data):
        """
        处理数据的核心方法，子类必须实现

        Args:
            data: 原始数据

        Returns:
            处理后的数据
        """
        raise NotImplementedError("Subclass must implement process method")

    def validate(self, data):
        """
        验证数据

        Args:
            data: 数据

        Returns:
            bool: 数据是否有效
        """
        if data is None or len(data) == 0:
            return False
        return True

class SocialMediaProcessor(DataProcessor):
    """
    社交媒体数据处理器
    """

    def process(self, data):
        """
        处理社交媒体数据

        Args:
            data: 原始社交媒体数据

        Returns:
            处理后的社交媒体数据
        """
        if not self.validate(data):
            return []

        processed_data = []

        for item in data:
            # 清洗文本数据
            cleaned_text = self._clean_text(item.get('text', '') or item.get('content', ''))

            # 提取特征
            features = {
                'text_length': len(cleaned_text),
                'word_count': len(cleaned_text.split()),
                'has_url': self._has_url(cleaned_text),
                'has_mention': self._has_mention(cleaned_text),
                'has_hashtag': self._has_hashtag(cleaned_text)
            }

            # 处理时间数据
            timestamp = self._process_timestamp(item)

            # 合并数据
            processed_item = {
                **item,
                'cleaned_text': cleaned_text,
                'features': features,
                'processed_timestamp': timestamp
            }

            processed_data.append(processed_item)

        return processed_data

    def _clean_text(self, text):
        """
        清洗文本

        Args:
            text: 原始文本

        Returns:
            清洗后的文本
        """
        if not text:
            return ''

        # 移除多余的空白字符
        text = ' '.join(text.split())
        # 移除特殊字符
        text = ''.join(e for e in text if e.isalnum() or e.isspace() or e in ['@', '#', '!', '?', '.', ','])

        return text.strip()

    def _has_url(self, text):
        """
        检查文本是否包含 URL

        Args:
            text: 文本

        Returns:
            bool: 是否包含 URL
        """
        import re
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return bool(url_pattern.search(text))

    def _has_mention(self, text):
        """
        检查文本是否包含 @ 提及

        Args:
            text: 文本

        Returns:
            bool: 是否包含 @ 提及
        """
        return '@' in text

    def _has_hashtag(self, text):
        """
        检查文本是否包含 # 标签

        Args:
            text: 文本

        Returns:
            bool: 是否包含 # 标签
        """
        return '#' in text

    def _process_timestamp(self, item):
        """
        处理时间戳

        Args:
            item: 数据项

        Returns:
            处理后的时间戳
        """
        timestamp = item.get('created_at')

        if isinstance(timestamp, str):
            try:
                # 尝试解析不同格式的时间戳
                if 'T' in timestamp:
                    return datetime.fromisoformat(timestamp).timestamp()
                else:
                    return datetime.strptime(timestamp, '%Y-%m-%d').timestamp()
            except:
                pass
        elif isinstance(timestamp, int):
            # 检查是否是 Unix 时间戳
            if timestamp > 1000000000:
                return timestamp

        return None

class BlockchainProcessor(DataProcessor):
    """
    区块链数据处理器
    """

    def process(self, data):
        """
        处理区块链数据

        Args:
            data: 原始区块链数据

        Returns:
            处理后的区块链数据
        """
        if not self.validate(data):
            return []

        processed_data = []

        for item in data:
            # 处理交易数据
            if 'signature' in item:
                processed_item = self._process_transaction(item)
            # 处理账户数据
            elif 'pubkey' in item:
                processed_item = self._process_account(item)
            # 处理代币持有者数据
            elif 'address' in item and 'amount' in item:
                processed_item = self._process_token_holder(item)
            else:
                processed_item = item

            processed_data.append(processed_item)

        return processed_data

    def _process_transaction(self, tx):
        """
        处理交易数据

        Args:
            tx: 交易数据

        Returns:
            处理后的交易数据
        """
        # 计算交易特征
        features = {
            'has_memo': tx.get('memo') is not None,
            'instruction_count': len(tx.get('instructions', [])),
            'has_error': tx.get('err') is not None
        }

        # 处理时间数据
        block_time = tx.get('block_time')

        return {
            **tx,
            'features': features,
            'processed_block_time': block_time
        }

    def _process_account(self, account):
        """
        处理账户数据

        Args:
            account: 账户数据

        Returns:
            处理后的账户数据
        """
        # 计算账户特征
        features = {
            'is_executable': account.get('executable', False),
            'data_size_kb': account.get('data_length', 0) / 1024
        }

        return {
            **account,
            'features': features
        }

    def _process_token_holder(self, holder):
        """
        处理代币持有者数据

        Args:
            holder: 持有者数据

        Returns:
            处理后的持有者数据
        """
        # 计算持有者特征
        features = {
            'amount_normalized': holder.get('amount', 0) / 10**9  # 假设是 SOL 或类似代币
        }

        return {
            **holder,
            'features': features
        }

class MarketDataProcessor(DataProcessor):
    """
    市场数据处理器
    """

    def process(self, data):
        """
        处理市场数据

        Args:
            data: 原始市场数据

        Returns:
            处理后的市场数据
        """
        if not self.validate(data):
            return []

        processed_data = []

        for item in data:
            # 处理价格数据
            if 'price' in item or 'close' in item:
                processed_item = self._process_price_data(item)
            # 处理交易量数据
            elif 'volume' in item:
                processed_item = self._process_volume_data(item)
            else:
                processed_item = item

            processed_data.append(processed_item)

        return processed_data

    def _process_price_data(self, price_data):
        """
        处理价格数据

        Args:
            price_data: 价格数据

        Returns:
            处理后的价格数据
        """
        # 计算价格特征
        features = {}

        # 计算价格变化
        if 'open' in price_data and 'close' in price_data:
            open_price = price_data.get('open')
            close_price = price_data.get('close')
            if open_price and close_price:
                features['price_change'] = close_price - open_price
                features['price_change_percent'] = ((close_price - open_price) / open_price) * 100
                features['is_positive'] = features['price_change'] > 0

        # 计算波动性
        if 'high' in price_data and 'low' in price_data:
            high = price_data.get('high')
            low = price_data.get('low')
            if high and low:
                features['volatility'] = high - low
                features['volatility_percent'] = ((high - low) / ((high + low) / 2)) * 100

        # 处理时间数据
        timestamp = self._process_timestamp(price_data)

        return {
            **price_data,
            'features': features,
            'processed_timestamp': timestamp
        }

    def _process_volume_data(self, volume_data):
        """
        处理交易量数据

        Args:
            volume_data: 交易量数据

        Returns:
            处理后的交易量数据
        """
        # 计算交易量特征
        features = {}

        # 处理时间数据
        timestamp = self._process_timestamp(volume_data)

        return {
            **volume_data,
            'features': features,
            'processed_timestamp': timestamp
        }

    def _process_timestamp(self, data):
        """
        处理时间戳

        Args:
            data: 数据

        Returns:
            处理后的时间戳
        """
        # 尝试从不同字段获取时间戳
        timestamp_fields = ['timestamp', 'block_time', 'date', 'created_at']

        for field in timestamp_fields:
            if field in data:
                value = data[field]

                if isinstance(value, int):
                    # 检查是否是 Unix 时间戳
                    if value > 1000000000:
                        return value
                elif isinstance(value, str):
                    try:
                        # 尝试解析 ISO 格式时间
                        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        return dt.timestamp()
                    except:
                        pass

        return None

class TraditionalFinanceProcessor(DataProcessor):
    """
    传统金融数据处理器
    """

    def process(self, data):
        """
        处理传统金融数据

        Args:
            data: 原始传统金融数据

        Returns:
            处理后的传统金融数据
        """
        if not self.validate(data):
            return []

        processed_data = []

        for item in data:
            # 处理宏观经济指标
            if 'indicator' in item:
                processed_item = self._process_macro_indicator(item)
            # 处理机构持仓数据
            elif 'holder' in item:
                processed_item = self._process_institutional_holding(item)
            else:
                processed_item = item

            processed_data.append(processed_item)

        return processed_data

    def _process_macro_indicator(self, indicator):
        """
        处理宏观经济指标

        Args:
            indicator: 宏观经济指标

        Returns:
            处理后的宏观经济指标
        """
        # 处理时间数据
        timestamp = self._process_timestamp(indicator)

        return {
            **indicator,
            'processed_timestamp': timestamp
        }

    def _process_institutional_holding(self, holding):
        """
        处理机构持仓数据

        Args:
            holding: 机构持仓数据

        Returns:
            处理后的机构持仓数据
        """
        # 计算持仓特征
        features = {}

        # 处理百分比数据
        if 'percentage' in holding:
            features['percentage_normalized'] = holding['percentage'] / 100

        return {
            **holding,
            'features': features
        }

    def _process_timestamp(self, data):
        """
        处理时间戳

        Args:
            data: 数据

        Returns:
            处理后的时间戳
        """
        # 尝试从不同字段获取时间戳
        date_fields = ['date', 'observation_date', 'created_at']

        for field in date_fields:
            if field in data:
                value = data[field]

                if isinstance(value, str):
                    try:
                        # 尝试解析日期格式
                        dt = datetime.strptime(value, '%Y-%m-%d')
                        return dt.timestamp()
                    except:
                        pass

        return None
