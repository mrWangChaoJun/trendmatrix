# 系统测试脚本

import time
from api.main_api_service import MainAPIService
from commerce.api.commerce_api_service import CommerceAPIService
from api.auth_service import AuthService

class SystemTest:
    """
    系统测试类
    """

    def __init__(self):
        """
        初始化系统测试
        """
        # 初始化服务
        self.auth_service = AuthService()
        self.commerce_service = CommerceAPIService()
        self.main_api_service = MainAPIService(
            auth_service=self.auth_service,
            commerce_api_service=self.commerce_service
        )

    def test_system_integration(self):
        """
        测试系统集成
        """
        print("\n=== 开始系统集成测试 ===")

        # 1. 测试用户注册
        print("\n1. 测试用户注册")
        register_data = {
            "username": "system_test_user",
            "email": "system_test@example.com",
            "password": "password123",
            "role": "user"
        }
        register_response = self.auth_service.register(register_data)
        assert register_response["success"] is True
        user_id = register_response["data"]["user_id"]
        token = register_response["data"]["token"]
        print(f"✅ 用户注册成功: {user_id}")

        # 2. 测试用户登录
        print("\n2. 测试用户登录")
        login_data = {
            "username": "system_test_user",
            "password": "password123"
        }
        login_response = self.auth_service.login(login_data)
        assert login_response["success"] is True
        print("✅ 用户登录成功")

        # 3. 测试令牌验证
        print("\n3. 测试令牌验证")
        verify_response = self.auth_service.verify_token(token)
        assert verify_response["success"] is True
        print("✅ 令牌验证成功")

        # 4. 测试订阅管理
        print("\n4. 测试订阅管理")
        # 创建基础版订阅
        subscription_response = self.commerce_service.create_subscription(user_id, "basic")
        assert subscription_response["success"] is True
        print("✅ 创建基础版订阅成功")

        # 5. 测试支付方式管理
        print("\n5. 测试支付方式管理")
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
        print(f"✅ 添加支付方式成功: {payment_method_id}")

        # 6. 测试支付处理
        print("\n6. 测试支付处理")
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

        # 7. 测试订阅升级
        print("\n7. 测试订阅升级")
        update_response = self.commerce_service.update_subscription(user_id, "professional")
        assert update_response["success"] is True
        print("✅ 订阅升级成功")

        # 8. 测试使用限制
        print("\n8. 测试使用限制")
        api_usage_response = self.commerce_service.check_api_usage(user_id)
        assert api_usage_response["success"] is True
        print("✅ API使用限制检查成功")

        signal_usage_response = self.commerce_service.check_signal_usage(user_id)
        assert signal_usage_response["success"] is True
        print("✅ 信号使用限制检查成功")

        # 9. 测试交易历史
        print("\n9. 测试交易历史")
        history_response = self.commerce_service.get_transaction_history(user_id)
        assert history_response["success"] is True
        assert len(history_response["data"]["transactions"]) > 0
        print("✅ 交易历史查询成功")

        # 10. 测试服务信息
        print("\n10. 测试服务信息")
        service_info_response = self.main_api_service.get_service_info()
        assert service_info_response["success"] is True
        assert "api_version" in service_info_response["data"]
        assert "services" in service_info_response["data"]
        print("✅ 服务信息查询成功")

        print("\n=== 系统集成测试完成 ===")
        print("✅ 所有测试用例通过！")

    def test_performance(self):
        """
        测试系统性能
        """
        print("\n=== 开始性能测试 ===")

        # 1. 测试API响应时间
        print("\n1. 测试API响应时间")
        response_times = []

        # 测试用户登录响应时间
        login_data = {
            "username": "system_test_user",
            "password": "password123"
        }

        for i in range(5):
            start_time = time.time()
            login_response = self.auth_service.login(login_data)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # 转换为毫秒
            response_times.append(response_time)
            print(f"  登录响应时间 #{i+1}: {response_time:.2f}ms")

        average_response_time = sum(response_times) / len(response_times)
        print(f"\n✅ 平均登录响应时间: {average_response_time:.2f}ms")
        assert average_response_time < 500, f"响应时间过长: {average_response_time:.2f}ms"

        # 2. 测试并发处理能力
        print("\n2. 测试并发处理能力")
        import concurrent.futures

        def test_concurrent_login():
            login_data = {
                "username": "system_test_user",
                "password": "password123"
            }
            start_time = time.time()
            response = self.auth_service.login(login_data)
            end_time = time.time()
            return (response["success"], end_time - start_time)

        # 测试5个并发请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test_concurrent_login) for _ in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # 检查所有请求是否成功
        all_success = all(result[0] for result in results)
        assert all_success, "并发请求失败"

        # 计算平均响应时间
        total_time = sum(result[1] for result in results)
        avg_time = (total_time / len(results)) * 1000
        print(f"✅ 5个并发请求成功，平均响应时间: {avg_time:.2f}ms")

        # 3. 测试订阅创建性能
        print("\n3. 测试订阅创建性能")
        create_times = []

        for i in range(3):
            test_user_id = f"perf_test_user_{i}"
            start_time = time.time()
            # 创建临时用户
            register_data = {
                "username": test_user_id,
                "email": f"{test_user_id}@example.com",
                "password": "password123",
                "role": "user"
            }
            self.auth_service.register(register_data)
            # 创建订阅
            response = self.commerce_service.create_subscription(test_user_id, "basic")
            end_time = time.time()
            create_time = (end_time - start_time) * 1000
            create_times.append(create_time)
            print(f"  订阅创建时间 #{i+1}: {create_time:.2f}ms")

        avg_create_time = sum(create_times) / len(create_times)
        print(f"\n✅ 平均订阅创建时间: {avg_create_time:.2f}ms")
        assert avg_create_time < 1000, f"订阅创建时间过长: {avg_create_time:.2f}ms"

        print("\n=== 性能测试完成 ===")
        print("✅ 所有性能测试通过！")

    def run_all_tests(self):
        """
        运行所有系统测试
        """
        print("==================================================")
        print("           TrendMatrix 系统测试")
        print("==================================================")

        # 运行系统集成测试
        self.test_system_integration()

        # 运行性能测试
        self.test_performance()

        print("\n==================================================")
        print("           系统测试全部通过！")
        print("==================================================")

if __name__ == "__main__":
    system_test = SystemTest()
    system_test.run_all_tests()
