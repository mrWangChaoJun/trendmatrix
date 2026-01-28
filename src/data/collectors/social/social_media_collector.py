# Social Media Data Collector

import time
import json
import requests
from datetime import datetime
from ..base_collector import BaseCollector

class SocialMediaCollector(BaseCollector):
    """
    社交媒体数据采集器基类
    """

    def __init__(self, config=None):
        """
        初始化社交媒体采集器

        Args:
            config: 配置参数，包含 API 密钥等
        """
        super().__init__(config)
        self.api_keys = config.get('api_keys', {})
        self.rate_limit_delay = config.get('rate_limit_delay', 1)

    def handle_rate_limit(self, response):
        """
        处理 API 速率限制

        Args:
            response: API 响应对象
        """
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting for {retry_after} seconds...")
            time.sleep(retry_after)
            return True
        return False

class XCollector(SocialMediaCollector):
    """
    X (原 Twitter) 数据采集器
    """

    def __init__(self, config=None):
        """
        初始化 X 采集器

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.data_source = "x"
        self.api_base_url = "https://api.x.com/2"

    def collect(self, query, max_results=100, **kwargs):
        """
        采集 X 平台上的趋势数据

        Args:
            query: 搜索关键词
            max_results: 最大结果数
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        bearer_token = self.api_keys.get('x_bearer_token')
        if not bearer_token:
            raise ValueError("X bearer token not provided")

        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        # 构建请求参数
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,text,author_id",
            "user.fields": "username,name,public_metrics",
            "expansions": "author_id"
        }

        # 发送请求
        url = f"{self.api_base_url}/tweets/search/recent"
        response = requests.get(url, headers=headers, params=params)

        # 处理速率限制
        if self.handle_rate_limit(response):
            response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error collecting X data: {response.status_code} - {response.text}")
            return []

        # 处理响应数据
        data = response.json()
        tweets = data.get('data', [])
        includes = data.get('includes', {})
        users = includes.get('users', [])

        # 转换数据格式
        transformed_data = []
        for tweet in tweets:
            user_id = tweet.get('author_id')
            user = next((u for u in users if u.get('id') == user_id), {})

            transformed_data.append({
                'id': tweet.get('id'),
                'text': tweet.get('text'),
                'created_at': tweet.get('created_at'),
                'author': {
                    'id': user_id,
                    'username': user.get('username'),
                    'name': user.get('name')
                },
                'metrics': tweet.get('public_metrics', {}),
                'source': 'x',
                'collected_at': datetime.utcnow().isoformat()
            })

        # 更新上次采集时间
        self.set_last_collected(datetime.utcnow().isoformat())

        return transformed_data

class TelegramCollector(SocialMediaCollector):
    """
    Telegram 数据采集器
    """

    def __init__(self, config=None):
        """
        初始化 Telegram 采集器

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.data_source = "telegram"
        self.api_base_url = "https://api.telegram.org/bot"

    def collect(self, channel_id, limit=100, **kwargs):
        """
        采集 Telegram 频道数据

        Args:
            channel_id: 频道 ID
            limit: 最大消息数
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        bot_token = self.api_keys.get('telegram_bot_token')
        if not bot_token:
            raise ValueError("Telegram bot token not provided")

        # 构建请求 URL
        url = f"{self.api_base_url}{bot_token}/getChatHistory"

        # 发送请求
        params = {
            "chat_id": channel_id,
            "limit": limit
        }

        response = requests.get(url, params=params)

        # 处理速率限制
        if self.handle_rate_limit(response):
            response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error collecting Telegram data: {response.status_code} - {response.text}")
            return []

        # 处理响应数据
        data = response.json()
        if not data.get('ok'):
            print(f"Telegram API error: {data.get('description')}")
            return []

        messages = data.get('result', {}).get('messages', [])

        # 转换数据格式
        transformed_data = []
        for message in messages:
            transformed_data.append({
                'id': message.get('message_id'),
                'text': message.get('text', ''),
                'created_at': message.get('date'),
                'author': {
                    'id': message.get('from', {}).get('id'),
                    'username': message.get('from', {}).get('username'),
                    'name': message.get('from', {}).get('first_name')
                },
                'source': 'telegram',
                'collected_at': datetime.utcnow().isoformat()
            })

        # 更新上次采集时间
        self.set_last_collected(datetime.utcnow().isoformat())

        return transformed_data

class DiscordCollector(SocialMediaCollector):
    """
    Discord 数据采集器
    """

    def __init__(self, config=None):
        """
        初始化 Discord 采集器

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.data_source = "discord"
        self.api_base_url = "https://discord.com/api/v10"

    def collect(self, channel_id, limit=100, **kwargs):
        """
        采集 Discord 频道数据

        Args:
            channel_id: 频道 ID
            limit: 最大消息数
            **kwargs: 其他参数

        Returns:
            采集的数据
        """
        discord_token = self.api_keys.get('discord_token')
        if not discord_token:
            raise ValueError("Discord token not provided")

        headers = {
            "Authorization": f"Bot {discord_token}",
            "Content-Type": "application/json"
        }

        # 构建请求 URL
        url = f"{self.api_base_url}/channels/{channel_id}/messages"

        # 发送请求
        params = {
            "limit": limit
        }

        response = requests.get(url, headers=headers, params=params)

        # 处理速率限制
        if self.handle_rate_limit(response):
            response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error collecting Discord data: {response.status_code} - {response.text}")
            return []

        # 处理响应数据
        messages = response.json()

        # 转换数据格式
        transformed_data = []
        for message in messages:
            transformed_data.append({
                'id': message.get('id'),
                'content': message.get('content'),
                'created_at': message.get('timestamp'),
                'author': {
                    'id': message.get('author', {}).get('id'),
                    'username': message.get('author', {}).get('username'),
                    'discriminator': message.get('author', {}).get('discriminator')
                },
                'attachments': message.get('attachments', []),
                'embeds': message.get('embeds', []),
                'source': 'discord',
                'collected_at': datetime.utcnow().isoformat()
            })

        # 更新上次采集时间
        self.set_last_collected(datetime.utcnow().isoformat())

        return transformed_data
