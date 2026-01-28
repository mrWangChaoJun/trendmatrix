# Commerce API Service
# 商业模式API服务，集成订阅管理和支付系统

import logging
from typing import Dict, List, Optional, Any
from commerce.subscription.subscription_service import SubscriptionService
from commerce.payment.payment_service import PaymentService

class CommerceAPIService:
    """
    商业模式API服务
    集成订阅管理和支付系统
    """

    def __init__(self, subscription_service: Optional[SubscriptionService] = None, payment_service: Optional[PaymentService] = None):
        """
        初始化商业模式API服务

        Args:
            subscription_service: 订阅服务实例
            payment_service: 支付服务实例
        """
        self.logger = logging.getLogger(__name__)
        
        # 依赖服务
        self.subscription_service = subscription_service or SubscriptionService()
        self.payment_service = payment_service or PaymentService()

    def get_service_info(self) -> Dict[str, Any]:
        """
        获取服务信息

        Returns:
            服务信息
        """
        try:
            info = {
                "services": {
                    "subscription": True,
                    "payment": True
                },
                "endpoints": [
                    # 订阅端点
                    "/api/commerce/plans",
                    "/api/commerce/plan/{plan_id}",
                    "/api/commerce/subscription",
                    "/api/commerce/subscription/update",
                    "/api/commerce/subscription/cancel",
                    "/api/commerce/usage/api",
                    "/api/commerce/usage/signal",
                    # 支付端点
                    "/api/commerce/payment/methods",
                    "/api/commerce/payment/add",
                    "/api/commerce/payment/list",
                    "/api/commerce/payment/set-default",
                    "/api/commerce/payment/delete",
                    "/api/commerce/payment/process",
                    "/api/commerce/payment/history",
                    # 账单端点
                    "/api/commerce/invoice/{invoice_id}",
                    "/api/commerce/invoices"
                ]
            }

            return self._success_response(info)
        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return self._error_response(str(e))

    # 订阅相关方法
    def get_plans(self) -> Dict[str, Any]:
        """
        获取所有订阅计划

        Returns:
            订阅计划列表
        """
        try:
            return self.subscription_service.get_plans()
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
            return self.subscription_service.get_plan_details(plan_id)
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
            return self.subscription_service.create_subscription(user_id, plan_id)
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
            return self.subscription_service.get_user_subscription(user_id)
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
            return self.subscription_service.update_subscription(user_id, plan_id)
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
            return self.subscription_service.cancel_subscription(user_id)
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
            return self.subscription_service.check_api_usage(user_id)
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
            return self.subscription_service.check_signal_usage(user_id)
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
            return self.subscription_service.record_api_usage(user_id)
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
            return self.subscription_service.record_signal_usage(user_id)
        except Exception:
            return False

    # 支付相关方法
    def get_supported_payment_methods(self) -> Dict[str, Any]:
        """
        获取支持的支付方式

        Returns:
            支持的支付方式列表
        """
        try:
            return self.payment_service.get_supported_payment_methods()
        except Exception as e:
            self.logger.error(f"Error getting supported payment methods: {str(e)}")
            return self._error_response(str(e))

    def add_payment_method(self, user_id: str, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加用户支付方式

        Args:
            user_id: 用户ID
            payment_data: 支付方式数据

        Returns:
            添加结果
        """
        try:
            return self.payment_service.add_payment_method(user_id, payment_data)
        except Exception as e:
            self.logger.error(f"Error adding payment method: {str(e)}")
            return self._error_response(str(e))

    def get_user_payment_methods(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户支付方式

        Args:
            user_id: 用户ID

        Returns:
            用户支付方式列表
        """
        try:
            return self.payment_service.get_user_payment_methods(user_id)
        except Exception as e:
            self.logger.error(f"Error getting user payment methods: {str(e)}")
            return self._error_response(str(e))

    def set_default_payment_method(self, user_id: str, payment_method_id: str) -> Dict[str, Any]:
        """
        设置默认支付方式

        Args:
            user_id: 用户ID
            payment_method_id: 支付方式ID

        Returns:
            设置结果
        """
        try:
            return self.payment_service.set_default_payment_method(user_id, payment_method_id)
        except Exception as e:
            self.logger.error(f"Error setting default payment method: {str(e)}")
            return self._error_response(str(e))

    def delete_payment_method(self, user_id: str, payment_method_id: str) -> Dict[str, Any]:
        """
        删除用户支付方式

        Args:
            user_id: 用户ID
            payment_method_id: 支付方式ID

        Returns:
            删除结果
        """
        try:
            return self.payment_service.delete_payment_method(user_id, payment_method_id)
        except Exception as e:
            self.logger.error(f"Error deleting payment method: {str(e)}")
            return self._error_response(str(e))

    def process_payment(self, user_id: str, payment_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理支付

        Args:
            user_id: 用户ID
            payment_request: 支付请求数据

        Returns:
            支付处理结果
        """
        try:
            return self.payment_service.process_payment(user_id, payment_request)
        except Exception as e:
            self.logger.error(f"Error processing payment: {str(e)}")
            return self._error_response(str(e))

    def get_transaction_history(self, user_id: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        获取交易历史

        Args:
            user_id: 用户ID
            limit: 限制返回数量
            offset: 偏移量

        Returns:
            交易历史
        """
        try:
            return self.payment_service.get_transaction_history(user_id, limit, offset)
        except Exception as e:
            self.logger.error(f"Error getting transaction history: {str(e)}")
            return self._error_response(str(e))

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        获取账单详情

        Args:
            invoice_id: 账单ID

        Returns:
            账单详情
        """
        try:
            return self.payment_service.get_invoice(invoice_id)
        except Exception as e:
            self.logger.error(f"Error getting invoice: {str(e)}")
            return self._error_response(str(e))

    def get_user_invoices(self, user_id: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        获取用户账单列表

        Args:
            user_id: 用户ID
            limit: 限制返回数量
            offset: 偏移量

        Returns:
            账单列表
        """
        try:
            return self.payment_service.get_user_invoices(user_id, limit, offset)
        except Exception as e:
            self.logger.error(f"Error getting user invoices: {str(e)}")
            return self._error_response(str(e))

    # 集成方法
    def create_subscription_with_payment(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建订阅并处理支付

        Args:
            user_id: 用户ID
            request_data: 请求数据

        Returns:
            创建和支付结果
        """
        try:
            # 验证请求参数
            required_params = ['plan_id', 'payment_method_id']
            for param in required_params:
                if param not in request_data:
                    return self._error_response(f"Missing required parameter: {param}")

            plan_id = request_data['plan_id']
            payment_method_id = request_data['payment_method_id']

            # 获取计划信息
            plan_info = self.subscription_service.get_plan_details(plan_id)
            if not plan_info.get('success'):
                return plan_info

            plan = plan_info.get('data', {}).get('plan', {})
            price = plan.get('price', 0)
            currency = plan.get('currency', 'USD')

            # 如果价格为0，直接创建订阅
            if price == 0:
                subscription_result = self.subscription_service.create_subscription(user_id, plan_id)
                return subscription_result

            # 处理支付
            payment_request = {
                'amount': price,
                'currency': currency,
                'description': f"Subscription to {plan.get('name', 'Plan')}",
                'payment_method_id': payment_method_id
            }

            payment_result = self.payment_service.process_payment(user_id, payment_request)
            if not payment_result.get('success'):
                return payment_result

            # 支付成功后创建订阅
            subscription_result = self.subscription_service.create_subscription(user_id, plan_id)
            if not subscription_result.get('success'):
                # 这里可以添加退款逻辑
                return subscription_result

            return self._success_response({
                'subscription': subscription_result.get('data', {}).get('subscription'),
                'payment': payment_result.get('data', {}).get('transaction'),
                'invoice_id': payment_result.get('data', {}).get('invoice_id')
            })

        except Exception as e:
            self.logger.error(f"Error creating subscription with payment: {str(e)}")
            return self._error_response(str(e))

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
