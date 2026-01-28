# API Service

import logging
from typing import Dict, List, Optional, Any

class APIService:
    """
    API 服务
    提供信号系统的外部访问接口
    """

    def __init__(self, signal_generator=None, signal_evaluator=None, signal_classifier=None, notification_service=None, history_service=None):
        """
        初始化 API 服务

        Args:
            signal_generator: 信号生成器
            signal_evaluator: 信号评估器
            signal_classifier: 信号分类器
            notification_service: 通知服务
            history_service: 历史服务
        """
        self.logger = logging.getLogger(__name__)

        # 依赖服务
        self.signal_generator = signal_generator
        self.signal_evaluator = signal_evaluator
        self.signal_classifier = signal_classifier
        self.notification_service = notification_service
        self.history_service = history_service

        # API 版本
        self.api_version = "1.0"

    def generate_signal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.signal_generator:
                return self._error_response("Signal generator not available")

            # 验证请求参数
            required_params = ['asset', 'signal_type', 'strength', 'confidence', 'trigger_conditions']
            for param in required_params:
                if param not in request:
                    return self._error_response(f"Missing required parameter: {param}")

            # 生成信号
            signal = self.signal_generator.generate_signal(
                asset=request['asset'],
                signal_type=request['signal_type'],
                strength=request['strength'],
                confidence=request['confidence'],
                trigger_conditions=request['trigger_conditions'],
                ai_analysis=request.get('ai_analysis'),
                market_data=request.get('market_data')
            )

            if not signal:
                return self._error_response("Failed to generate signal")

            # 添加到历史记录
            if self.history_service:
                self.history_service.add_signal_to_history(signal)

            # 发送通知
            if self.notification_service:
                self.notification_service.check_and_send_notifications(signal)

            return self._success_response(signal)

        except Exception as e:
            self.logger.error(f"Error generating signal: {str(e)}")
            return self._error_response(str(e))

    def generate_from_ai_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于 AI 分析生成信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.signal_generator:
                return self._error_response("Signal generator not available")

            # 验证请求参数
            if 'ai_analysis' not in request or 'market_data' not in request:
                return self._error_response("Missing required parameters: ai_analysis and market_data")

            # 生成信号
            signals = self.signal_generator.generate_from_ai_analysis(
                ai_analysis=request['ai_analysis'],
                market_data=request['market_data']
            )

            if not signals:
                return self._error_response("Failed to generate signals from AI analysis")

            # 添加到历史记录并发送通知
            for signal in signals:
                if self.history_service:
                    self.history_service.add_signal_to_history(signal)
                if self.notification_service:
                    self.notification_service.check_and_send_notifications(signal)

            return self._success_response(signals)

        except Exception as e:
            self.logger.error(f"Error generating signals from AI analysis: {str(e)}")
            return self._error_response(str(e))

    def evaluate_signal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.signal_evaluator:
                return self._error_response("Signal evaluator not available")

            # 验证请求参数
            if 'signal' not in request:
                return self._error_response("Missing required parameter: signal")

            # 评估信号
            evaluation = self.signal_evaluator.evaluate_signal(
                signal=request['signal'],
                historical_data=request.get('historical_data')
            )

            if not evaluation:
                return self._error_response("Failed to evaluate signal")

            return self._success_response(evaluation)

        except Exception as e:
            self.logger.error(f"Error evaluating signal: {str(e)}")
            return self._error_response(str(e))

    def classify_signal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分类信号

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.signal_classifier:
                return self._error_response("Signal classifier not available")

            # 验证请求参数
            if 'signal' not in request:
                return self._error_response("Missing required parameter: signal")

            # 分类信号
            classification = self.signal_classifier.classify_signal(request['signal'])

            if not classification:
                return self._error_response("Failed to classify signal")

            return self._success_response(classification)

        except Exception as e:
            self.logger.error(f"Error classifying signal: {str(e)}")
            return self._error_response(str(e))

    def set_user_thresholds(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        设置用户阈值

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.notification_service:
                return self._error_response("Notification service not available")

            # 验证请求参数
            if 'user_id' not in request or 'thresholds' not in request:
                return self._error_response("Missing required parameters: user_id and thresholds")

            # 设置阈值
            success = self.notification_service.set_user_thresholds(
                user_id=request['user_id'],
                thresholds=request['thresholds']
            )

            if not success:
                return self._error_response("Failed to set user thresholds")

            return self._success_response({"message": "User thresholds set successfully"})

        except Exception as e:
            self.logger.error(f"Error setting user thresholds: {str(e)}")
            return self._error_response(str(e))

    def get_user_thresholds(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户阈值

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.notification_service:
                return self._error_response("Notification service not available")

            # 验证请求参数
            if 'user_id' not in request:
                return self._error_response("Missing required parameter: user_id")

            # 获取阈值
            thresholds = self.notification_service.get_user_thresholds(request['user_id'])

            return self._success_response(thresholds)

        except Exception as e:
            self.logger.error(f"Error getting user thresholds: {str(e)}")
            return self._error_response(str(e))

    def get_signal_history(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取信号历史

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.history_service:
                return self._error_response("History service not available")

            # 获取历史记录
            history = self.history_service.get_signal_history(
                filters=request.get('filters'),
                limit=request.get('limit', 100)
            )

            return self._success_response(history)

        except Exception as e:
            self.logger.error(f"Error getting signal history: {str(e)}")
            return self._error_response(str(e))

    def get_signal_statistics(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取信号统计信息

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.history_service:
                return self._error_response("History service not available")

            # 获取统计信息
            statistics = self.history_service.get_signal_statistics(
                time_range=request.get('time_range')
            )

            return self._success_response(statistics)

        except Exception as e:
            self.logger.error(f"Error getting signal statistics: {str(e)}")
            return self._error_response(str(e))

    def get_accuracy_tracking(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取准确率追踪信息

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.history_service:
                return self._error_response("History service not available")

            # 获取准确率追踪
            accuracy_tracking = self.history_service.get_accuracy_tracking(
                asset=request.get('asset'),
                signal_type=request.get('signal_type')
            )

            return self._success_response(accuracy_tracking)

        except Exception as e:
            self.logger.error(f"Error getting accuracy tracking: {str(e)}")
            return self._error_response(str(e))

    def update_signal_outcome(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新信号结果

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.history_service:
                return self._error_response("History service not available")

            # 验证请求参数
            if 'signal_id' not in request or 'outcome' not in request:
                return self._error_response("Missing required parameters: signal_id and outcome")

            # 更新结果
            success = self.history_service.update_signal_outcome(
                signal_id=request['signal_id'],
                outcome=request['outcome']
            )

            if not success:
                return self._error_response("Failed to update signal outcome")

            return self._success_response({"message": "Signal outcome updated successfully"})

        except Exception as e:
            self.logger.error(f"Error updating signal outcome: {str(e)}")
            return self._error_response(str(e))

    def get_notification_history(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取通知历史

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.notification_service:
                return self._error_response("Notification service not available")

            # 获取通知历史
            history = self.notification_service.get_notification_history(
                user_id=request.get('user_id'),
                limit=request.get('limit', 50)
            )

            return self._success_response(history)

        except Exception as e:
            self.logger.error(f"Error getting notification history: {str(e)}")
            return self._error_response(str(e))

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
                    "signal_generator": self.signal_generator is not None,
                    "signal_evaluator": self.signal_evaluator is not None,
                    "signal_classifier": self.signal_classifier is not None,
                    "notification_service": self.notification_service is not None,
                    "history_service": self.history_service is not None
                },
                "endpoints": [
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
                    "/api/service/info"
                ]
            }

            return self._success_response(info)

        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
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
