# 用户验收测试脚本

from api.auth_service import AuthService
from commerce.api.commerce_api_service import CommerceAPIService
from api.main_api_service import MainAPIService

class UserAcceptanceTest:
    """
    用户验收测试类
    """

    def __init__(self):
        """
        初始化用户验收测试
        """
        self.auth_service = AuthService()
        self.commerce_service = CommerceAPIService()
        self.main_api_service = MainAPIService(
            auth_service=self.auth_service,
            commerce_api_service=self.commerce_service
        )

    def test_user_registration_and_login(self):
        """
        测试用户注册和登录流程
        """
        print("\n=== 测试场景 1: 用户注册和登录 ===")

        # 1. 测试用户注册
        print("\n1. 测试用户注册")
        register_data = {
            "username": "acceptance_user",
            "email": "acceptance@example.com",
            "password": "Password123!",
            "role": "user"
        }
        register_response = self.auth_service.register(register_data)
        assert register_response["success"] is True
        user_id = register_response["data"]["user_id"]
        print(f"✅ 用户注册成功: {user_id}")

        # 2. 测试用户登录
        print("\n2. 测试用户登录")
        login_data = {
            "username": "acceptance_user",
            "password": "Password123!"
        }
        login_response = self.auth_service.login(login_data)
        assert login_response["success"] is True
        token = login_response["data"]["token"]
        print("✅ 用户登录成功")

        # 3. 测试令牌验证
        print("\n3. 测试令牌验证")
        verify_response = self.auth_service.verify_token(token)
        assert verify_response["success"] is True
        print("✅ 令牌验证成功")

        print("\n=== 场景 1 测试完成 ===")

    def test_subscription_management(self):
        """
        测试订阅管理流程
        """
        print("\n=== 测试场景 2: 订阅管理 ===")

        # 1. 准备测试用户
        print("\n1. 准备测试用户")
        user_data = {
            "username": "subscription_user",
            "email": "subscription@example.com",
            "password": "Password123!",
            "role": "user"
        }
        user_response = self.auth_service.register(user_data)
        assert user_response["success"] is True
        user_id = user_response["data"]["user_id"]
        print(f"✅ 测试用户准备成功: {user_id}")

        # 2. 测试获取订阅计划
        print("\n2. 测试获取订阅计划")
        plans_response = self.commerce_service.get_plans()
        assert plans_response["success"] is True
        plans = plans_response["data"]["plans"]
        assert "basic" in plans
        assert "professional" in plans
        assert "enterprise" in plans
        print("✅ 订阅计划获取成功")

        # 3. 测试创建基础版订阅
        print("\n3. 测试创建基础版订阅")
        subscription_response = self.commerce_service.create_subscription(user_id, "basic")
        assert subscription_response["success"] is True
        subscription = subscription_response["data"]["subscription"]
        assert subscription["plan_id"] == "basic"
        print("✅ 基础版订阅创建成功")

        # 4. 测试获取用户订阅信息
        print("\n4. 测试获取用户订阅信息")
        get_subscription_response = self.commerce_service.get_user_subscription(user_id)
        assert get_subscription_response["success"] is True
        user_subscription = get_subscription_response["data"]["subscription"]
        assert user_subscription["plan_id"] == "basic"
        print("✅ 用户订阅信息获取成功")

        # 5. 测试订阅升级
        print("\n5. 测试订阅升级")
        update_response = self.commerce_service.update_subscription(user_id, "professional")
        assert update_response["success"] is True
        updated_subscription = update_response["data"]["subscription"]
        assert updated_subscription["plan_id"] == "professional"
        print("✅ 订阅升级成功")

        # 6. 测试取消订阅
        print("\n6. 测试取消订阅")
        cancel_response = self.commerce_service.cancel_subscription(user_id)
        assert cancel_response["success"] is True
        cancelled_subscription = cancel_response["data"]["subscription"]
        assert cancelled_subscription["status"] == "cancelled"
        print("✅ 订阅取消成功")

        print("\n=== 场景 2 测试完成 ===")

    def test_payment_processing(self):
        """
        测试支付处理流程
        """
        print("\n=== 测试场景 3: 支付处理 ===")

        # 1. 准备测试用户
        print("\n1. 准备测试用户")
        user_data = {
            "username": "payment_user",
            "email": "payment@example.com",
            "password": "Password123!",
            "role": "user"
        }
        user_response = self.auth_service.register(user_data)
        assert user_response["success"] is True
        user_id = user_response["data"]["user_id"]
        print(f"✅ 测试用户准备成功: {user_id}")

        # 2. 测试添加支付方式
        print("\n2. 测试添加支付方式")
        payment_data = {
            "type": "credit_card",
            "name": "Test Credit Card",
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        add_payment_response = self.commerce_service.add_payment_method(user_id, payment_data)
        assert add_payment_response["success"] is True
        payment_method_id = add_payment_response["data"]["payment_method"]["payment_method_id"]
        print(f"✅ 支付方式添加成功: {payment_method_id}")

        # 3. 测试获取用户支付方式
        print("\n3. 测试获取用户支付方式")
        get_payment_response = self.commerce_service.get_user_payment_methods(user_id)
        assert get_payment_response["success"] is True
        payment_methods = get_payment_response["data"]["payment_methods"]
        assert len(payment_methods) > 0
        print("✅ 用户支付方式获取成功")

        # 4. 测试设置默认支付方式
        print("\n4. 测试设置默认支付方式")
        set_default_response = self.commerce_service.set_default_payment_method(user_id, payment_method_id)
        assert set_default_response["success"] is True
        print("✅ 默认支付方式设置成功")

        # 5. 测试处理支付
        print("\n5. 测试处理支付")
        payment_request = {
            "amount": 99.0,
            "currency": "USD",
            "description": "Test Payment",
            "payment_method_id": payment_method_id
        }
        payment_response = self.commerce_service.process_payment(user_id, payment_request)
        assert payment_response["success"] is True
        transaction_id = payment_response["data"]["transaction"]["transaction_id"]
        print(f"✅ 支付处理成功: {transaction_id}")

        # 6. 测试获取交易历史
        print("\n6. 测试获取交易历史")
        history_response = self.commerce_service.get_transaction_history(user_id)
        assert history_response["success"] is True
        transactions = history_response["data"]["transactions"]
        assert len(transactions) > 0
        print("✅ 交易历史获取成功")

        print("\n=== 场景 3 测试完成 ===")

    def test_usage_limits(self):
        """
        测试使用限制功能
        """
        print("\n=== 测试场景 4: 使用限制 ===")

        # 1. 准备测试用户
        print("\n1. 准备测试用户")
        user_data = {
            "username": "limits_user",
            "email": "limits@example.com",
            "password": "Password123!",
            "role": "user"
        }
        user_response = self.auth_service.register(user_data)
        assert user_response["success"] is True
        user_id = user_response["data"]["user_id"]
        print(f"✅ 测试用户准备成功: {user_id}")

        # 2. 测试创建基础版订阅
        print("\n2. 测试创建基础版订阅")
        subscription_response = self.commerce_service.create_subscription(user_id, "basic")
        assert subscription_response["success"] is True
        print("✅ 基础版订阅创建成功")

        # 3. 测试API使用限制
        print("\n3. 测试API使用限制")
        api_usage_response = self.commerce_service.check_api_usage(user_id)
        assert api_usage_response["success"] is True
        api_usage = api_usage_response["data"]["usage"]
        assert api_usage["limit"] == 1000  # 基础版API限制
        print(f"✅ API使用限制检查成功: {api_usage['limit']} 次/月")

        # 4. 测试信号生成限制
        print("\n4. 测试信号生成限制")
        signal_usage_response = self.commerce_service.check_signal_usage(user_id)
        assert signal_usage_response["success"] is True
        signal_usage = signal_usage_response["data"]["usage"]
        assert signal_usage["limit"] == 10  # 基础版信号限制
        print(f"✅ 信号生成限制检查成功: {signal_usage['limit']} 次/天")

        # 5. 测试使用记录
        print("\n5. 测试使用记录")
        # 记录API使用
        for i in range(3):
            success = self.commerce_service.record_api_usage(user_id)
            assert success is True
        # 检查API使用记录
        api_usage_response_after = self.commerce_service.check_api_usage(user_id)
        assert api_usage_response_after["success"] is True
        usage_after = api_usage_response_after["data"]["usage"]
        assert usage_after["usage"] >= 3
        print(f"✅ API使用记录成功: 已使用 {usage_after['usage']} 次")

        print("\n=== 场景 4 测试完成 ===")

    def test_service_integration(self):
        """
        测试服务集成
        """
        print("\n=== 测试场景 5: 服务集成 ===")

        # 1. 测试获取服务信息
        print("\n1. 测试获取服务信息")
        service_info_response = self.main_api_service.get_service_info()
        assert service_info_response["success"] is True
        service_info = service_info_response["data"]
        assert "api_version" in service_info
        assert "services" in service_info
        assert "endpoints" in service_info
        print(f"✅ 服务信息获取成功，API版本: {service_info['api_version']}")

        # 2. 测试服务状态
        print("\n2. 测试服务状态")
        services = service_info["services"]
        assert services["auth"] is True
        assert services["commerce"] is True
        print("✅ 服务状态检查成功")

        # 3. 测试端点列表
        print("\n3. 测试端点列表")
        endpoints = service_info["endpoints"]
        assert len(endpoints) > 0
        print(f"✅ 端点列表获取成功，共 {len(endpoints)} 个端点")

        print("\n=== 场景 5 测试完成 ===")

    def run_all_acceptance_tests(self):
        """
        运行所有用户验收测试
        """
        print("==================================================")
        print("           TrendMatrix 用户验收测试")
        print("==================================================")

        # 运行场景 1: 用户注册和登录
        self.test_user_registration_and_login()

        # 运行场景 2: 订阅管理
        self.test_subscription_management()

        # 运行场景 3: 支付处理
        self.test_payment_processing()

        # 运行场景 4: 使用限制
        self.test_usage_limits()

        # 运行场景 5: 服务集成
        self.test_service_integration()

        print("\n==================================================")
        print("           用户验收测试完成！")
        print("==================================================")
        print("\n测试结果总结:")
        print("✅ 所有测试场景通过")
        print("✅ 系统功能满足用户需求")
        print("✅ 核心流程运行正常")
        print("\n建议:")
        print("1. 为生产环境添加更严格的安全措施")
        print("2. 优化系统性能以支持更多并发用户")
        print("3. 完善用户界面，提升用户体验")

if __name__ == "__main__":
    uat = UserAcceptanceTest()
    uat.run_all_acceptance_tests()
