# FastAPI Server
# 初始化FastAPI应用并启动服务器

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
import time
from dotenv import load_dotenv

from app import TrendMatrixApp
from api.main_api_service import MainAPIService
from monitoring.monitoring import (
    initialize_monitoring,
    record_request,
    record_error,
    get_detailed_health_status,
    update_system_health
)
from cache.cache_service import cache_service
from security.security import security_config, add_security_middlewares

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化监控
initialize_monitoring()

# 创建TrendMatrix应用实例
trendmatrix_app = TrendMatrixApp()

# 获取主API服务实例
main_api_service = trendmatrix_app.get_main_api_service()

# 创建FastAPI应用实例
app = FastAPI(
    title="TrendMatrix API",
    description="Solana blockchain analysis and trading signals API",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 配置CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加安全中间件
add_security_middlewares(app)

# 安全头部中间件
@app.middleware("http")
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

# 请求监控和缓存中间件
@app.middleware("http")
async def request_monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    method = request.method
    body = {}

    try:
        # 对于GET请求，直接检查缓存
        if method == "GET":
            # 检查缓存
            cached_response = cache_service.get(endpoint, method, body)
            if cached_response:
                # 缓存命中，直接返回
                latency = time.time() - start_time
                record_request(endpoint, method, 200, latency)

                # 创建响应
                response = JSONResponse(
                    status_code=200,
                    content=cached_response
                )

                # 添加安全头部
                security_headers = security_config.get_security_headers()
                for key, value in security_headers.items():
                    response.headers[key] = value

                return response

        # 缓存未命中，执行请求
        response = await call_next(request)
        latency = time.time() - start_time

        # 记录请求
        status = response.status_code
        record_request(endpoint, method, status, latency)

        # 对于成功的响应，缓存结果（只缓存GET请求，避免POST请求体读取问题）
        if status == 200 and method == "GET":
            # 读取响应体
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # 解析响应体
            import json
            try:
                response_data = json.loads(response_body.decode('utf-8'))

                # 缓存响应
                cache_service.set(endpoint, method, body, response_data)
            except:
                pass

            # 重新构建响应
            response = JSONResponse(
                status_code=status,
                content=json.loads(response_body.decode('utf-8'))
            )

        return response
    except Exception as e:
        latency = time.time() - start_time

        # 记录错误
        record_error(type(e).__name__, endpoint)
        record_request(endpoint, method, 500, latency)

        raise

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "data": None
        }
    )

# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "TrendMatrix API"
    }

# 详细健康状态端点
@app.get("/health/detailed")
async def detailed_health_check():
    return get_detailed_health_status()

# 缓存统计端点
@app.get("/cache/stats")
async def get_cache_stats():
    return cache_service.get_stats()

# 清除缓存端点
@app.post("/cache/clear")
async def clear_cache(endpoint: str = None):
    success = cache_service.clear(endpoint)
    return {
        "success": success,
        "message": f"Cache cleared {'for endpoint: ' + endpoint if endpoint else 'completely'}"
    }

# 服务信息端点
@app.get("/api/service/info")
async def get_service_info():
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_service_info()

