# Payment Service
# 支付系统服务，实现支付处理和账单管理

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

class PaymentService:
    """
    支付系统服务
    处理支付交易、账单管理和支付方法管理
    """

    def __init__(self):
        """
        初始化支付服务
        """
        self.logger = logging.getLogger(__name__)
        
        # 模拟支付方法数据库
        self.payment_methods = {}
        
        # 模拟交易记录
        self.transactions = {}
        
        # 模拟账单记录
        self.invoices = {}
        
        # 支持的支付方式
        self.supported_payment_methods = [
            "credit_card",
            "paypal",
            "crypto",
            "bank_transfer"
        ]
        
        # 支持的加密货币
        self.supported_cryptocurrencies = [
            "BTC",
            "ETH",
            "SOL",
            "USDC"
        ]

    def get_supported_payment_methods(self) -> Dict[str, Any]:
        """
        获取支持的支付方式

        Returns:
            支持的支付方式列表
        """
        try:
            return self._success_response({
                "payment_methods": self.supported_payment_methods,
                "cryptocurrencies": self.supported_cryptocurrencies
            })
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
            # 验证请求参数
            required_params = ['type', 'name']
            for param in required_params:
                if param not in payment_data:
                    return self._error_response(f"Missing required parameter: {param}")

            # 验证支付方式类型
            payment_type = payment_data['type']
            if payment_type not in self.supported_payment_methods:
                return self._error_response(f"Unsupported payment method: {payment_type}")

            # 根据支付类型验证特定参数
            if payment_type == "credit_card":
                if 'card_number' not in payment_data or 'expiry_date' not in payment_data or 'cvv' not in payment_data:
                    return self._error_response("Missing credit card details")
            elif payment_type == "paypal":
                if 'paypal_email' not in payment_data:
                    return self._error_response("Missing PayPal email")
            elif payment_type == "crypto":
                if 'crypto_type' not in payment_data or 'wallet_address' not in payment_data:
                    return self._error_response("Missing cryptocurrency details")
                if payment_data['crypto_type'] not in self.supported_cryptocurrencies:
                    return self._error_response(f"Unsupported cryptocurrency: {payment_data['crypto_type']}")
            elif payment_type == "bank_transfer":
                if 'bank_name' not in payment_data or 'account_number' not in payment_data:
                    return self._error_response("Missing bank transfer details")

            # 初始化用户支付方式
            if user_id not in self.payment_methods:
                self.payment_methods[user_id] = []

            # 创建支付方式ID
            payment_method_id = f"pm_{user_id}_{int(datetime.now().timestamp())}"

            # 创建支付方式记录
            payment_method = {
                "payment_method_id": payment_method_id,
                "user_id": user_id,
                "type": payment_type,
                "name": payment_data['name'],
                "created_at": datetime.now().isoformat(),
                "is_default": len(self.payment_methods[user_id]) == 0,  # 第一个为默认
                "details": {}
            }

            # 添加特定支付方式的详细信息
            if payment_type == "credit_card":
                # 安全存储（实际应用中应加密存储）
                payment_method["details"] = {
                    "card_number": "****" + payment_data['card_number'][-4:],
                    "expiry_date": payment_data['expiry_date'],
                    "card_holder": payment_data.get('card_holder', '')
                }
            elif payment_type == "paypal":
                payment_method["details"] = {
                    "paypal_email": payment_data['paypal_email']
                }
            elif payment_type == "crypto":
                payment_method["details"] = {
                    "crypto_type": payment_data['crypto_type'],
                    "wallet_address": payment_data['wallet_address']
                }
            elif payment_type == "bank_transfer":
                payment_method["details"] = {
                    "bank_name": payment_data['bank_name'],
                    "account_number": "****" + payment_data['account_number'][-4:],
                    "routing_number": payment_data.get('routing_number', '')
                }

            # 添加到用户支付方式列表
            self.payment_methods[user_id].append(payment_method)

            return self._success_response({
                "payment_method": payment_method
            })
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
            if user_id not in self.payment_methods:
                return self._success_response({
                    "payment_methods": []
                })

            return self._success_response({
                "payment_methods": self.payment_methods[user_id]
            })
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
            if user_id not in self.payment_methods:
                return self._error_response("No payment methods found for user")

            # 查找支付方式
            payment_method = None
            for pm in self.payment_methods[user_id]:
                if pm['payment_method_id'] == payment_method_id:
                    payment_method = pm
                    break

            if not payment_method:
                return self._error_response("Payment method not found")

            # 更新默认状态
            for pm in self.payment_methods[user_id]:
                pm['is_default'] = (pm['payment_method_id'] == payment_method_id)

            return self._success_response({
                "message": "Default payment method set successfully",
                "payment_method": payment_method
            })
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
            if user_id not in self.payment_methods:
                return self._error_response("No payment methods found for user")

            # 查找并删除支付方式
            payment_method = None
            updated_methods = []
            for pm in self.payment_methods[user_id]:
                if pm['payment_method_id'] == payment_method_id:
                    payment_method = pm
                else:
                    updated_methods.append(pm)

            if not payment_method:
                return self._error_response("Payment method not found")

            # 更新支付方式列表
            self.payment_methods[user_id] = updated_methods

            # 如果删除的是默认支付方式，设置第一个为默认
            if payment_method['is_default'] and updated_methods:
                updated_methods[0]['is_default'] = True

            return self._success_response({
                "message": "Payment method deleted successfully"
            })
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
            # 验证请求参数
            required_params = ['amount', 'currency', 'description']
            for param in required_params:
                if param not in payment_request:
                    return self._error_response(f"Missing required parameter: {param}")

            # 获取金额和货币
            amount = payment_request['amount']
            currency = payment_request['currency']
            description = payment_request['description']

            # 验证金额
            if amount <= 0:
                return self._error_response("Amount must be positive")

            # 获取支付方式
            payment_method_id = payment_request.get('payment_method_id')
            payment_method = None

            if payment_method_id:
                # 使用指定的支付方式
                if user_id in self.payment_methods:
                    for pm in self.payment_methods[user_id]:
                        if pm['payment_method_id'] == payment_method_id:
                            payment_method = pm
                            break
                if not payment_method:
                    return self._error_response("Payment method not found")
            else:
                # 使用默认支付方式
                if user_id in self.payment_methods and self.payment_methods[user_id]:
                    for pm in self.payment_methods[user_id]:
                        if pm['is_default']:
                            payment_method = pm
                            break
                    # 如果没有默认，使用第一个
                    if not payment_method:
                        payment_method = self.payment_methods[user_id][0]
                else:
                    return self._error_response("No payment method found")

            # 生成交易ID
            transaction_id = f"txn_{user_id}_{int(datetime.now().timestamp())}"

            # 模拟支付处理（实际应用中应调用支付网关API）
            # 这里只是模拟成功
            transaction = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "payment_method_id": payment_method['payment_method_id'],
                "payment_method_type": payment_method['type'],
                "amount": amount,
                "currency": currency,
                "description": description,
                "status": "completed",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            # 保存交易记录
            if user_id not in self.transactions:
                self.transactions[user_id] = []
            self.transactions[user_id].append(transaction)

            # 创建账单
            invoice_id = self._create_invoice(user_id, transaction)

            return self._success_response({
                "transaction": transaction,
                "invoice_id": invoice_id
            })
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
            if user_id not in self.transactions:
                return self._success_response({
                    "transactions": [],
                    "total": 0
                })

            transactions = self.transactions[user_id]
            total = len(transactions)
            
            # 按时间倒序排序
            sorted_transactions = sorted(
                transactions,
                key=lambda x: x['created_at'],
                reverse=True
            )

            # 分页
            paginated_transactions = sorted_transactions[offset:offset + limit]

            return self._success_response({
                "transactions": paginated_transactions,
                "total": total,
                "limit": limit,
                "offset": offset
            })
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
            if invoice_id not in self.invoices:
                return self._error_response("Invoice not found")

            return self._success_response({
                "invoice": self.invoices[invoice_id]
            })
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
            # 查找用户的账单
            user_invoices = []
            for invoice in self.invoices.values():
                if invoice['user_id'] == user_id:
                    user_invoices.append(invoice)

            total = len(user_invoices)
            
            # 按时间倒序排序
            sorted_invoices = sorted(
                user_invoices,
                key=lambda x: x['created_at'],
                reverse=True
            )

            # 分页
            paginated_invoices = sorted_invoices[offset:offset + limit]

            return self._success_response({
                "invoices": paginated_invoices,
                "total": total,
                "limit": limit,
                "offset": offset
            })
        except Exception as e:
            self.logger.error(f"Error getting user invoices: {str(e)}")
            return self._error_response(str(e))

    def _create_invoice(self, user_id: str, transaction: Dict[str, Any]) -> str:
        """
        创建账单

        Args:
            user_id: 用户ID
            transaction: 交易数据

        Returns:
            账单ID
        """
        # 创建账单ID
        invoice_id = f"inv_{user_id}_{int(datetime.now().timestamp())}"

        # 创建账单
        invoice = {
            "invoice_id": invoice_id,
            "user_id": user_id,
            "transaction_id": transaction['transaction_id'],
            "amount": transaction['amount'],
            "currency": transaction['currency'],
            "description": transaction['description'],
            "status": "paid",
            "created_at": datetime.now().isoformat(),
            "paid_at": datetime.now().isoformat()
        }

        # 保存账单
        self.invoices[invoice_id] = invoice

        return invoice_id

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
