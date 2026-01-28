# Subscription Service
# 订阅管理服务，实现不同级别的订阅计划和权限管理

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class SubscriptionService:
    """
    订阅管理服务
    处理用户订阅、计划管理和权限控制
    """

    def __init__(self):
        """
        初始化订阅服务
        """
        self.logger = logging.getLogger(__name__)
        
        # 订阅计划定义
        self.subscription_plans = {
            "basic": {
                "name": "基础版",
                "price": 0,
                "currency": "USD",
                "billing_cycle": "monthly",
                "features": [
                    "基础数据访问",
                    "每日信号限制 (10个)",
                    "基础分析工具",
                    "标准API速率限制",
                    "邮件支持"
                ],
                "api_rate_limit": 1000,  # 每月API调用限制
                "signal_limit": 10,  # 每日信号限制
                "data_access_level": "basic",
                "support_level": "email"
            },
            "professional": {
                "name": "专业版",
                "price": 99,
                "currency": "USD",
                "billing_cycle": "monthly",
                "features": [
                    "完整数据访问",
                    "每日信号无限制",
                    "高级分析工具",
                    "增强API速率限制",
                    "优先邮件支持",
                    "AI模型访问",
                    "自定义阈值设置"
                ],
                "api_rate_limit": 10000,  # 每月API调用限制
                "signal_limit": 0,  # 无限制
                "data_access_level": "full",
                "support_level": "priority_email"
            },
            "enterprise": {
                "name": "企业版",
                "price": 499,
                "currency": "USD",
                "billing_cycle": "monthly",
                "features": [
                    "完整数据访问",
                    "每日信号无限制",
                    "所有分析工具",
                    "无API速率限制",
                    "24/7 技术支持",
                    "AI模型定制",
                    "专用API端点",
                    "高级报告生成",
                    "团队协作功能"
                ],
                "api_rate_limit": 0,  # 无限制
                "signal_limit": 0,  # 无限制
                "data_access_level": "enterprise",
                "support_level": "24/7"
            }
        }

        # 模拟用户订阅数据库
        self.user_subscriptions = {}
        
        # 模拟API使用统计
        self.api_usage = {}
        
        # 模拟信号使用统计
        self.signal_usage = {}

    def get_plans(self) -> Dict[str, Any]:
        """
        获取所有订阅计划

        Returns:
            订阅计划列表
        """
        try:
            return self._success_response({
                "plans": self.subscription_plans
            })
        except Exception as e:
            self.logger.error(f"Error getting plans: {str(e)}")
            return self._error_response(str(e))

    def get_plan_details(self, plan_id: str) -> Dict[str, Any]:
        """
        获取特定计划详情

        Args:
            plan_id: 计划ID

        Returns:
            计划详情
        """
        try:
            if plan_id not in self.subscription_plans:
                return self._error_response(f"Plan not found: {plan_id}")

            return self._success_response({
                "plan": self.subscription_plans[plan_id]
            })
        except Exception as e:
            self.logger.error(f"Error getting plan details: {str(e)}")
            return self._error_response(str(e))

    def create_subscription(self, user_id: str, plan_id: str) -> Dict[str, Any]:
        """
        创建用户订阅

        Args:
            user_id: 用户ID
            plan_id: 计划ID

        Returns:
            订阅创建结果
        """
        try:
            # 验证计划是否存在
            if plan_id not in self.subscription_plans:
                return self._error_response(f"Invalid plan: {plan_id}")

            # 计算订阅到期时间
            now = datetime.now()
            if self.subscription_plans[plan_id]["billing_cycle"] == "monthly":
                expiry_date = now + timedelta(days=30)
            elif self.subscription_plans[plan_id]["billing_cycle"] == "yearly":
                expiry_date = now + timedelta(days=365)
            else:
                expiry_date = now + timedelta(days=30)  # 默认月付

            # 创建订阅
            subscription_id = f"sub_{user_id}_{int(now.timestamp())}"
            self.user_subscriptions[user_id] = {
                "subscription_id": subscription_id,
                "user_id": user_id,
                "plan_id": plan_id,
                "plan_name": self.subscription_plans[plan_id]["name"],
                "start_date": now.isoformat(),
                "expiry_date": expiry_date.isoformat(),
                "status": "active",
                "auto_renew": True,
                "payment_method": None,
                "last_payment_date": None,
                "next_payment_date": expiry_date.isoformat()
            }

            # 初始化使用统计
            if user_id not in self.api_usage:
                self.api_usage[user_id] = {
                    "current_month": now.strftime("%Y-%m"),
                    "usage": 0,
                    "limit": self.subscription_plans[plan_id]["api_rate_limit"]
                }

            if user_id not in self.signal_usage:
                self.signal_usage[user_id] = {
                    "current_day": now.strftime("%Y-%m-%d"),
                    "usage": 0,
                    "limit": self.subscription_plans[plan_id]["signal_limit"]
                }

            return self._success_response({
                "subscription": self.user_subscriptions[user_id]
            })
        except Exception as e:
            self.logger.error(f"Error creating subscription: {str(e)}")
            return self._error_response(str(e))

    def get_user_subscription(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户订阅信息

        Args:
            user_id: 用户ID

        Returns:
            用户订阅信息
        """
        try:
            if user_id not in self.user_subscriptions:
                # 如果用户没有订阅，默认返回基础版
                return self._success_response({
                    "subscription": {
                        "subscription_id": f"sub_{user_id}_default",
                        "user_id": user_id,
                        "plan_id": "basic",
                        "plan_name": "基础版",
                        "start_date": datetime.now().isoformat(),
                        "expiry_date": "2100-12-31T23:59:59",
                        "status": "active",
                        "auto_renew": False,
                        "payment_method": None,
                        "last_payment_date": None,
                        "next_payment_date": None
                    }
                })

            # 检查订阅是否过期
            subscription = self.user_subscriptions[user_id]
            expiry_date = datetime.fromisoformat(subscription["expiry_date"])
            if datetime.now() > expiry_date:
                subscription["status"] = "expired"
                self.user_subscriptions[user_id] = subscription

            return self._success_response({
                "subscription": subscription
            })
        except Exception as e:
            self.logger.error(f"Error getting user subscription: {str(e)}")
            return self._error_response(str(e))

    def update_subscription(self, user_id: str, plan_id: str) -> Dict[str, Any]:
        """
        更新用户订阅计划

        Args:
            user_id: 用户ID
            plan_id: 新计划ID

        Returns:
            更新结果
        """
        try:
            # 验证计划是否存在
            if plan_id not in self.subscription_plans:
                return self._error_response(f"Invalid plan: {plan_id}")

            # 计算新的到期时间
            now = datetime.now()
            if self.subscription_plans[plan_id]["billing_cycle"] == "monthly":
                expiry_date = now + timedelta(days=30)
            elif self.subscription_plans[plan_id]["billing_cycle"] == "yearly":
                expiry_date = now + timedelta(days=365)
            else:
                expiry_date = now + timedelta(days=30)  # 默认月付

            # 更新订阅
            subscription_id = f"sub_{user_id}_{int(now.timestamp())}"
            self.user_subscriptions[user_id] = {
                "subscription_id": subscription_id,
                "user_id": user_id,
                "plan_id": plan_id,
                "plan_name": self.subscription_plans[plan_id]["name"],
                "start_date": now.isoformat(),
                "expiry_date": expiry_date.isoformat(),
                "status": "active",
                "auto_renew": True,
                "payment_method": None,
                "last_payment_date": None,
                "next_payment_date": expiry_date.isoformat()
            }

            # 更新使用限制
            if user_id in self.api_usage:
                self.api_usage[user_id]["limit"] = self.subscription_plans[plan_id]["api_rate_limit"]
                self.api_usage[user_id]["current_month"] = now.strftime("%Y-%m")
                self.api_usage[user_id]["usage"] = 0

            if user_id in self.signal_usage:
                self.signal_usage[user_id]["limit"] = self.subscription_plans[plan_id]["signal_limit"]
                self.signal_usage[user_id]["current_day"] = now.strftime("%Y-%m-%d")
                self.signal_usage[user_id]["usage"] = 0

            return self._success_response({
                "subscription": self.user_subscriptions[user_id]
            })
        except Exception as e:
            self.logger.error(f"Error updating subscription: {str(e)}")
            return self._error_response(str(e))

    def cancel_subscription(self, user_id: str) -> Dict[str, Any]:
        """
        取消用户订阅

        Args:
            user_id: 用户ID

        Returns:
            取消结果
        """
        try:
            if user_id not in self.user_subscriptions:
                return self._error_response("Subscription not found")

            # 标记为已取消
            subscription = self.user_subscriptions[user_id]
            subscription["status"] = "cancelled"
            subscription["auto_renew"] = False
            self.user_subscriptions[user_id] = subscription

            return self._success_response({
                "message": "Subscription cancelled successfully",
                "subscription": subscription
            })
        except Exception as e:
            self.logger.error(f"Error cancelling subscription: {str(e)}")
            return self._error_response(str(e))

    def check_api_usage(self, user_id: str) -> Dict[str, Any]:
        """
        检查API使用情况

        Args:
            user_id: 用户ID

        Returns:
            API使用情况
        """
        try:
            now = datetime.now()
            current_month = now.strftime("%Y-%m")

            # 获取用户订阅
            subscription_info = self.get_user_subscription(user_id)
            if not subscription_info.get("success"):
                return subscription_info

            subscription = subscription_info.get("data", {}).get("subscription", {})
            plan_id = subscription.get("plan_id", "basic")
            limit = self.subscription_plans[plan_id]["api_rate_limit"]

            # 初始化或更新API使用统计
            if user_id not in self.api_usage or self.api_usage[user_id]["current_month"] != current_month:
                self.api_usage[user_id] = {
                    "current_month": current_month,
                    "usage": 0,
                    "limit": limit
                }

            usage = self.api_usage[user_id]
            return self._success_response({
                "usage": usage
            })
        except Exception as e:
            self.logger.error(f"Error checking API usage: {str(e)}")
            return self._error_response(str(e))

    def check_signal_usage(self, user_id: str) -> Dict[str, Any]:
        """
        检查信号使用情况

        Args:
            user_id: 用户ID

        Returns:
            信号使用情况
        """
        try:
            now = datetime.now()
            current_day = now.strftime("%Y-%m-%d")

            # 获取用户订阅
            subscription_info = self.get_user_subscription(user_id)
            if not subscription_info.get("success"):
                return subscription_info

            subscription = subscription_info.get("data", {}).get("subscription", {})
            plan_id = subscription.get("plan_id", "basic")
            limit = self.subscription_plans[plan_id]["signal_limit"]

            # 初始化或更新信号使用统计
            if user_id not in self.signal_usage or self.signal_usage[user_id]["current_day"] != current_day:
                self.signal_usage[user_id] = {
                    "current_day": current_day,
                    "usage": 0,
                    "limit": limit
                }

            usage = self.signal_usage[user_id]
            return self._success_response({
                "usage": usage
            })
        except Exception as e:
            self.logger.error(f"Error checking signal usage: {str(e)}")
            return self._error_response(str(e))

    def record_api_usage(self, user_id: str) -> bool:
        """
        记录API使用

        Args:
            user_id: 用户ID

        Returns:
            是否允许API调用
        """
        try:
            now = datetime.now()
            current_month = now.strftime("%Y-%m")

            # 获取用户订阅
            subscription_info = self.get_user_subscription(user_id)
            if not subscription_info.get("success"):
                return False

            subscription = subscription_info.get("data", {}).get("subscription", {})
            plan_id = subscription.get("plan_id", "basic")
            limit = self.subscription_plans[plan_id]["api_rate_limit"]

            # 无限制计划
            if limit == 0:
                return True

            # 初始化或更新API使用统计
            if user_id not in self.api_usage or self.api_usage[user_id]["current_month"] != current_month:
                self.api_usage[user_id] = {
                    "current_month": current_month,
                    "usage": 0,
                    "limit": limit
                }

            # 检查是否超过限制
            if self.api_usage[user_id]["usage"] >= limit:
                return False

            # 增加使用计数
            self.api_usage[user_id]["usage"] += 1
            return True
        except Exception:
            return False

    def record_signal_usage(self, user_id: str) -> bool:
        """
        记录信号使用

        Args:
            user_id: 用户ID

        Returns:
            是否允许信号生成
        """
        try:
            now = datetime.now()
            current_day = now.strftime("%Y-%m-%d")

            # 获取用户订阅
            subscription_info = self.get_user_subscription(user_id)
            if not subscription_info.get("success"):
                return False

            subscription = subscription_info.get("data", {}).get("subscription", {})
            plan_id = subscription.get("plan_id", "basic")
            limit = self.subscription_plans[plan_id]["signal_limit"]

            # 无限制计划
            if limit == 0:
                return True

            # 初始化或更新信号使用统计
            if user_id not in self.signal_usage or self.signal_usage[user_id]["current_day"] != current_day:
                self.signal_usage[user_id] = {
                    "current_day": current_day,
                    "usage": 0,
                    "limit": limit
                }

            # 检查是否超过限制
            if self.signal_usage[user_id]["usage"] >= limit:
                return False

            # 增加使用计数
            self.signal_usage[user_id]["usage"] += 1
            return True
        except Exception:
            return False

    def _success_response(self, data: Any) -> Dict[str, Any]:
        """
        成功响应

        Args:
            data: 响应数据

        Returns:
            响应对象
        """
        return {
            "success": True,
            "data": data,
            "message": "Operation completed successfully"
        }

    def _error_response(self, message: str) -> Dict[str, Any]:
        """
        错误响应

        Args:
            message: 错误消息

        Returns:
            响应对象
        """
        return {
            "success": False,
            "data": None,
            "message": message
        }
