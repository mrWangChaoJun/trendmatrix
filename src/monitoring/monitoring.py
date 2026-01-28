# Monitoring Configuration
# 监控配置和指标收集

import os
import time
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化Sentry
sentry_dsn = os.getenv('SENTRY_DSN')
if sentry_dsn and sentry_dsn != 'your-sentry-dsn':
    try:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FastApiIntegration(),
                RedisIntegration(),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        print("Sentry initialized successfully")
    except Exception as e:
        print(f"Error initializing Sentry: {e}")
else:
    print("Sentry not initialized (DSN not configured)")

# Prometheus指标定义

# 请求计数
REQUEST_COUNT = Counter(
    'trendmatrix_request_count',
    'Total number of requests',
    ['endpoint', 'method', 'status']
)

# 请求延迟
REQUEST_LATENCY = Histogram(
    'trendmatrix_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint', 'method']
)

# 系统健康状态
SYSTEM_HEALTH = Gauge(
    'trendmatrix_system_health',
    'System health status (1=healthy, 0=unhealthy)'
)

# API服务状态
API_SERVICE_STATUS = Gauge(
    'trendmatrix_api_service_status',
    'API service status (1=healthy, 0=unhealthy)',
    ['service']
)

# 信号生成计数
SIGNAL_GENERATION_COUNT = Counter(
    'trendmatrix_signal_generation_count',
    'Total number of signals generated',
    ['signal_type', 'success']
)

# Solana分析计数
SOLANA_ANALYSIS_COUNT = Counter(
    'trendmatrix_solana_analysis_count',
    'Total number of Solana analyses',
    ['analysis_type', 'success']
)

# 错误计数
ERROR_COUNT = Counter(
    'trendmatrix_error_count',
    'Total number of errors',
    ['error_type', 'endpoint']
)

# 系统资源使用
SYSTEM_CPU_USAGE = Gauge(
    'trendmatrix_system_cpu_usage',
    'System CPU usage percentage'
)

SYSTEM_MEMORY_USAGE = Gauge(
    'trendmatrix_system_memory_usage',
    'System memory usage percentage'
)

# 初始化监控服务
def initialize_monitoring():
    """初始化监控服务"""
    # 启动Prometheus指标服务器
    prometheus_enabled = os.getenv('PROMETHEUS_ENABLED', 'true').lower() == 'true'
    if prometheus_enabled:
        try:
            # 启动Prometheus指标服务器在9091端口
            start_http_server(9091)
            print("Prometheus metrics server started on port 9091")
        except Exception as e:
            print(f"Error starting Prometheus metrics server: {e}")

    # 设置初始健康状态
    SYSTEM_HEALTH.set(1)

    # 设置初始服务状态
    API_SERVICE_STATUS.labels(service='signals').set(1)
    API_SERVICE_STATUS.labels(service='solana').set(1)
    API_SERVICE_STATUS.labels(service='auth').set(0)
    API_SERVICE_STATUS.labels(service='commerce').set(0)

# 更新系统健康状态
def update_system_health(healthy):
    """更新系统健康状态"""
    SYSTEM_HEALTH.set(1 if healthy else 0)

# 更新API服务状态
def update_api_service_status(service, healthy):
    """更新API服务状态"""
    API_SERVICE_STATUS.labels(service=service).set(1 if healthy else 0)

# 记录请求
def record_request(endpoint, method, status, latency):
    """记录请求"""
    REQUEST_COUNT.labels(endpoint=endpoint, method=method, status=status).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint, method=method).observe(latency)

# 记录信号生成
def record_signal_generation(signal_type, success):
    """记录信号生成"""
    SIGNAL_GENERATION_COUNT.labels(signal_type=signal_type, success=success).inc()

# 记录Solana分析
def record_solana_analysis(analysis_type, success):
    """记录Solana分析"""
    SOLANA_ANALYSIS_COUNT.labels(analysis_type=analysis_type, success=success).inc()

# 记录错误
def record_error(error_type, endpoint):
    """记录错误"""
    ERROR_COUNT.labels(error_type=error_type, endpoint=endpoint).inc()

# 更新系统资源使用
def update_system_resources():
    """更新系统资源使用"""
    try:
        import psutil
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        SYSTEM_CPU_USAGE.set(cpu_usage)
        SYSTEM_MEMORY_USAGE.set(memory_usage)

        return cpu_usage, memory_usage
    except Exception as e:
        print(f"Error updating system resources: {e}")
        return 0, 0

# 健康检查扩展
def get_detailed_health_status():
    """获取详细的健康状态"""
    from app import TrendMatrixApp

    try:
        app_instance = TrendMatrixApp()
        main_api_service = app_instance.get_main_api_service()

        # 获取服务信息
        service_info = main_api_service.get_service_info() if main_api_service else {}

        # 更新系统资源
        cpu_usage, memory_usage = update_system_resources()

        health_status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'services': {
                'api': main_api_service is not None,
                'signals': service_info.get('data', {}).get('services', {}).get('signals', False),
                'solana': service_info.get('data', {}).get('services', {}).get('solana', False),
                'auth': service_info.get('data', {}).get('services', {}).get('auth', False),
                'commerce': service_info.get('data', {}).get('services', {}).get('commerce', False)
            },
            'resources': {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage
            },
            'metrics': {
                'request_count': 0,  # 暂时设置为0，需要使用正确的方法获取
                'error_count': 0,  # 暂时设置为0，需要使用正确的方法获取
                'signal_count': 0,  # 暂时设置为0，需要使用正确的方法获取
                'solana_analysis_count': 0  # 暂时设置为0，需要使用正确的方法获取
            }
        }

        # 更新健康状态
        all_services_healthy = all(health_status['services'].values())
        update_system_health(all_services_healthy)

        return health_status

    except Exception as e:
        update_system_health(False)
        return {
            'status': 'unhealthy',
            'timestamp': time.time(),
            'error': str(e)
        }
