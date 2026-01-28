# Auth Service
# 用户认证和授权服务

import logging
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class AuthService:
    """
    用户认证和授权服务
    处理用户登录、注册、令牌管理和权限验证
    """

    def __init__(self, secret_key: str = "your-secret-key", algorithm: str = "HS256", token_expiry: int = 24):
        """
        初始化认证服务

        Args:
            secret_key: JWT签名密钥
            algorithm: JWT算法
            token_expiry: 令牌过期时间（小时）
        """
        self.logger = logging.getLogger(__name__)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry = token_expiry

        # 模拟用户数据库
        self.users_db = {}
        self.roles_db = {
            "admin": ["*"],  # 所有权限
            "user": ["read", "analyze"],  # 只读和分析权限
            "guest": ["read"]  # 仅读取权限
        }

    def register(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户注册

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            # 验证请求参数
            required_params = ['username', 'email', 'password', 'role']
            for param in required_params:
                if param not in request:
                    return self._error_response(f"Missing required parameter: {param}")

            # 验证角色
            if request['role'] not in self.roles_db:
                return self._error_response(f"Invalid role: {request['role']}")

            # 验证用户是否已存在
            if request['username'] in self.users_db:
                return self._error_response("Username already exists")

            if any(user['email'] == request['email'] for user in self.users_db.values()):
                return self._error_response("Email already exists")

            # 哈希密码
            hashed_password = bcrypt.hashpw(
                request['password'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            # 创建用户
            user_id = f"user_{len(self.users_db) + 1}"
            self.users_db[request['username']] = {
                "id": user_id,
                "username": request['username'],
                "email": request['email'],
                "password": hashed_password,
                "role": request['role'],
                "created_at": datetime.now().isoformat()
            }

            # 生成令牌
            token = self._generate_token(user_id, request['username'], request['role'])

            return self._success_response({
                "user_id": user_id,
                "username": request['username'],
                "email": request['email'],
                "role": request['role'],
                "token": token
            })

        except Exception as e:
            self.logger.error(f"Error registering user: {str(e)}")
            return self._error_response(str(e))

    def login(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户登录

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            # 验证请求参数
            required_params = ['username', 'password']
            for param in required_params:
                if param not in request:
                    return self._error_response(f"Missing required parameter: {param}")

            # 验证用户
            user = self.users_db.get(request['username'])
            if not user:
                return self._error_response("Invalid username or password")

            # 验证密码
            if not bcrypt.checkpw(
                request['password'].encode('utf-8'),
                user['password'].encode('utf-8')
            ):
                return self._error_response("Invalid username or password")

            # 生成令牌
            token = self._generate_token(user['id'], user['username'], user['role'])

            return self._success_response({
                "user_id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "token": token
            })

        except Exception as e:
            self.logger.error(f"Error logging in user: {str(e)}")
            return self._error_response(str(e))

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        验证令牌

        Args:
            token: JWT令牌

        Returns:
            验证结果
        """
        try:
            # 解码令牌，添加leeway处理时钟差异
            import time
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_signature": True},
                leeway=30  # 30秒的时间误差
            )

            # 验证令牌过期时间
            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                return self._error_response("Token expired")

            return self._success_response({
                "user_id": payload['sub'],
                "username": payload['username'],
                "role": payload['role'],
                "exp": payload['exp']
            })

        except jwt.ExpiredSignatureError:
            return self._error_response("Token expired")
        except jwt.InvalidTokenError as e:
            self.logger.error(f"Invalid token: {str(e)}")
            return self._error_response(f"Invalid token: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error verifying token: {str(e)}")
            return self._error_response(str(e))

    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """
        检查用户权限

        Args:
            user_role: 用户角色
            required_permission: 所需权限

        Returns:
            是否有权限
        """
        try:
            # 检查角色是否存在
            if user_role not in self.roles_db:
                return False

            # 获取角色权限
            permissions = self.roles_db[user_role]

            # 检查是否有通配符权限
            if '*' in permissions:
                return True

            # 检查是否有所需权限
            return required_permission in permissions

        except Exception as e:
            self.logger.error(f"Error checking permission: {str(e)}")
            return False

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            用户信息
        """
        try:
            # 查找用户
            for user in self.users_db.values():
                if user['id'] == user_id:
                    # 移除密码字段
                    user_info = user.copy()
                    user_info.pop('password')
                    return self._success_response(user_info)

            return self._error_response("User not found")

        except Exception as e:
            self.logger.error(f"Error getting user info: {str(e)}")
            return self._error_response(str(e))

    def update_user(self, user_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            # 查找用户
            user_key = None
            user = None
            for key, value in self.users_db.items():
                if value['id'] == user_id:
                    user_key = key
                    user = value
                    break

            if not user:
                return self._error_response("User not found")

            # 更新用户信息
            if 'email' in request:
                user['email'] = request['email']
            if 'role' in request:
                if request['role'] not in self.roles_db:
                    return self._error_response(f"Invalid role: {request['role']}")
                user['role'] = request['role']
            if 'password' in request:
                # 哈希新密码
                user['password'] = bcrypt.hashpw(
                    request['password'].encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')

            user['updated_at'] = datetime.now().isoformat()
            self.users_db[user_key] = user

            # 移除密码字段
            user_info = user.copy()
            user_info.pop('password')

            return self._success_response(user_info)

        except Exception as e:
            self.logger.error(f"Error updating user: {str(e)}")
            return self._error_response(str(e))

    def logout(self, user_id: str) -> Dict[str, Any]:
        """
        用户登出

        Args:
            user_id: 用户ID

        Returns:
            响应结果
        """
        try:
            # 这里可以实现令牌黑名单等功能
            # 目前简单返回成功
            return {
                "success": True,
                "data": {"message": "Logout successful"},
                "message": "Logout successful"
            }

        except Exception as e:
            self.logger.error(f"Error logging out user: {str(e)}")
            return self._error_response(str(e))

    def _generate_token(self, user_id: str, username: str, role: str) -> str:
        """
        生成JWT令牌

        Args:
            user_id: 用户ID
            username: 用户名
            role: 用户角色

        Returns:
            JWT令牌
        """
        # 设置令牌过期时间
        expiry = datetime.now() + timedelta(hours=self.token_expiry)

        # 创建令牌载荷
        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "iat": int(datetime.now().timestamp()),
            "exp": int(expiry.timestamp())
        }

        # 生成令牌
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )

        return token

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
