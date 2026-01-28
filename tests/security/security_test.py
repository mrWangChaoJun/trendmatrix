# 安全测试脚本

from api.auth_service import AuthService
from commerce.api.commerce_api_service import CommerceAPIService

class SecurityTest:
    """
    安全测试类
    """

    def __init__(self):
        """
        初始化安全测试
        """
        self.auth_service = AuthService()
        self.commerce_service = CommerceAPIService()

    def test_authentication_security(self):
        """
        测试认证安全性
        """
        print("\n=== 开始认证安全性测试 ===")

        # 1. 测试弱密码
        print("\n1. 测试弱密码")
        weak_password_data = {
            "username": "weak_pass_user",
            "email": "weak_pass@example.com",
            "password": "123456",  # 弱密码
            "role": "user"
        }
        # 注意：当前实现允许弱密码，实际应用中应该添加密码强度检查
        weak_pass_response = self.auth_service.register(weak_password_data)
        assert weak_pass_response["success"] is True
        print("⚠️  当前实现允许弱密码，建议添加密码强度检查")

        # 2. 测试暴力破解防护
        print("\n2. 测试暴力破解防护")
        # 模拟多次登录尝试
        login_data = {
            "username": "weak_pass_user",
            "password": "wrongpassword"
        }

        # 测试5次错误登录
        for i in range(5):
            response = self.auth_service.login(login_data)
            assert response["success"] is False
        print("⚠️  当前实现没有暴力破解防护，建议添加登录尝试限制")

        # 3. 测试令牌安全
        print("\n3. 测试令牌安全")
        # 注册用户获取令牌
        secure_user_data = {
            "username": "secure_user",
            "email": "secure@example.com",
            "password": "SecurePassword123!",
            "role": "user"
        }
        secure_register_response = self.auth_service.register(secure_user_data)
        token = secure_register_response["data"]["token"]

        # 测试无效令牌
        invalid_token = token + "invalid"
        invalid_token_response = self.auth_service.verify_token(invalid_token)
        assert invalid_token_response["success"] is False
        print("✅ 无效令牌验证失败，令牌安全检查通过")

        # 4. 测试授权安全
        print("\n4. 测试授权安全")
        # 测试权限检查
        assert self.auth_service.check_permission("user", "read") is True
        assert self.auth_service.check_permission("user", "analyze") is True
        assert self.auth_service.check_permission("user", "delete") is False
        assert self.auth_service.check_permission("guest", "read") is True
        assert self.auth_service.check_permission("guest", "analyze") is False
        print("✅ 权限检查通过，授权安全测试成功")

        print("\n=== 认证安全性测试完成 ===")

    def test_input_validation(self):
        """
        测试输入验证
        """
        print("\n=== 开始输入验证测试 ===")

        # 1. 测试SQL注入防护
        print("\n1. 测试SQL注入防护")
        sql_injection_data = {
            "username": "admin' --",
            "email": "sql@example.com",
            "password": "password123",
            "role": "user"
        }
        sql_response = self.auth_service.register(sql_injection_data)
        # 应该返回成功，因为我们使用的是内存存储，实际应用中应该测试数据库存储
        print("⚠️  当前使用内存存储，建议在实际数据库环境中测试SQL注入防护")

        # 2. 测试XSS防护
        print("\n2. 测试XSS防护")
        xss_data = {
            "username": "<script>alert('XSS')</script>",
            "email": "xss@example.com",
            "password": "password123",
            "role": "user"
        }
        xss_response = self.auth_service.register(xss_data)
        # 应该返回成功，因为我们使用的是内存存储，实际应用中应该测试前端和后端的XSS防护
        print("⚠️  当前使用内存存储，建议在实际Web环境中测试XSS防护")

        # 3. 测试参数验证
        print("\n3. 测试参数验证")
        # 测试缺少必要参数
        missing_params_data = {
            "username": "testuser",
            "email": "test@example.com",
            # 缺少password和role
        }
        missing_params_response = self.auth_service.register(missing_params_data)
        assert missing_params_response["success"] is False
        assert "Missing required parameter" in missing_params_response["message"]
        print("✅ 参数验证通过，缺少必要参数时返回错误")

        # 测试无效角色
        invalid_role_data = {
            "username": "invalid_role_user",
            "email": "invalid_role@example.com",
            "password": "password123",
            "role": "invalid_role"
        }
        invalid_role_response = self.auth_service.register(invalid_role_data)
        assert invalid_role_response["success"] is False
        assert "Invalid role" in invalid_role_response["message"]
        print("✅ 无效角色验证通过，返回错误信息")

        print("\n=== 输入验证测试完成 ===")

    def test_sensitive_data_protection(self):
        """
        测试敏感数据保护
        """
        print("\n=== 开始敏感数据保护测试 ===")

        # 1. 测试密码加密
        print("\n1. 测试密码加密")
        password_data = {
            "username": "password_test_user",
            "email": "password_test@example.com",
            "password": "Password123!",
            "role": "user"
        }
        password_response = self.auth_service.register(password_data)
        user_id = password_response["data"]["user_id"]

        # 获取用户信息，检查密码是否被隐藏
        user_info_response = self.auth_service.get_user_info(user_id)
        assert user_info_response["success"] is True
        user_info = user_info_response["data"]
        assert "password" not in user_info
        print("✅ 密码在用户信息中被隐藏，敏感数据保护通过")

        # 2. 测试支付信息保护
        print("\n2. 测试支付信息保护")
        # 添加支付方式
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_payment_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_payment_response["success"] is True
        payment_method = add_payment_response["data"]["payment_method"]

        # 检查卡号是否被部分隐藏
        card_details = payment_method["details"]
        assert "card_number" in card_details
        assert "****" in card_details["card_number"]
        assert len(card_details["card_number"]) == 8  # **** + 后4位
        print("✅ 信用卡号被部分隐藏，支付信息保护通过")

        # 3. 测试交易数据保护
        print("\n3. 测试交易数据保护")
        # 处理支付
        payment_request = {
            "amount": 99.0,
            "currency": "USD",
            "description": "Test Payment",
            "payment_method_id": payment_method["payment_method_id"]
        }
        payment_response = self.commerce_service.process_payment(user_id, payment_request)
        assert payment_response["success"] is True
        transaction = payment_response["data"]["transaction"]

        # 检查交易数据中是否包含敏感信息
        assert "payment_method_id" in transaction
        assert "payment_method_type" in transaction
        assert "card_number" not in transaction
        assert "cvv" not in transaction
        print("✅ 交易数据中不包含敏感信息，数据保护通过")

        print("\n=== 敏感数据保护测试完成 ===")

    def test_rate_limiting(self):
        """
        测试速率限制
        """
        print("\n=== 开始速率限制测试 ===")

        # 1. 测试API调用限制
        print("\n1. 测试API调用限制")
        # 创建基础版订阅用户
        rate_limit_user_data = {
            "username": "rate_limit_user",
            "email": "rate_limit@example.com",
            "password": "password123",
            "role": "user"
        }
        rate_limit_response = self.auth_service.register(rate_limit_user_data)
        rate_limit_user_id = rate_limit_response["data"]["user_id"]

        # 创建基础版订阅
        subscription_response = self.commerce_service.create_subscription(rate_limit_user_id, "basic")
        assert subscription_response["success"] is True

        # 测试API使用限制
        api_usage_response = self.commerce_service.check_api_usage(rate_limit_user_id)
        assert api_usage_response["success"] is True
        usage = api_usage_response["data"]["usage"]
        assert usage["limit"] == 1000  # 基础版API限制
        print("✅ API使用限制检查通过")

        # 2. 测试信号生成限制
        print("\n2. 测试信号生成限制")
        signal_usage_response = self.commerce_service.check_signal_usage(rate_limit_user_id)
        assert signal_usage_response["success"] is True
        signal_usage = signal_usage_response["data"]["usage"]
        assert signal_usage["limit"] == 10  # 基础版信号限制
        print("✅ 信号生成限制检查通过")

        # 3. 测试速率限制记录
        print("\n3. 测试速率限制记录")
        # 记录API使用
        for i in range(5):
            success = self.commerce_service.record_api_usage(rate_limit_user_id)
            assert success is True

        # 检查API使用记录
        api_usage_response_after = self.commerce_service.check_api_usage(rate_limit_user_id)
        usage_after = api_usage_response_after["data"]["usage"]
        assert usage_after["usage"] >= 5
        print("✅ 速率限制记录功能正常")

        print("\n=== 速率限制测试完成 ===")

    def run_all_security_tests(self):
        """
        运行所有安全测试
        """
        print("==================================================")
        print("           TrendMatrix 安全测试")
        print("==================================================")

        # 运行认证安全性测试
        self.test_authentication_security()

        # 运行输入验证测试
        self.test_input_validation()

        # 运行敏感数据保护测试
        self.test_sensitive_data_protection()

        # 运行速率限制测试
        self.test_rate_limiting()

        print("\n==================================================")
        print("           安全测试完成！")
        print("==================================================")
        print("\n安全测试结果:")
        print("✅ 认证和授权安全测试通过")
        print("✅ 输入验证测试通过")
        print("✅ 敏感数据保护测试通过")
        print("✅ 速率限制测试通过")
        print("\n建议改进:")
        print("1. 添加密码强度检查")
        print("2. 添加暴力破解防护")
        print("3. 在实际Web环境中测试XSS和SQL注入防护")
        print("4. 添加HTTPS加密传输")

if __name__ == "__main__":
    security_test = SecurityTest()
    security_test.run_all_security_tests()
