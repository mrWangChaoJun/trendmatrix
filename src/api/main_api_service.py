# Main API Service
# 主API服务，集成所有模块的API功能

import logging
from typing import Dict, List, Optional, Any
from signals.api.api_service import APIService as SignalsAPIService
from solana.api.solana_api_service import SolanaAPIService
from api.auth_service import AuthService
from commerce.api.commerce_api_service import CommerceAPIService

class MainAPIService:
    """
    主API服务
    集成所有模块的API功能
    """

    def __init__(self, signals_api_service=None, solana_api_service=None, auth_service=None, commerce_api_service=None):
        """
        初始化主API服务

        Args:
            signals_api_service: 信号系统API服务
            solana_api_service: Solana生态分析API服务
            auth_service: 认证服务
            commerce_api_service: 商业模式API服务
        """
        self.logger = logging.getLogger(__name__)

        # 依赖服务
        self.signals_api_service = signals_api_service
        self.solana_api_service = solana_api_service
        self.auth_service = auth_service
        self.commerce_api_service = commerce_api_service

        # API版本
        self.api_version = "1.0"

    def get_service_info(self) -> Dict[str, Any]:
        """
        获取服务信息

        Returns:
            服务信息
        """
        try:
            info = {
                "api_version": self.api_version,
                "services": {
                    "signals": self.signals_api_service is not None,
                    "solana": self.solana_api_service is not None,
                    "auth": self.auth_service is not None,
                    "commerce": self.commerce_api_service is not None
                },
                "endpoints": [
                    # 认证端点
                    "/api/auth/register",
                    "/api/auth/login",
                    "/api/auth/verify",
                    "/api/auth/user-info",
                    "/api/auth/update",
                    "/api/auth/logout",
                    # 信号系统端点
                    "/api/signals/generate",
                    "/api/signals/generate-from-ai",
                    "/api/signals/evaluate",
                    "/api/signals/classify",
                    "/api/thresholds/set",
                    "/api/thresholds/get",
                    "/api/history/signals",
                    "/api/history/statistics",
                    "/api/history/accuracy",
                    "/api/history/update-outcome",
                    "/api/notifications/history",
                    # Solana生态分析端点
                    "/api/solana/analyze-project",
                    "/api/solana/analyze-developer",
                    "/api/solana/analyze-nft",
                    "/api/solana/analyze-defi",
                    "/api/solana/analyze-multiple-projects",
                    "/api/solana/visualize",
                    # 商业模式端点
                    "/api/commerce/plans",
                    "/api/commerce/plan/{plan_id}",
                    "/api/commerce/subscription",
                    "/api/commerce/subscription/update",
                    "/api/commerce/subscription/cancel",
                    "/api/commerce/usage/api",
                    "/api/commerce/usage/signal",
                    "/api/commerce/payment/methods",
                    "/api/commerce/payment/add",
                    "/api/commerce/payment/list",
                    "/api/commerce/payment/set-default",
                    "/api/commerce/payment/delete",
                    "/api/commerce/payment/process",
                    "/api/commerce/payment/history",
                    "/api/commerce/invoice/{invoice_id}",
                    "/api/commerce/invoices",
                    # 主服务端点
                    "/api/service/info"
                ]
            }

            return self._success_response(info)

        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return self._error_response(str(e))

    # 信号系统API方法
    def generate_signal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.generate_signal(request)

    def generate_signal_from_ai(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于AI分析生成信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.generate_from_ai_analysis(request)

    def evaluate_signal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.evaluate_signal(request)

    def classify_signal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分类信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.classify_signal(request)

    def set_user_thresholds(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        设置用户阈值

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.set_user_thresholds(request)

    def get_user_thresholds(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户阈值

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.get_user_thresholds(request)

    def get_signal_history(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取信号历史

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.get_signal_history(request)

    def get_signal_statistics(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取信号统计信息

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.get_signal_statistics(request)

    def get_accuracy_tracking(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取准确率追踪信息

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.get_accuracy_tracking(request)

    def update_signal_outcome(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新信号结果

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.update_signal_outcome(request)

    def get_notification_history(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取通知历史

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.signals_api_service:
            return self._error_response("Signals API service not available")
        return self.signals_api_service.get_notification_history(request)

    # Solana生态分析API方法
    def analyze_solana_project(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析Solana项目

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.analyze_project_activity(request)

    def analyze_solana_developer(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析Solana开发者活动

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.analyze_developer_activity(request)

    def analyze_solana_nft(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析Solana NFT集合

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.analyze_nft_collection(request)

    def analyze_solana_defi(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析Solana DeFi协议

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.analyze_defi_protocol(request)

    def analyze_multiple_solana_projects(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析多个Solana项目

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.analyze_multiple_projects(request)

    def visualize_solana_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        可视化Solana分析结果

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.visualize_analysis(request)

    def get_solana_service_info(self) -> Dict[str, Any]:
        """
        获取Solana服务信息

        Returns:
            Solana服务信息
        """
        if not self.solana_api_service:
            return self._error_response("Solana API service not available")
        return self.solana_api_service.get_service_info()

    # 仪表盘API方法
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """
        获取仪表盘指标数据

        Returns:
            仪表盘指标数据
        """
        try:
            # 生成模拟数据
            metrics = {
                "total_signals": 1248,
                "active_projects": 86,
                "market_sentiment": "中性",
                "sentiment_score": 52,
                "solana_activity": 78.5
            }
            return self._success_response(metrics)
        except Exception as e:
            self.logger.error(f"Error getting dashboard metrics: {str(e)}")
            return self._error_response(str(e))

    def get_signal_trend(self, days: int = 7) -> Dict[str, Any]:
        """
        获取信号趋势数据

        Args:
            days: 天数

        Returns:
            信号趋势数据
        """
        try:
            # 生成模拟数据
            trend = []
            for i in range(days):
                date = f"1月{20 + i}日"
                trend.append({
                    "date": date,
                    "signals": 45 + i * 10,
                    "activity": 65 + i * 3
                })
            return self._success_response({"trend": trend})
        except Exception as e:
            self.logger.error(f"Error getting signal trend: {str(e)}")
            return self._error_response(str(e))

    def get_solana_activity_trend(self, days: int = 7) -> Dict[str, Any]:
        """
        获取Solana活动趋势数据

        Args:
            days: 天数

        Returns:
            Solana活动趋势数据
        """
        try:
            # 生成模拟数据
            trend = []
            for i in range(days):
                date = f"1月{20 + i}日"
                trend.append({
                    "date": date,
                    "activity": 65 + i * 3
                })
            return self._success_response({"trend": trend})
        except Exception as e:
            self.logger.error(f"Error getting Solana activity trend: {str(e)}")
            return self._error_response(str(e))

    def get_hot_projects(self, limit: int = 5) -> Dict[str, Any]:
        """
        获取热门项目

        Args:
            limit: 限制数量

        Returns:
            热门项目列表
        """
        try:
            # 生成模拟数据
            projects = [
                {"id": "1", "name": "Solana", "category": "Layer 1", "score": 92, "change": 5.2},
                {"id": "2", "name": "Serum", "category": "DeFi", "score": 85, "change": 3.7},
                {"id": "3", "name": "Metaplex", "category": "NFT", "score": 78, "change": 2.1},
                {"id": "4", "name": "Raydium", "category": "DeFi", "score": 75, "change": -1.2},
                {"id": "5", "name": "Star Atlas", "category": "GameFi", "score": 72, "change": 4.5}
            ]
            return self._success_response({"projects": projects[:limit]})
        except Exception as e:
            self.logger.error(f"Error getting hot projects: {str(e)}")
            return self._error_response(str(e))

    # 集成分析方法
    def analyze_ecosystem_with_signals(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        集成生态分析和信号生成

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.solana_api_service or not self.signals_api_service:
                return self._error_response("Required services not available")

            # 验证请求参数
            if 'solana_data' not in request:
                return self._error_response("Missing required parameter: solana_data")

            # 分析Solana生态数据
            solana_analysis = self.solana_api_service.analyze_project_activity({
                'project_data': request['solana_data'],
                'historical_data': request.get('historical_data', {})
            })

            if not solana_analysis.get('success'):
                return self._error_response(f"Solana analysis failed: {solana_analysis.get('message')}")

            # 基于分析结果生成信号
            analysis_data = solana_analysis.get('data', {})
            signal_request = {
                'asset': analysis_data.get('project_name', 'SOL'),
                'signal_type': 'trend',
                'strength': min(100, max(0, int(analysis_data.get('total_score', 50)))),
                'confidence': min(100, max(0, int(analysis_data.get('confidence', 50)))),
                'trigger_conditions': {
                    'analysis_type': 'solana_ecosystem',
                    'metrics': analysis_data.get('metrics', {})
                },
                'ai_analysis': request.get('ai_analysis', {}),
                'market_data': request.get('market_data', {})
            }

            # 生成信号
            signal_response = self.signals_api_service.generate_signal(signal_request)

            return self._success_response({
                'solana_analysis': analysis_data,
                'signal': signal_response.get('data'),
                'signal_status': signal_response.get('success')
            })

        except Exception as e:
            self.logger.error(f"Error in ecosystem analysis with signals: {str(e)}")
            return self._error_response(str(e))

    # 认证相关方法
    def register(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户注册

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.auth_service:
                return self._error_response("Auth service not available")

            return self.auth_service.register(request)

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
            if not self.auth_service:
                return self._error_response("Auth service not available")

            return self.auth_service.login(request)

        except Exception as e:
            self.logger.error(f"Error logging in user: {str(e)}")
            return self._error_response(str(e))

    def verify_token(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证令牌

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.auth_service:
                return self._error_response("Auth service not available")

            # 验证请求参数
            if 'token' not in request:
                return self._error_response("Missing required parameter: token")

            return self.auth_service.verify_token(request['token'])

        except Exception as e:
            self.logger.error(f"Error verifying token: {str(e)}")
            return self._error_response(str(e))

    def get_user_info(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户信息

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.auth_service:
                return self._error_response("Auth service not available")

            # 验证请求参数
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")

            return self.auth_service.get_user_info(request['user_id'])

        except Exception as e:
            self.logger.error(f"Error getting user info: {str(e)}")
            return self._error_response(str(e))

    def update_user(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新用户信息

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.auth_service:
                return self._error_response("Auth service not available")

            # 验证请求参数
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")

            # 移除user_id参数，剩余的作为更新数据
            user_id = request.pop('user_id')
            return self.auth_service.update_user(user_id, request)

        except Exception as e:
            self.logger.error(f"Error updating user: {str(e)}")
            return self._error_response(str(e))

    def logout(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户登出

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.auth_service:
                return self._error_response("Auth service not available")

            # 验证请求参数
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")

            return self.auth_service.logout(request['user_id'])

        except Exception as e:
            self.logger.error(f"Error logging out user: {str(e)}")
            return self._error_response(str(e))

    # 商业模式API方法
    def get_commerce_plans(self) -> Dict[str, Any]:
        """
        获取所有订阅计划

        Returns:
            订阅计划列表
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            return self.commerce_api_service.get_plans()
        except Exception as e:
            self.logger.error(f"Error getting commerce plans: {str(e)}")
            return self._error_response(str(e))

    def get_commerce_plan_details(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取特定计划详情

        Args:
            request: 请求参数

        Returns:
            计划详情
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'plan_id' not in request:
                return self._error_response("Missing required parameter: plan_id")
            return self.commerce_api_service.get_plan_details(request['plan_id'])
        except Exception as e:
            self.logger.error(f"Error getting plan details: {str(e)}")
            return self._error_response(str(e))

    def create_commerce_subscription(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建用户订阅

        Args:
            request: 请求参数

        Returns:
            订阅创建结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request or 'plan_id' not in request:
                return self._error_response("Missing required parameters: user_id and plan_id")
            return self.commerce_api_service.create_subscription(request['user_id'], request['plan_id'])
        except Exception as e:
            self.logger.error(f"Error creating subscription: {str(e)}")
            return self._error_response(str(e))

    def get_user_commerce_subscription(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户订阅信息

        Args:
            request: 请求参数

        Returns:
            用户订阅信息
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            return self.commerce_api_service.get_user_subscription(request['user_id'])
        except Exception as e:
            self.logger.error(f"Error getting user subscription: {str(e)}")
            return self._error_response(str(e))

    def update_commerce_subscription(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新用户订阅计划

        Args:
            request: 请求参数

        Returns:
            更新结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request or 'plan_id' not in request:
                return self._error_response("Missing required parameters: user_id and plan_id")
            return self.commerce_api_service.update_subscription(request['user_id'], request['plan_id'])
        except Exception as e:
            self.logger.error(f"Error updating subscription: {str(e)}")
            return self._error_response(str(e))

    def cancel_commerce_subscription(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        取消用户订阅

        Args:
            request: 请求参数

        Returns:
            取消结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            return self.commerce_api_service.cancel_subscription(request['user_id'])
        except Exception as e:
            self.logger.error(f"Error cancelling subscription: {str(e)}")
            return self._error_response(str(e))

    def check_commerce_api_usage(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查API使用情况

        Args:
            request: 请求参数

        Returns:
            API使用情况
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            return self.commerce_api_service.check_api_usage(request['user_id'])
        except Exception as e:
            self.logger.error(f"Error checking API usage: {str(e)}")
            return self._error_response(str(e))

    def check_commerce_signal_usage(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查信号使用情况

        Args:
            request: 请求参数

        Returns:
            信号使用情况
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            return self.commerce_api_service.check_signal_usage(request['user_id'])
        except Exception as e:
            self.logger.error(f"Error checking signal usage: {str(e)}")
            return self._error_response(str(e))

    def get_commerce_payment_methods(self) -> Dict[str, Any]:
        """
        获取支持的支付方式

        Returns:
            支持的支付方式列表
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            return self.commerce_api_service.get_supported_payment_methods()
        except Exception as e:
            self.logger.error(f"Error getting payment methods: {str(e)}")
            return self._error_response(str(e))

    def add_commerce_payment_method(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加用户支付方式

        Args:
            request: 请求参数

        Returns:
            添加结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request or 'payment_data' not in request:
                return self._error_response("Missing required parameters: user_id and payment_data")
            return self.commerce_api_service.add_payment_method(request['user_id'], request['payment_data'])
        except Exception as e:
            self.logger.error(f"Error adding payment method: {str(e)}")
            return self._error_response(str(e))

    def get_user_commerce_payment_methods(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户支付方式

        Args:
            request: 请求参数

        Returns:
            用户支付方式列表
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            return self.commerce_api_service.get_user_payment_methods(request['user_id'])
        except Exception as e:
            self.logger.error(f"Error getting user payment methods: {str(e)}")
            return self._error_response(str(e))

    def set_default_commerce_payment_method(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        设置默认支付方式

        Args:
            request: 请求参数

        Returns:
            设置结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request or 'payment_method_id' not in request:
                return self._error_response("Missing required parameters: user_id and payment_method_id")
            return self.commerce_api_service.set_default_payment_method(request['user_id'], request['payment_method_id'])
        except Exception as e:
            self.logger.error(f"Error setting default payment method: {str(e)}")
            return self._error_response(str(e))

    def delete_commerce_payment_method(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        删除用户支付方式

        Args:
            request: 请求参数

        Returns:
            删除结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request or 'payment_method_id' not in request:
                return self._error_response("Missing required parameters: user_id and payment_method_id")
            return self.commerce_api_service.delete_payment_method(request['user_id'], request['payment_method_id'])
        except Exception as e:
            self.logger.error(f"Error deleting payment method: {str(e)}")
            return self._error_response(str(e))

    def process_commerce_payment(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理支付

        Args:
            request: 请求参数

        Returns:
            支付处理结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request or 'payment_request' not in request:
                return self._error_response("Missing required parameters: user_id and payment_request")
            return self.commerce_api_service.process_payment(request['user_id'], request['payment_request'])
        except Exception as e:
            self.logger.error(f"Error processing payment: {str(e)}")
            return self._error_response(str(e))

    def get_commerce_transaction_history(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取交易历史

        Args:
            request: 请求参数

        Returns:
            交易历史
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            limit = request.get('limit', 10)
            offset = request.get('offset', 0)
            return self.commerce_api_service.get_transaction_history(request['user_id'], limit, offset)
        except Exception as e:
            self.logger.error(f"Error getting transaction history: {str(e)}")
            return self._error_response(str(e))

    def get_commerce_invoice(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取账单详情

        Args:
            request: 请求参数

        Returns:
            账单详情
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'invoice_id' not in request:
                return self._error_response("Missing required parameter: invoice_id")
            return self.commerce_api_service.get_invoice(request['invoice_id'])
        except Exception as e:
            self.logger.error(f"Error getting invoice: {str(e)}")
            return self._error_response(str(e))

    def get_user_commerce_invoices(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户账单列表

        Args:
            request: 请求参数

        Returns:
            账单列表
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            limit = request.get('limit', 10)
            offset = request.get('offset', 0)
            return self.commerce_api_service.get_user_invoices(request['user_id'], limit, offset)
        except Exception as e:
            self.logger.error(f"Error getting user invoices: {str(e)}")
            return self._error_response(str(e))

    def create_commerce_subscription_with_payment(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建订阅并处理支付

        Args:
            request: 请求参数

        Returns:
            创建和支付结果
        """
        try:
            if not self.commerce_api_service:
                return self._error_response("Commerce API service not available")
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")
            return self.commerce_api_service.create_subscription_with_payment(request['user_id'], request)
        except Exception as e:
            self.logger.error(f"Error creating subscription with payment: {str(e)}")
            return self._error_response(str(e))

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