# 认证端点
@app.post("/api/auth/register")
async def register(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.register(request)

@app.post("/api/auth/login")
async def login(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.login(request)

@app.post("/api/auth/verify")
async def verify_token(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.verify_token(request)

@app.post("/api/auth/user-info")
async def get_user_info(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_user_info(request)

@app.post("/api/auth/update")
async def update_user(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.update_user(request)

@app.post("/api/auth/logout")
async def logout(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.logout(request)

# 信号系统端点
@app.post("/api/signals/generate")
async def generate_signal(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.generate_signal(request)

@app.post("/api/signals/generate-from-ai")
async def generate_signal_from_ai(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.generate_signal_from_ai(request)

@app.post("/api/signals/evaluate")
async def evaluate_signal(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.evaluate_signal(request)

@app.post("/api/signals/classify")
async def classify_signal(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.classify_signal(request)

@app.post("/api/thresholds/set")
async def set_user_thresholds(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.set_user_thresholds(request)

@app.post("/api/thresholds/get")
async def get_user_thresholds(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_user_thresholds(request)

@app.get("/api/history/signals")
async def get_signal_history(limit: int = 5):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_signal_history({"limit": limit})

@app.post("/api/history/statistics")
async def get_signal_statistics(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_signal_statistics(request)

@app.post("/api/history/accuracy")
async def get_accuracy_tracking(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_accuracy_tracking(request)

@app.post("/api/history/update-outcome")
async def update_signal_outcome(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.update_signal_outcome(request)

@app.post("/api/notifications/history")
async def get_notification_history(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_notification_history(request)

# Solana生态分析端点
@app.post("/api/solana/analyze-project")
async def analyze_solana_project(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.analyze_solana_project(request)

@app.post("/api/solana/analyze-developer")
async def analyze_solana_developer(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.analyze_solana_developer(request)

@app.post("/api/solana/analyze-nft")
async def analyze_solana_nft(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.analyze_solana_nft(request)

@app.post("/api/solana/analyze-defi")
async def analyze_solana_defi(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.analyze_solana_defi(request)

@app.post("/api/solana/analyze-multiple-projects")
async def analyze_multiple_solana_projects(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.analyze_multiple_solana_projects(request)

@app.post("/api/solana/visualize")
async def visualize_solana_analysis(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.visualize_solana_analysis(request)

# 商业模式端点
@app.get("/api/commerce/plans")
async def get_commerce_plans():
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_commerce_plans()

@app.post("/api/commerce/plan/{plan_id}")
async def get_commerce_plan_details(plan_id: str, request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_commerce_plan_details({"plan_id": plan_id, **request})

@app.post("/api/commerce/subscription")
async def create_commerce_subscription(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.create_commerce_subscription(request)

@app.post("/api/commerce/subscription/update")
async def update_commerce_subscription(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.update_commerce_subscription(request)

@app.post("/api/commerce/subscription/cancel")
async def cancel_commerce_subscription(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.cancel_commerce_subscription(request)

@app.post("/api/commerce/usage/api")
async def check_commerce_api_usage(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.check_commerce_api_usage(request)

@app.post("/api/commerce/usage/signal")
async def check_commerce_signal_usage(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.check_commerce_signal_usage(request)

@app.get("/api/commerce/payment/methods")
async def get_commerce_payment_methods():
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_commerce_payment_methods()

@app.post("/api/commerce/payment/add")
async def add_commerce_payment_method(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.add_commerce_payment_method(request)

@app.post("/api/commerce/payment/list")
async def get_user_commerce_payment_methods(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_user_commerce_payment_methods(request)

@app.post("/api/commerce/payment/set-default")
async def set_default_commerce_payment_method(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.set_default_commerce_payment_method(request)

@app.post("/api/commerce/payment/delete")
async def delete_commerce_payment_method(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.delete_commerce_payment_method(request)

@app.post("/api/commerce/payment/process")
async def process_commerce_payment(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.process_commerce_payment(request)

@app.post("/api/commerce/payment/history")
async def get_commerce_transaction_history(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_commerce_transaction_history(request)

@app.post("/api/commerce/invoice/{invoice_id}")
async def get_commerce_invoice(invoice_id: str, request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_commerce_invoice({"invoice_id": invoice_id, **request})

@app.post("/api/commerce/invoices")
async def get_user_commerce_invoices(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_user_commerce_invoices(request)

# 集成分析端点
@app.post("/api/analyze/ecosystem-with-signals")
async def analyze_ecosystem_with_signals(request: dict):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.analyze_ecosystem_with_signals(request)

# 仪表盘API端点
@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_dashboard_metrics()

@app.get("/api/signals/history/trend")
async def get_signal_trend(days: int = 7):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_signal_trend(days)

@app.get("/api/solana/activity/trend")
async def get_solana_activity_trend(days: int = 7):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_solana_activity_trend(days)

@app.get("/api/solana/projects/hot")
async def get_hot_projects(limit: int = 5):
    if not main_api_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return main_api_service.get_hot_projects(limit)

if __name__ == "__main__":
    # 启动服务器
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))

    logger.info(f"Starting TrendMatrix API server on {host}:{port}")
    logger.info(f"API documentation available at http://{host}:{port}/api/docs")

    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
