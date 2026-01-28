# 商业模式服务测试用例

import pytest
from commerce.api.commerce_api_service import CommerceAPIService

class TestCommerceAPIService:
    """
    商业模式服务测试类
    """

    def setup_method(self):
        """
        测试方法设置
        """
        self.commerce_service = CommerceAPIService()

    def test_get_plans(self):
        """
        测试获取订阅计划
        """
        response = self.commerce_service.get_plans()
        assert response["success"] is True
        assert "plans" in response["data"]
        plans = response["data"]["plans"]
        assert "basic" in plans
        assert "professional" in plans
        assert "enterprise" in plans

    def test_get_plan_details(self):
        """
        测试获取计划详情
        """
        # 测试基础版计划
        response = self.commerce_service.get_plan_details("basic")
        assert response["success"] is True
        assert "plan" in response["data"]
        plan = response["data"]["plan"]
        assert plan["name"] == "基础版"
        assert plan["price"] == 0

        # 测试专业版计划
        response = self.commerce_service.get_plan_details("professional")
        assert response["success"] is True
        plan = response["data"]["plan"]
        assert plan["name"] == "专业版"
        assert plan["price"] == 99

        # 测试企业版计划
        response = self.commerce_service.get_plan_details("enterprise")
        assert response["success"] is True
        plan = response["data"]["plan"]
        assert plan["name"] == "企业版"
        assert plan["price"] == 499

        # 测试不存在的计划
        response = self.commerce_service.get_plan_details("nonexistent")
        assert response["success"] is False
        assert "Plan not found" in response["message"]

    def test_create_subscription(self):
        """
        测试创建订阅
        """
        user_id = "test_user_1"
        plan_id = "basic"

        response = self.commerce_service.create_subscription(user_id, plan_id)
        assert response["success"] is True
        assert "subscription" in response["data"]
        subscription = response["data"]["subscription"]
        assert subscription["user_id"] == user_id
        assert subscription["plan_id"] == plan_id
        assert subscription["status"] == "active"

    def test_get_user_subscription(self):
        """
        测试获取用户订阅
        """
        user_id = "test_user_2"
        plan_id = "professional"

        # 创建订阅
        create_response = self.commerce_service.create_subscription(user_id, plan_id)
        assert create_response["success"] is True

        # 获取用户订阅
        response = self.commerce_service.get_user_subscription(user_id)
        assert response["success"] is True
        assert "subscription" in response["data"]
        subscription = response["data"]["subscription"]
        assert subscription["user_id"] == user_id
        assert subscription["plan_id"] == plan_id

        # 获取不存在用户的订阅（应该返回基础版）
        response = self.commerce_service.get_user_subscription("nonexistent_user")
        assert response["success"] is True
        assert "subscription" in response["data"]
        subscription = response["data"]["subscription"]
        assert subscription["plan_id"] == "basic"

    def test_update_subscription(self):
        """
        测试更新订阅
        """
        user_id = "test_user_3"

        # 创建初始订阅
        create_response = self.commerce_service.create_subscription(user_id, "basic")
        assert create_response["success"] is True

        # 更新到专业版
        update_response = self.commerce_service.update_subscription(user_id, "professional")
        assert update_response["success"] is True
        subscription = update_response["data"]["subscription"]
        assert subscription["plan_id"] == "professional"

    def test_cancel_subscription(self):
        """
        测试取消订阅
        """
        user_id = "test_user_4"

        # 创建订阅
        create_response = self.commerce_service.create_subscription(user_id, "professional")
        assert create_response["success"] is True

        # 取消订阅
        cancel_response = self.commerce_service.cancel_subscription(user_id)
        assert cancel_response["success"] is True
        subscription = cancel_response["data"]["subscription"]
        assert subscription["status"] == "cancelled"
        assert subscription["auto_renew"] is False

    def test_check_api_usage(self):
        """
        测试检查API使用情况
        """
        user_id = "test_user_5"

        # 创建订阅
        create_response = self.commerce_service.create_subscription(user_id, "basic")
        assert create_response["success"] is True

        # 检查API使用情况
        response = self.commerce_service.check_api_usage(user_id)
        assert response["success"] is True
        assert "usage" in response["data"]
        usage = response["data"]["usage"]
        assert "current_month" in usage
        assert "usage" in usage
        assert "limit" in usage

    def test_check_signal_usage(self):
        """
        测试检查信号使用情况
        """
        user_id = "test_user_6"

        # 创建订阅
        create_response = self.commerce_service.create_subscription(user_id, "basic")
        assert create_response["success"] is True

        # 检查信号使用情况
        response = self.commerce_service.check_signal_usage(user_id)
        assert response["success"] is True
        assert "usage" in response["data"]
        usage = response["data"]["usage"]
        assert "current_day" in usage
        assert "usage" in usage
        assert "limit" in usage

    def test_record_api_usage(self):
        """
        测试记录API使用
        """
        user_id = "test_user_7"

        # 创建订阅
        create_response = self.commerce_service.create_subscription(user_id, "basic")
        assert create_response["success"] is True

        # 记录API使用
        for i in range(5):
            result = self.commerce_service.record_api_usage(user_id)
            assert result is True

    def test_record_signal_usage(self):
        """
        测试记录信号使用
        """
        user_id = "test_user_8"

        # 创建订阅
        create_response = self.commerce_service.create_subscription(user_id, "basic")
        assert create_response["success"] is True

        # 记录信号使用
        for i in range(5):
            result = self.commerce_service.record_signal_usage(user_id)
            assert result is True

    def test_get_supported_payment_methods(self):
        """
        测试获取支持的支付方式
        """
        response = self.commerce_service.get_supported_payment_methods()
        assert response["success"] is True
        assert "payment_methods" in response["data"]
        assert "cryptocurrencies" in response["data"]
        payment_methods = response["data"]["payment_methods"]
        assert "credit_card" in payment_methods
        assert "paypal" in payment_methods
        assert "crypto" in payment_methods
        assert "bank_transfer" in payment_methods

    def test_add_payment_method(self):
        """
        测试添加支付方式
        """
        user_id = "test_user_9"

        # 添加信用卡支付方式
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123",
            "card_holder": "Test User"
        }

        response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert response["success"] is True
        assert "payment_method" in response["data"]
        payment_method = response["data"]["payment_method"]
        assert payment_method["user_id"] == user_id
        assert payment_method["type"] == "credit_card"
        assert payment_method["name"] == "Test Credit Card"

    def test_get_user_payment_methods(self):
        """
        测试获取用户支付方式
        """
        user_id = "test_user_10"

        # 添加支付方式
        payment_data = {
            "type": "paypal",
            "name": "Test PayPal",
            "paypal_email": "test@paypal.com"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True

        # 获取用户支付方式
        response = self.commerce_service.get_user_payment_methods(user_id)
        assert response["success"] is True
        assert "payment_methods" in response["data"]
        payment_methods = response["data"]["payment_methods"]
        assert len(payment_methods) > 0

    def test_set_default_payment_method(self):
        """
        测试设置默认支付方式
        """
        user_id = "test_user_11"

        # 添加两个支付方式
        payment_data1 = {
            "type": "credit_card",
            "name": "Credit Card 1",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response1 = self.commerce_service.add_payment_method(user_id, payment_data1)
        assert add_response1["success"] is True

        payment_data2 = {
            "type": "paypal",
            "name": "PayPal",
            "paypal_email": "test@paypal.com"
        }
        add_response2 = self.commerce_service.add_payment_method(user_id, payment_data2)
        assert add_response2["success"] is True

        # 设置第二个为默认
        payment_method_id = add_response2["data"]["payment_method"]["payment_method_id"]
        set_default_response = self.commerce_service.set_default_payment_method(user_id, payment_method_id)
        assert set_default_response["success"] is True

    def test_delete_payment_method(self):
        """
        测试删除支付方式
        """
        user_id = "test_user_12"

        # 添加支付方式
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True
        payment_method_id = add_response["data"]["payment_method"]["payment_method_id"]

        # 删除支付方式
        delete_response = self.commerce_service.delete_payment_method(user_id, payment_method_id)
        assert delete_response["success"] is True

    def test_process_payment(self):
        """
        测试处理支付
        """
        user_id = "test_user_13"

        # 添加支付方式
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True
        payment_method_id = add_response["data"]["payment_method"]["payment_method_id"]

        # 处理支付
        payment_request = {
            "amount": 99.0,
            "currency": "USD",
            "description": "Test Payment",
            "payment_method_id": payment_method_id
        }

        response = self.commerce_service.process_payment(user_id, payment_request)
        assert response["success"] is True
        assert "transaction" in response["data"]
        assert "invoice_id" in response["data"]

    def test_get_transaction_history(self):
        """
        测试获取交易历史
        """
        user_id = "test_user_14"

        # 添加支付方式并处理支付
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True
        payment_method_id = add_response["data"]["payment_method"]["payment_method_id"]

        # 处理支付
        payment_request = {
            "amount": 99.0,
            "currency": "USD",
            "description": "Test Payment",
            "payment_method_id": payment_method_id
        }
        process_response = self.commerce_service.process_payment(user_id, payment_request)
        assert process_response["success"] is True

        # 获取交易历史
        response = self.commerce_service.get_transaction_history(user_id)
        assert response["success"] is True
        assert "transactions" in response["data"]
        transactions = response["data"]["transactions"]
        assert len(transactions) > 0

    def test_get_invoice(self):
        """
        测试获取账单详情
        """
        user_id = "test_user_15"

        # 添加支付方式并处理支付
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True
        payment_method_id = add_response["data"]["payment_method"]["payment_method_id"]

        # 处理支付
        payment_request = {
            "amount": 99.0,
            "currency": "USD",
            "description": "Test Payment",
            "payment_method_id": payment_method_id
        }
        process_response = self.commerce_service.process_payment(user_id, payment_request)
        assert process_response["success"] is True
        invoice_id = process_response["data"]["invoice_id"]

        # 获取账单详情
        response = self.commerce_service.get_invoice(invoice_id)
        assert response["success"] is True
        assert "invoice" in response["data"]
        invoice = response["data"]["invoice"]
        assert invoice["invoice_id"] == invoice_id
        assert invoice["amount"] == 99.0

    def test_get_user_invoices(self):
        """
        测试获取用户账单列表
        """
        user_id = "test_user_16"

        # 添加支付方式并处理支付
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True
        payment_method_id = add_response["data"]["payment_method"]["payment_method_id"]

        # 处理支付
        payment_request = {
            "amount": 99.0,
            "currency": "USD",
            "description": "Test Payment",
            "payment_method_id": payment_method_id
        }
        process_response = self.commerce_service.process_payment(user_id, payment_request)
        assert process_response["success"] is True

        # 获取用户账单列表
        response = self.commerce_service.get_user_invoices(user_id)
        assert response["success"] is True
        assert "invoices" in response["data"]
        invoices = response["data"]["invoices"]
        assert len(invoices) > 0

    def test_create_subscription_with_payment(self):
        """
        测试创建订阅并处理支付
        """
        user_id = "test_user_17"

        # 添加支付方式
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_response["success"] is True
        payment_method_id = add_response["data"]["payment_method"]["payment_method_id"]

        # 创建订阅并处理支付
        request_data = {
            "plan_id": "professional",
            "payment_method_id": payment_method_id
        }

        response = self.commerce_service.create_subscription_with_payment(user_id, request_data)
        assert response["success"] is True
        assert "subscription" in response["data"]
        assert "payment" in response["data"]
        assert "invoice_id" in response["data"]

if __name__ == "__main__":
    pytest.main([__file__])
