# Security Configuration
# 安全配置和安全措施实现

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from jose import JWTError, jwt

# 安全配置类
class SecurityConfig:
    """
    安全配置类
    实现各种安全措施和配置
    """

    def __init__(self):
        """
        初始化安全配置
        """
        # 从环境变量加载配置
        self.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
        self.csrf_secret = os.getenv('CSRF_SECRET', secrets.token_urlsafe(32))
        self.algorithm = os.getenv('ALGORITHM', 'HS256')
        self.access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
        self.refresh_token_expire_days = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '7'))

        # 安全设置
        self.secure_cookies = os.getenv('SECURE_COOKIES', 'true').lower() == 'true'
        self.xss_protection = True
        self.content_security_policy = True
        self.hsts = True

        # 密码策略
        self.password_min_length = 8
        self.password_require_uppercase = True
        self.password_require_lowercase = True
        self.password_require_digit = True
        self.password_require_special = True

        # 速率限制
        self.rate_limit_per_minute = int(os.getenv('API_RATE_LIMIT_PER_MINUTE', '1000'))
        self.rate_limit_per_hour = int(os.getenv('API_RATE_LIMIT_PER_HOUR', '10000'))

    def validate_password(self, password: str) -> Dict[str, Any]:
        """
        验证密码强度

        Args:
            password: 密码字符串

        Returns:
            验证结果
        """
        errors = []

        # 检查密码长度
        if len(password) < self.password_min_length:
            errors.append(f"Password must be at least {self.password_min_length} characters long")

        # 检查大写字母
        if self.password_require_uppercase and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

        # 检查小写字母
        if self.password_require_lowercase and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")

        # 检查数字
        if self.password_require_digit and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")

        # 检查特殊字符
        if self.password_require_special and not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?~' for c in password):
            errors.append("Password must contain at least one special character")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def generate_csrf_token(self, user_id: str) -> str:
        """
        生成CSRF令牌

        Args:
            user_id: 用户ID

        Returns:
            CSRF令牌
        """
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        return jwt.encode(payload, self.csrf_secret, algorithm=self.algorithm)

    def validate_csrf_token(self, token: str) -> Dict[str, Any]:
        """
        验证CSRF令牌

        Args:
            token: CSRF令牌

        Returns:
            验证结果
        """
        try:
            payload = jwt.decode(token, self.csrf_secret, algorithms=[self.algorithm])
            return {
                "valid": True,
                "user_id": payload.get("sub")
            }
        except JWTError:
            return {
                "valid": False,
                "error": "Invalid CSRF token"
            }

    def hash_password(self, password: str) -> str:
        """
        哈希密码

        Args:
            password: 原始密码

        Returns:
            哈希后的密码
        """
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码

        Args:
            plain_password: 原始密码
            hashed_password: 哈希后的密码

        Returns:
            验证结果
        """
        import bcrypt
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def generate_secure_token(self, length: int = 32) -> str:
        """
        生成安全令牌

        Args:
            length: 令牌长度

        Returns:
            安全令牌
        """
        return secrets.token_urlsafe(length)

    def get_security_headers(self) -> Dict[str, str]:
        """
        获取安全头部

        Returns:
            安全头部字典
        """
        headers = {
            # 防止XSS攻击
            "X-XSS-Protection": "1; mode=block",

            # 防止MIME类型嗅探
            "X-Content-Type-Options": "nosniff",

            # 防止点击劫持
            "X-Frame-Options": "DENY",

            # 强制HTTPS
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",

            # 内容安全策略
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none'",

            # 引用策略
            "Referrer-Policy": "strict-origin-when-cross-origin",

            # 功能策略
            "Feature-Policy": "camera 'none'; microphone 'none'; geolocation 'none'; payment 'none'"
        }

        return headers

# 创建安全配置实例
security_config = SecurityConfig()

# 安全中间件
def add_security_middlewares(app):
    """
    添加安全中间件到FastAPI应用

    Args:
        app: FastAPI应用实例
    """
    # 信任主机中间件
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # 在生产环境中应该设置具体的主机名
    )

    # GZIP压缩中间件
    app.add_middleware(GZipMiddleware, minimum_size=1000)

# 安全头部中间件函数
def create_security_headers_middleware():
    """
    创建安全头部中间件
    """
    async def security_headers_middleware(request: Request, call_next):
        """
        添加安全头部的中间件
        """
        response = await call_next(request)

        # 添加安全头部
        security_headers = security_config.get_security_headers()
        for key, value in security_headers.items():
            response.headers[key] = value

        return response
    return security_headers_middleware

# 密码策略验证
async def validate_password_strength(password: str) -> bool:
    """
    验证密码强度

    Args:
        password: 密码字符串

    Returns:
        验证结果
    """
    result = security_config.validate_password(password)
    return result["valid"]

# CSRF保护装饰器
def csrf_protect(func):
    """
    CSRF保护装饰器
    """
    async def wrapper(request: Request, *args, **kwargs):
        # 从请求头获取CSRF令牌
        csrf_token = request.headers.get("X-CSRF-Token")

        if not csrf_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Missing CSRF token"
            )

        # 验证CSRF令牌
        validation = security_config.validate_csrf_token(csrf_token)
        if not validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token"
            )

        # 继续处理请求
        return await func(request, *args, **kwargs)

    return wrapper
