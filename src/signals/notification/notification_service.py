# Notification Service

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

class NotificationService:
    """
    通知服务
    处理信号通知和阈值管理
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化通知服务

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 通知配置
        self.notification_enabled = self.config.get('enabled', True)
        self.default_thresholds = self.config.get('default_thresholds', {
            'buy': 6,
            'sell': 6,
            'alert': 5,
            'hold': 0
        })

        # 用户自定义阈值
        self.user_thresholds = {}

        # 通知渠道
        self.channels = {
            'email': self._send_email_notification,
            'sms': self._send_sms_notification,
            'webhook': self._send_webhook_notification,
            'system': self._send_system_notification
        }

        # 通知历史
        self.notification_history = []

    def set_user_thresholds(self, user_id: str, thresholds: Dict[str, int]) -> bool:
        """
        设置用户自定义阈值

        Args:
            user_id: 用户 ID
            thresholds: 阈值配置

        Returns:
            是否成功
        """
        try:
            # 验证阈值
            if not self._validate_thresholds(thresholds):
                self.logger.error("Invalid thresholds")
                return False

            # 保存用户阈值
            self.user_thresholds[user_id] = thresholds
            self.logger.info(f"Set thresholds for user {user_id}: {thresholds}")

            return True

        except Exception as e:
            self.logger.error(f"Error setting user thresholds: {str(e)}")
            return False

    def get_user_thresholds(self, user_id: str) -> Dict[str, int]:
        """
        获取用户阈值

        Args:
            user_id: 用户 ID

        Returns:
            阈值配置
        """
        return self.user_thresholds.get(user_id, self.default_thresholds)

    def check_and_send_notifications(self, signal: Dict[str, Any], user_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        检查信号并发送通知

        Args:
            signal: 信号对象
            user_ids: 用户 ID 列表

        Returns:
            通知结果列表
        """
        try:
            if not self.notification_enabled:
                self.logger.info("Notifications disabled")
                return []

            # 验证信号
            if not self._validate_signal(signal):
                self.logger.error("Invalid signal for notification")
                return []

            # 确定目标用户
            target_users = user_ids or self.user_thresholds.keys()
            if not target_users:
                target_users = ['default']  # 默认用户

            # 处理每个用户的通知
            notification_results = []
            for user_id in target_users:
                # 检查是否需要通知
                if self._should_notify(user_id, signal):
                    # 发送通知
                    notification = self._send_notification(user_id, signal)
                    if notification:
                        notification_results.append(notification)

            return notification_results

        except Exception as e:
            self.logger.error(f"Error checking and sending notifications: {str(e)}")
            return []

    def _should_notify(self, user_id: str, signal: Dict[str, Any]) -> bool:
        """
        检查是否应该发送通知

        Args:
            user_id: 用户 ID
            signal: 信号对象

        Returns:
            是否应该通知
        """
        try:
            # 获取用户阈值
            thresholds = self.get_user_thresholds(user_id)

            # 检查信号类型阈值
            signal_type = signal['type']
            if signal_type not in thresholds:
                return False

            # 检查信号强度是否达到阈值
            signal_strength = signal['strength']
            threshold = thresholds[signal_type]

            return signal_strength >= threshold

        except Exception as e:
            self.logger.error(f"Error checking notification condition: {str(e)}")
            return False

    def _send_notification(self, user_id: str, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送通知

        Args:
            user_id: 用户 ID
            signal: 信号对象

        Returns:
            通知结果
        """
        try:
            # 获取用户通知配置
            user_config = self._get_user_notification_config(user_id)

            # 构建通知内容
            notification_content = self._build_notification_content(signal)

            # 发送到各个渠道
            channel_results = {}
            for channel in user_config.get('channels', ['system']):
                if channel in self.channels:
                    result = self.channels[channel](user_id, notification_content)
                    channel_results[channel] = result

            # 记录通知历史
            notification = {
                'notification_id': f"notif_{int(time.time())}_{user_id}",
                'user_id': user_id,
                'signal_id': signal['signal_id'],
                'signal_type': signal['type'],
                'signal_strength': signal['strength'],
                'signal_level': signal.get('level', 'unknown'),
                'content': notification_content,
                'channels': channel_results,
                'timestamp': datetime.now().isoformat(),
                'status': 'sent' if any(channel_results.values()) else 'failed'
            }

            self.notification_history.append(notification)
            self.logger.info(f"Sent notification to user {user_id} for signal {signal['signal_id']}")

            return notification

        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
            return None

    def _build_notification_content(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建通知内容

        Args:
            signal: 信号对象

        Returns:
            通知内容
        """
        asset = signal['asset']
        signal_type = signal['type']
        strength = signal['strength']
        confidence = signal['confidence']
        level = signal.get('level', 'unknown')
        description = signal.get('description', '')

        # 构建标题和消息
        titles = {
            'buy': f"🚀 买入信号: {asset}",
            'sell': f"📉 卖出信号: {asset}",
            'alert': f"⚠️ 预警信号: {asset}",
            'hold': f"📊 持有信号: {asset}"
        }

        messages = {
            'buy': f"{asset} 生成买入信号\n强度: {strength}/10\n置信度: {confidence:.2f}\n级别: {level}\n{description}",
            'sell': f"{asset} 生成卖出信号\n强度: {strength}/10\n置信度: {confidence:.2f}\n级别: {level}\n{description}",
            'alert': f"{asset} 生成预警信号\n强度: {strength}/10\n置信度: {confidence:.2f}\n级别: {level}\n{description}",
            'hold': f"{asset} 生成持有信号\n强度: {strength}/10\n置信度: {confidence:.2f}\n级别: {level}\n{description}"
        }

        return {
            'title': titles.get(signal_type, f"信号: {asset}"),
            'message': messages.get(signal_type, description),
            'asset': asset,
            'signal_type': signal_type,
            'strength': strength,
            'confidence': confidence,
            'level': level,
            'signal_id': signal['signal_id'],
            'timestamp': signal['timestamp'],
            'data': signal
        }

    def _send_email_notification(self, user_id: str, content: Dict[str, Any]) -> bool:
        """
        发送邮件通知

        Args:
            user_id: 用户 ID
            content: 通知内容

        Returns:
            是否成功
        """
        try:
            # 这里应该集成实际的邮件发送服务
            # 现在只是模拟实现
            self.logger.info(f"Sending email notification to user {user_id}: {content['title']}")
            # 实际实现示例:
            # email_client.send_email(
            #     to=user_email,
            #     subject=content['title'],
            #     body=content['message']
            # )
            return True

        except Exception as e:
            self.logger.error(f"Error sending email notification: {str(e)}")
            return False

    def _send_sms_notification(self, user_id: str, content: Dict[str, Any]) -> bool:
        """
        发送短信通知

        Args:
            user_id: 用户 ID
            content: 通知内容

        Returns:
            是否成功
        """
        try:
            # 这里应该集成实际的短信发送服务
            # 现在只是模拟实现
            self.logger.info(f"Sending SMS notification to user {user_id}: {content['title']}")
            # 实际实现示例:
            # sms_client.send_sms(
            #     to=user_phone,
            #     message=content['message'][:160]  # 短信长度限制
            # )
            return True

        except Exception as e:
            self.logger.error(f"Error sending SMS notification: {str(e)}")
            return False

    def _send_webhook_notification(self, user_id: str, content: Dict[str, Any]) -> bool:
        """
        发送 Webhook 通知

        Args:
            user_id: 用户 ID
            content: 通知内容

        Returns:
            是否成功
        """
        try:
            # 这里应该集成实际的 Webhook 发送服务
            # 现在只是模拟实现
            self.logger.info(f"Sending webhook notification to user {user_id}: {content['title']}")
            # 实际实现示例:
            # import requests
            # webhook_url = user_webhook_url
            # requests.post(webhook_url, json=content, timeout=5)
            return True

        except Exception as e:
            self.logger.error(f"Error sending webhook notification: {str(e)}")
            return False

    def _send_system_notification(self, user_id: str, content: Dict[str, Any]) -> bool:
        """
        发送系统通知

        Args:
            user_id: 用户 ID
            content: 通知内容

        Returns:
            是否成功
        """
        try:
            # 系统内部通知，存储到通知中心
            self.logger.info(f"Sending system notification to user {user_id}: {content['title']}")
            # 实际实现可能是存储到数据库或通知中心
            return True

        except Exception as e:
            self.logger.error(f"Error sending system notification: {str(e)}")
            return False

    def _validate_thresholds(self, thresholds: Dict[str, int]) -> bool:
        """
        验证阈值配置

        Args:
            thresholds: 阈值配置

        Returns:
            是否有效
        """
        try:
            for signal_type, threshold in thresholds.items():
                if not isinstance(threshold, int) or threshold < 0 or threshold > 10:
                    return False
            return True

        except Exception as e:
            self.logger.error(f"Error validating thresholds: {str(e)}")
            return False

    def _validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        验证信号

        Args:
            signal: 信号对象

        Returns:
            是否有效
        """
        try:
            required_fields = ['signal_id', 'asset', 'type', 'strength', 'confidence']
            for field in required_fields:
                if field not in signal:
                    return False

            if not 1 <= signal['strength'] <= 10:
                return False

            if not 0 <= signal['confidence'] <= 1:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating signal: {str(e)}")
            return False

    def _get_user_notification_config(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户通知配置

        Args:
            user_id: 用户 ID

        Returns:
            通知配置
        """
        # 这里应该从用户配置中获取
        # 现在返回默认配置
        return {
            'channels': ['system'],
            'enabled': True
        }

    def get_notification_history(self, user_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取通知历史

        Args:
            user_id: 用户 ID
            limit: 限制数量

        Returns:
            通知历史列表
        """
        try:
            if user_id:
                history = [n for n in self.notification_history if n['user_id'] == user_id]
            else:
                history = self.notification_history

            return history[-limit:]

        except Exception as e:
            self.logger.error(f"Error getting notification history: {str(e)}")
            return []

    def update_notification_config(self, config: Dict[str, Any]) -> bool:
        """
        更新通知配置

        Args:
            config: 配置参数

        Returns:
            是否成功
        """
        try:
            if 'enabled' in config:
                self.notification_enabled = config['enabled']

            if 'default_thresholds' in config:
                if self._validate_thresholds(config['default_thresholds']):
                    self.default_thresholds = config['default_thresholds']

            self.logger.info("Updated notification config")
            return True

        except Exception as e:
            self.logger.error(f"Error updating notification config: {str(e)}")
            return False

    def clear_notification_history(self, user_id: Optional[str] = None) -> bool:
        """
        清除通知历史

        Args:
            user_id: 用户 ID

        Returns:
            是否成功
        """
        try:
            if user_id:
                self.notification_history = [n for n in self.notification_history if n['user_id'] != user_id]
            else:
                self.notification_history = []

            self.logger.info(f"Cleared notification history for user {user_id if user_id else 'all users'}")
            return True

        except Exception as e:
            self.logger.error(f"Error clearing notification history: {str(e)}")
            return False
