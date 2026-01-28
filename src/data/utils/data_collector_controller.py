# Data Collector Controller

import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..collectors.social.social_media_collector import XCollector, TelegramCollector, DiscordCollector
from ..collectors.blockchain.solana_collector import SolanaCollector
from ..collectors.market.market_collector import CryptoMarketCollector
from ..collectors.traditional.traditional_finance_collector import TraditionalFinanceCollector

from ..processors.data_processor import (
    SocialMediaProcessor,
    BlockchainProcessor,
    MarketDataProcessor,
    TraditionalFinanceProcessor
)

from ..storage.data_storage import StorageManager

class DataCollectorController:
    """
    数据采集控制器
    """

    def __init__(self, config=None):
        """
        初始化数据采集控制器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 初始化采集器
        self.collectors = self._init_collectors()

        # 初始化处理器
        self.processors = self._init_processors()

        # 初始化存储管理器
        self.storage_manager = StorageManager(config)

        # 初始化线程池
        self.executor = ThreadPoolExecutor(max_workers=10)

    def _init_collectors(self):
        """
        初始化采集器

        Returns:
            采集器字典
        """
        collectors = {
            'x': XCollector(self.config),
            'telegram': TelegramCollector(self.config),
            'discord': DiscordCollector(self.config),
            'solana': SolanaCollector(self.config),
            'crypto_market': CryptoMarketCollector(self.config),
            'traditional_finance': TraditionalFinanceCollector(self.config)
        }
        return collectors

    def _init_processors(self):
        """
        初始化处理器

        Returns:
            处理器字典
        """
        processors = {
            'social_media': SocialMediaProcessor(self.config),
            'blockchain': BlockchainProcessor(self.config),
            'market': MarketDataProcessor(self.config),
            'traditional_finance': TraditionalFinanceProcessor(self.config)
        }
        return processors

    def collect_social_media_data(self, platforms=None, queries=None, **kwargs):
        """
        采集社交媒体数据

        Args:
            platforms: 平台列表
            queries: 查询列表
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        if platforms is None:
            platforms = ['x', 'telegram', 'discord']

        if queries is None:
            queries = ['cryptocurrency', 'solana', 'nft']

        collected_data = []
        futures = []

        # 提交采集任务
        for platform in platforms:
            if platform not in self.collectors:
                self.logger.warning(f"Unsupported platform: {platform}")
                continue

            collector = self.collectors[platform]

            for query in queries:
                if platform == 'x':
                    future = self.executor.submit(
                        collector.collect,
                        query=query,
                        max_results=kwargs.get('max_results', 50)
                    )
                    futures.append((future, platform))
                elif platform == 'telegram':
                    # 需要频道 ID
                    channel_id = kwargs.get('telegram_channel_id', '@trendsnewsEN')
                    future = self.executor.submit(
                        collector.collect,
                        channel_id=channel_id,
                        limit=kwargs.get('max_results', 50)
                    )
                    futures.append((future, platform))
                elif platform == 'discord':
                    # 需要频道 ID
                    channel_id = kwargs.get('discord_channel_id')
                    if channel_id:
                        future = self.executor.submit(
                            collector.collect,
                            channel_id=channel_id,
                            limit=kwargs.get('max_results', 50)
                        )
                        futures.append((future, platform))

        # 收集结果
        for future, platform in futures:
            try:
                data = future.result()
                if data:
                    # 处理数据
                    processed_data = self.processors['social_media'].process(data)
                    collected_data.extend(processed_data)

                    # 存储数据
                    self.storage_manager.store(
                        processed_data,
                        storage_type='mongodb',
                        collection=f'social_media_{platform}'
                    )

            except Exception as e:
                self.logger.error(f"Error collecting {platform} data: {str(e)}")

        return collected_data

    def collect_blockchain_data(self, chain='solana', **kwargs):
        """
        采集区块链数据

        Args:
            chain: 区块链
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        collected_data = []

        if chain == 'solana':
            collector = self.collectors['solana']

            # 采集交易数据
            if 'address' in kwargs:
                transactions = collector.collect_transactions(
                    kwargs['address'],
                    limit=kwargs.get('limit', 100)
                )
                if transactions:
                    processed_transactions = self.processors['blockchain'].process(transactions)
                    collected_data.extend(processed_transactions)

                    # 存储数据
                    self.storage_manager.store(
                        processed_transactions,
                        storage_type='mongodb',
                        collection='solana_transactions'
                    )

            # 采集代币持有者数据
            if 'mint_address' in kwargs:
                holders = collector.collect_token_holders(
                    kwargs['mint_address'],
                    limit=kwargs.get('limit', 1000)
                )
                if holders:
                    processed_holders = self.processors['blockchain'].process(holders)
                    collected_data.extend(processed_holders)

                    # 存储数据
                    self.storage_manager.store(
                        processed_holders,
                        storage_type='mongodb',
                        collection='solana_token_holders'
                    )

        return collected_data

    def collect_market_data(self, symbols=None, **kwargs):
        """
        采集市场数据

        Args:
            symbols: 交易对符号列表
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        if symbols is None:
            symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']

        collected_data = []
        futures = []

        collector = self.collectors['crypto_market']

        # 提交采集任务
        for symbol in symbols:
            # 采集价格数据
            future = self.executor.submit(
                collector.collect_price_data,
                symbol=symbol,
                exchange=kwargs.get('exchange', 'binance'),
                interval=kwargs.get('interval', '1h'),
                limit=kwargs.get('limit', 100)
            )
            futures.append((future, 'price', symbol))

            # 采集交易量数据
            future = self.executor.submit(
                collector.collect_trading_volume,
                symbol=symbol,
                exchange=kwargs.get('exchange', 'binance')
            )
            futures.append((future, 'volume', symbol))

        # 收集结果
        for future, data_type, symbol in futures:
            try:
                data = future.result()
                if data:
                    # 处理数据
                    processed_data = self.processors['market'].process(data)
                    collected_data.extend(processed_data)

                    # 存储数据
                    self.storage_manager.store(
                        processed_data,
                        storage_type='timescaledb',
                        table=f'crypto_{data_type}'
                    )

            except Exception as e:
                self.logger.error(f"Error collecting {data_type} data for {symbol}: {str(e)}")

        return collected_data

    def collect_traditional_finance_data(self, indicators=None, symbols=None, **kwargs):
        """
        采集传统金融数据

        Args:
            indicators: 指标列表
            symbols: 股票代码列表
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        collected_data = []

        collector = self.collectors['traditional_finance']

        # 采集宏观经济指标
        if indicators:
            macro_data = collector.collect_macro_indicators(indicators)
            if macro_data:
                processed_macro_data = self.processors['traditional_finance'].process(macro_data)
                collected_data.extend(processed_macro_data)

                # 存储数据
                self.storage_manager.store(
                    processed_macro_data,
                    storage_type='timescaledb',
                    table='macro_indicators'
                )

        # 采集机构持仓数据
        if symbols:
            for symbol in symbols:
                holdings_data = collector.collect_institutional_holdings(symbol)
                if holdings_data:
                    processed_holdings_data = self.processors['traditional_finance'].process(holdings_data)
                    collected_data.extend(processed_holdings_data)

                    # 存储数据
                    self.storage_manager.store(
                        processed_holdings_data,
                        storage_type='mongodb',
                        collection='institutional_holdings'
                    )

        return collected_data

    def run_full_collection(self, **kwargs):
        """
        运行完整的数据采集

        Args:
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        self.logger.info("Starting full data collection")
        start_time = time.time()

        # 并行运行所有采集任务
        futures = []

        # 社交媒体数据
        futures.append(self.executor.submit(
            self.collect_social_media_data,
            **kwargs
        ))

        # 区块链数据
        if 'solana_address' in kwargs:
            futures.append(self.executor.submit(
                self.collect_blockchain_data,
                chain='solana',
                address=kwargs['solana_address'],
                **kwargs
            ))

        # 市场数据
        futures.append(self.executor.submit(
            self.collect_market_data,
            **kwargs
        ))

        # 传统金融数据
        futures.append(self.executor.submit(
            self.collect_traditional_finance_data,
            indicators=['GDP', 'CPI', 'UNRATE', 'FEDFUNDS'],
            **kwargs
        ))

        # 收集结果
        collected_data = []
        for future in as_completed(futures):
            try:
                data = future.result()
                if data:
                    collected_data.extend(data)
            except Exception as e:
                self.logger.error(f"Error in full collection: {str(e)}")

        elapsed_time = time.time() - start_time
        self.logger.info(f"Full data collection completed in {elapsed_time:.2f} seconds")

        return collected_data

    def close(self):
        """
        关闭控制器
        """
        # 关闭线程池
        self.executor.shutdown(wait=True)

        # 关闭存储管理器
        self.storage_manager.close()

        self.logger.info("Data collector controller closed")
