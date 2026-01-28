# Cache Service
# 缓存服务，实现API响应缓存和性能优化

import os
import time
import hashlib
from typing import Dict, Any, Optional
import json

class CacheService:
    """
    缓存服务
    实现API响应缓存和性能优化
    """

    def __init__(self):
        """
        初始化缓存服务
        """
        # 内存缓存
        self.cache = {}
        
        # 缓存配置
        self.default_ttl = int(os.getenv('CACHE_TTL', '3600'))  # 默认缓存1小时
        self.max_cache_size = int(os.getenv('MAX_CACHE_SIZE', '1000'))  # 最大缓存条目数
        
        # 缓存统计
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def _generate_cache_key(self, endpoint: str, method: str, params: Dict[str, Any]) -> str:
        """
        生成缓存键

        Args:
            endpoint: API端点
            method: HTTP方法
            params: 请求参数

        Returns:
            缓存键
        """
        # 对参数进行排序，确保相同参数生成相同的键
        sorted_params = json.dumps(params, sort_keys=True) if params else ""
        
        # 生成MD5哈希作为缓存键
        cache_key = hashlib.md5(
            f"{endpoint}:{method}:{sorted_params}".encode('utf-8')
        ).hexdigest()
        
        return cache_key

    def get(self, endpoint: str, method: str, params: Dict[str, Any]) -> Optional[Any]:
        """
        获取缓存值

        Args:
            endpoint: API端点
            method: HTTP方法
            params: 请求参数

        Returns:
            缓存的值，如果不存在或已过期则返回None
        """
        cache_key = self._generate_cache_key(endpoint, method, params)
        
        # 检查缓存是否存在
        if cache_key not in self.cache:
            self.misses += 1
            return None
        
        # 获取缓存项
        cache_item = self.cache[cache_key]
        
        # 检查缓存是否过期
        current_time = time.time()
        if current_time > cache_item['expiry']:
            # 缓存过期，移除
            del self.cache[cache_key]
            self.misses += 1
            self.evictions += 1
            return None
        
        # 缓存命中
        self.hits += 1
        return cache_item['value']

    def set(self, endpoint: str, method: str, params: Dict[str, Any], value: Any, ttl: Optional[int] = None) -> bool:
        """
        设置缓存值

        Args:
            endpoint: API端点
            method: HTTP方法
            params: 请求参数
            value: 要缓存的值
            ttl: 缓存过期时间（秒），默认使用配置的TTL

        Returns:
            是否设置成功
        """
        try:
            # 检查缓存大小是否超过限制
            if len(self.cache) >= self.max_cache_size:
                # 移除最旧的缓存项
                self._evict_oldest()
            
            # 生成缓存键
            cache_key = self._generate_cache_key(endpoint, method, params)
            
            # 计算过期时间
            current_time = time.time()
            expiry = current_time + (ttl or self.default_ttl)
            
            # 设置缓存
            self.cache[cache_key] = {
                'value': value,
                'expiry': expiry,
                'created_at': current_time,
                'endpoint': endpoint,
                'method': method
            }
            
            return True
        except Exception:
            return False

    def delete(self, endpoint: str, method: str, params: Dict[str, Any]) -> bool:
        """
        删除缓存值

        Args:
            endpoint: API端点
            method: HTTP方法
            params: 请求参数

        Returns:
            是否删除成功
        """
        try:
            cache_key = self._generate_cache_key(endpoint, method, params)
            if cache_key in self.cache:
                del self.cache[cache_key]
                return True
            return False
        except Exception:
            return False

    def clear(self, endpoint: Optional[str] = None) -> bool:
        """
        清空缓存

        Args:
            endpoint: 可选，指定要清空的端点缓存

        Returns:
            是否清空成功
        """
        try:
            if endpoint:
                # 清空指定端点的缓存
                keys_to_delete = [
                    key for key, item in self.cache.items() 
                    if item['endpoint'] == endpoint
                ]
                for key in keys_to_delete:
                    del self.cache[key]
                    self.evictions += 1
            else:
                # 清空所有缓存
                self.evictions += len(self.cache)
                self.cache.clear()
            return True
        except Exception:
            return False

    def _evict_oldest(self):
        """
        移除最旧的缓存项
        """
        if not self.cache:
            return
        
        # 找到最旧的缓存项
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k]['created_at']
        )
        
        # 移除最旧的缓存项
        del self.cache[oldest_key]
        self.evictions += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            缓存统计信息
        """
        current_time = time.time()
        active_items = 0
        expired_items = 0
        
        # 统计活跃和过期的缓存项
        for cache_item in self.cache.values():
            if current_time < cache_item['expiry']:
                active_items += 1
            else:
                expired_items += 1
        
        return {
            'total_items': len(self.cache),
            'active_items': active_items,
            'expired_items': expired_items,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': (self.hits / (self.hits + self.misses) * 100) if (self.hits + self.misses) > 0 else 0,
            'evictions': self.evictions,
            'max_size': self.max_cache_size,
            'default_ttl': self.default_ttl
        }

    def clean_expired(self) -> int:
        """
        清理过期的缓存项

        Returns:
            清理的过期缓存项数量
        """
        current_time = time.time()
        expired_keys = [
            key for key, item in self.cache.items()
            if current_time > item['expiry']
        ]
        
        for key in expired_keys:
            del self.cache[key]
            self.evictions += 1
        
        return len(expired_keys)

# 创建全局缓存服务实例
cache_service = CacheService()
