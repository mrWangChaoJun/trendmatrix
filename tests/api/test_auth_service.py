# 认证服务测试用例

import pytest
from api.auth_service import AuthService

class TestAuthService:
    """
    认证服务测试类
    """

    def setup_method(self):
        """
        测试方法设置
        """
        self.auth_service = AuthService()

    def test_register_success(self):
        """
        测试用户注册成功
        """
        # 准备测试数据
        request_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }

        # 执行注册
        response = self.auth_service.register(request_data)

        # 验证响应
        assert response["success"] is True
        assert "user_id" in response["data"]
        assert response["data"]["username"] == "testuser"
        assert response["data"]["email"] == "test@example.com"
        assert response["data"]["role"] == "user"
        assert "token" in response["data"]

    def test_register_missing_params(self):
        """
        测试注册缺少参数
        """
        # 缺少用户名
        request_data = {
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }

        response = self.auth_service.register(request_data)
        assert response["success"] is False
        assert "Missing required parameter: username" in response["message"]

    def test_register_invalid_role(self):
        """
        测试注册无效角色
        """
        request_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "invalid_role"
        }

        response = self.auth_service.register(request_data)
        assert response["success"] is False
        assert "Invalid role: invalid_role" in response["message"]

    def test_register_existing_user(self):
        """
        测试注册已存在用户
        """
        # 先注册一个用户
        request_data1 = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        self.auth_service.register(request_data1)

        # 尝试使用相同用户名注册
        request_data2 = {
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123",
            "role": "user"
        }
        response = self.auth_service.register(request_data2)
        assert response["success"] is False
        assert "Username already exists" in response["message"]

    def test_login_success(self):
        """
        测试登录成功
        """
        # 先注册一个用户
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        self.auth_service.register(register_data)

        # 尝试登录
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.auth_service.login(login_data)

        # 验证响应
        assert response["success"] is True
        assert "user_id" in response["data"]
        assert response["data"]["username"] == "testuser"
        assert response["data"]["email"] == "test@example.com"
        assert response["data"]["role"] == "user"
        assert "token" in response["data"]

    def test_login_invalid_credentials(self):
        """
        测试登录无效凭据
        """
        # 尝试使用不存在的用户登录
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = self.auth_service.login(login_data)
        assert response["success"] is False
        assert "Invalid username or password" in response["message"]

        # 注册用户后使用错误密码登录
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        self.auth_service.register(register_data)

        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.auth_service.login(login_data)
        assert response["success"] is False
        assert "Invalid username or password" in response["message"]

    def test_verify_token(self):
        """
        测试令牌验证
        """
        # 注册用户并获取令牌
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        register_response = self.auth_service.register(register_data)
        token = register_response["data"]["token"]

        # 验证令牌
        response = self.auth_service.verify_token(token)
        assert response["success"] is True
        assert "user_id" in response["data"]
        assert "username" in response["data"]
        assert "role" in response["data"]

    def test_check_permission(self):
        """
        测试权限检查
        """
        # 测试管理员权限
        assert self.auth_service.check_permission("admin", "read") is True
        assert self.auth_service.check_permission("admin", "write") is True
        assert self.auth_service.check_permission("admin", "delete") is True

        # 测试用户权限
        assert self.auth_service.check_permission("user", "read") is True
        assert self.auth_service.check_permission("user", "analyze") is True
        assert self.auth_service.check_permission("user", "delete") is False

        # 测试访客权限
        assert self.auth_service.check_permission("guest", "read") is True
        assert self.auth_service.check_permission("guest", "analyze") is False
        assert self.auth_service.check_permission("guest", "write") is False

        # 测试无效角色
        assert self.auth_service.check_permission("invalid", "read") is False

    def test_get_user_info(self):
        """
        测试获取用户信息
        """
        # 注册用户
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        register_response = self.auth_service.register(register_data)
        user_id = register_response["data"]["user_id"]

        # 获取用户信息
        response = self.auth_service.get_user_info(user_id)
        assert response["success"] is True
        assert response["data"]["id"] == user_id
        assert response["data"]["username"] == "testuser"
        assert response["data"]["email"] == "test@example.com"
        assert response["data"]["role"] == "user"
        assert "password" not in response["data"]

        # 获取不存在的用户信息
        response = self.auth_service.get_user_info("nonexistent")
        assert response["success"] is False
        assert "User not found" in response["message"]

    def test_update_user(self):
        """
        测试更新用户信息
        """
        # 注册用户
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        register_response = self.auth_service.register(register_data)
        user_id = register_response["data"]["user_id"]

        # 更新用户邮箱
        update_data = {
            "email": "newemail@example.com"
        }
        response = self.auth_service.update_user(user_id, update_data)
        assert response["success"] is True
        assert response["data"]["email"] == "newemail@example.com"

        # 更新用户角色
        update_data = {
            "role": "admin"
        }
        response = self.auth_service.update_user(user_id, update_data)
        assert response["success"] is True
        assert response["data"]["role"] == "admin"

        # 更新用户密码
        update_data = {
            "password": "newpassword123"
        }
        response = self.auth_service.update_user(user_id, update_data)
        assert response["success"] is True

        # 验证密码更新成功
        login_data = {
            "username": "testuser",
            "password": "newpassword123"
        }
        login_response = self.auth_service.login(login_data)
        assert login_response["success"] is True

    def test_logout(self):
        """
        测试用户登出
        """
        # 注册用户
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
        register_response = self.auth_service.register(register_data)
        user_id = register_response["data"]["user_id"]

        # 测试登出
        response = self.auth_service.logout(user_id)
        assert response["success"] is True
        assert "Logout successful" in response["message"]

if __name__ == "__main__":
    pytest.main([__file__])
