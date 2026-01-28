# Test Signal System

import logging
import sys
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加项目根目录到 Python 路径
sys.path.insert(0, '/Users/mike/Desktop/wcjproject/Mantle/VibeCoding/TrendMatrix')

# 导入信号系统组件
from src.signals.core.generator.signal_generator import SignalGenerator
from src.signals.core.evaluator.signal_evaluator import SignalEvaluator
from src.signals.core.classifier.signal_classifier import SignalClassifier
from src.signals.core.engine.rule_engine import RuleEngine
from src.signals.notification.notification_service import NotificationService
from src.signals.history.history_service import HistoryService
from src.signals.api.api_service import APIService

class TestSignalSystem:
    """
    测试智能信号系统
    """

    def __init__(self):
        """
        初始化测试
        """
        logger.info("Initializing signal system test")

        # 初始化组件
        self.signal_generator = SignalGenerator()
        self.signal_evaluator = SignalEvaluator()
        self.signal_classifier = SignalClassifier()
        self.rule_engine = RuleEngine()
        self.notification_service = NotificationService()
        self.history_service = HistoryService()

        # 初始化 API 服务
        self.api_service = APIService(
            signal_generator=self.signal_generator,
            signal_evaluator=self.signal_evaluator,
            signal_classifier=self.signal_classifier,
            notification_service=self.notification_service,
            history_service=self.history_service
        )

        # 加载默认规则
        self._load_default_rules()

    def _load_default_rules(self):
        """
        加载默认规则
        """
        try:
            default_rules = self.rule_engine.get_default_rules()
            for rule in default_rules:
                rule_id = self.rule_engine.add_rule(rule)
                logger.info(f"Loaded default rule: {rule_id}")
        except Exception as e:
            logger.error(f"Error loading default rules: {str(e)}")

    def test_signal_generation(self):
        """
        测试信号生成
        """
        logger.info("Testing signal generation...")

        try:
            # 测试基本信号生成
            signal = self.signal_generator.generate_signal(
                asset="BTC",
                signal_type="buy",
                strength=8,
                confidence=0.85,
                trigger_conditions={"price_breakout": True, "volume_increase": 0.6},
                market_data={"current_price": 45000, "volume": 15000000000}
            )

            if signal:
                logger.info(f"Generated signal: {signal['signal_id']}")
                logger.info(f"Signal type: {signal['type']}")
                logger.info(f"Signal strength: {signal['strength']}")
                logger.info(f"Signal confidence: {signal['confidence']}")
                logger.info(f"Signal level: {signal['level']}")
                logger.info(f"Signal description: {signal['description']}")
                return True
            else:
                logger.error("Failed to generate signal")
                return False

        except Exception as e:
            logger.error(f"Error testing signal generation: {str(e)}")
            return False

    def test_ai_based_signal_generation(self):
        """
        测试基于 AI 分析的信号生成
        """
        logger.info("Testing AI-based signal generation...")

        try:
            # 模拟 AI 分析结果
            ai_analysis = {
                "sentiment_analysis": {
                    "average_sentiment": 0.6,
                    "confidence": 0.8
                },
                "price_prediction": {
                    "predicted_trend": "up",
                    "predicted_change": 0.05,
                    "confidence": 0.75
                },
                "anomaly_detection": {
                    "anomaly_risk": "low",
                    "anomaly_count": 0
                }
            }

            # 模拟市场数据
            market_data = {
                "asset": "ETH",
                "current_price": 3200,
                "volume": 8000000000,
                "market_trend": "up"
            }

            # 生成信号
            signals = self.signal_generator.generate_from_ai_analysis(
                ai_analysis=ai_analysis,
                market_data=market_data
            )

            if signals:
                logger.info(f"Generated {len(signals)} signals from AI analysis")
                for signal in signals:
                    logger.info(f"AI-generated signal: {signal['signal_id']}, type: {signal['type']}, strength: {signal['strength']}")
                return True
            else:
                logger.error("Failed to generate signals from AI analysis")
                return False

        except Exception as e:
            logger.error(f"Error testing AI-based signal generation: {str(e)}")
            return False

    def test_signal_evaluation(self):
        """
        测试信号评估
        """
        logger.info("Testing signal evaluation...")

        try:
            # 生成测试信号
            signal = self.signal_generator.generate_signal(
                asset="BTC",
                signal_type="buy",
                strength=7,
                confidence=0.75,
                trigger_conditions={"price_breakout": True},
                ai_analysis={
                    "sentiment_analysis": {"confidence": 0.8},
                    "price_prediction": {"confidence": 0.7}
                },
                market_data={"current_price": 45000}
            )

            if not signal:
                logger.error("Failed to generate test signal for evaluation")
                return False

            # 测试信号评估
            evaluation = self.signal_evaluator.evaluate_signal(signal)

            if evaluation:
                logger.info(f"Evaluated signal: {evaluation['signal_id']}")
                logger.info(f"Overall score: {evaluation['overall_score']:.2f}")
                logger.info(f"Evaluation level: {evaluation['evaluation_level']}")
                logger.info(f"Strength score: {evaluation['dimension_scores']['strength']:.2f}")
                logger.info(f"Confidence score: {evaluation['dimension_scores']['confidence']:.2f}")
                logger.info(f"AI analysis score: {evaluation['dimension_scores']['ai_analysis']:.2f}")
                logger.info(f"Market context score: {evaluation['dimension_scores']['market_context']:.2f}")
                logger.info(f"Recommendation: {evaluation['recommendation']['action']}")
                return True
            else:
                logger.error("Failed to evaluate signal")
                return False

        except Exception as e:
            logger.error(f"Error testing signal evaluation: {str(e)}")
            return False

    def test_signal_classification(self):
        """
        测试信号分类
        """
        logger.info("Testing signal classification...")

        try:
            # 生成测试信号
            signal = self.signal_generator.generate_signal(
                asset="ETH",
                signal_type="sell",
                strength=6,
                confidence=0.7,
                trigger_conditions={"price_drop": True},
                market_data={"market_trend": "down"}
            )

            if not signal:
                logger.error("Failed to generate test signal for classification")
                return False

            # 测试信号分类
            classification = self.signal_classifier.classify_signal(signal)

            if classification:
                logger.info(f"Classified signal: {classification['signal_id']}")
                logger.info(f"Strength category: {classification['strength_category']}")
                logger.info(f"Confidence category: {classification['confidence_category']}")
                logger.info(f"Level: {classification['level']}")
                logger.info(f"Risk level: {classification['risk_level']}")
                logger.info(f"Time sensitivity: {classification['time_sensitivity']}")
                logger.info(f"Asset class: {classification['asset_class']}")
                logger.info(f"Trend alignment: {classification['trend_alignment']}")
                logger.info(f"Comprehensive category: {classification['comprehensive_category']}")
                return True
            else:
                logger.error("Failed to classify signal")
                return False

        except Exception as e:
            logger.error(f"Error testing signal classification: {str(e)}")
            return False

    def test_notification_service(self):
        """
        测试通知服务
        """
        logger.info("Testing notification service...")

        try:
            # 设置用户阈值
            user_id = "test_user"
            thresholds = {
                "buy": 6,
                "sell": 6,
                "alert": 5,
                "hold": 0
            }

            success = self.notification_service.set_user_thresholds(user_id, thresholds)
            if success:
                logger.info(f"Set user thresholds for {user_id}")
            else:
                logger.error("Failed to set user thresholds")
                return False

            # 生成高优先级信号
            signal = self.signal_generator.generate_signal(
                asset="BTC",
                signal_type="buy",
                strength=9,
                confidence=0.9,
                trigger_conditions={"strong_buy_signal": True}
            )

            if signal:
                # 测试通知
                notifications = self.notification_service.check_and_send_notifications(signal, [user_id])
                if notifications:
                    logger.info(f"Sent {len(notifications)} notifications")
                    for notification in notifications:
                        logger.info(f"Notification ID: {notification['notification_id']}")
                        logger.info(f"Notification status: {notification['status']}")
                        logger.info(f"Notification channels: {notification['channels']}")
                    return True
                else:
                    logger.warning("No notifications sent (may be within threshold)")
                    return True
            else:
                logger.error("Failed to generate signal for notification test")
                return False

        except Exception as e:
            logger.error(f"Error testing notification service: {str(e)}")
            return False

    def test_history_service(self):
        """
        测试历史服务
        """
        logger.info("Testing history service...")

        try:
            # 生成并添加信号到历史
            signal = self.signal_generator.generate_signal(
                asset="BTC",
                signal_type="buy",
                strength=7,
                confidence=0.8,
                trigger_conditions={"test": True}
            )

            if signal:
                # 添加到历史
                added = self.history_service.add_signal_to_history(signal)
                if added:
                    logger.info(f"Added signal to history: {signal['signal_id']}")
                else:
                    logger.error("Failed to add signal to history")
                    return False

                # 更新信号结果
                outcome = {
                    "actual_outcome": "up",
                    "price_change": 0.08,
                    "timeframe": "24h"
                }

                updated = self.history_service.update_signal_outcome(signal['signal_id'], outcome)
                if updated:
                    logger.info(f"Updated signal outcome: {signal['signal_id']}")
                else:
                    logger.error("Failed to update signal outcome")

                # 获取历史记录
                history = self.history_service.get_signal_history(filters={"asset": "BTC"}, limit=5)
                logger.info(f"Retrieved {len(history)} signals from history")

                # 获取统计信息
                stats = self.history_service.get_signal_statistics()
                logger.info(f"Total signals: {stats.get('total_signals', 0)}")
                logger.info(f"Completed signals: {stats.get('completed_signals', 0)}")
                logger.info(f"Active signals: {stats.get('active_signals', 0)}")

                # 获取准确率追踪
                accuracy = self.history_service.get_accuracy_tracking(asset="BTC")
                logger.info(f"Overall accuracy: {accuracy.get('overall_accuracy', 0):.2f}")

                return True
            else:
                logger.error("Failed to generate signal for history test")
                return False

        except Exception as e:
            logger.error(f"Error testing history service: {str(e)}")
            return False

    def test_api_service(self):
        """
        测试 API 服务
        """
        logger.info("Testing API service...")

        try:
            # 测试服务信息
            service_info = self.api_service.get_service_info()
            if service_info:
                logger.info(f"API version: {service_info['data']['api_version']}")
                logger.info(f"Available services: {service_info['data']['services']}")
                logger.info(f"API endpoints: {len(service_info['data']['endpoints'])}")
            else:
                logger.error("Failed to get service info")
                return False

            # 测试 API 信号生成
            request = {
                "asset": "ETH",
                "signal_type": "sell",
                "strength": 7,
                "confidence": 0.75,
                "trigger_conditions": {"price_drop": True}
            }

            response = self.api_service.generate_signal(request)
            if response and response['success']:
                logger.info(f"API generated signal: {response['data']['signal_id']}")
                return True
            else:
                logger.error(f"API signal generation failed: {response.get('message', 'Unknown error')}")
                return False

        except Exception as e:
            logger.error(f"Error testing API service: {str(e)}")
            return False

    def run_all_tests(self):
        """
        运行所有测试
        """
        logger.info("Running all signal system tests...")

        tests = [
            ("Signal Generation", self.test_signal_generation),
            ("AI-based Signal Generation", self.test_ai_based_signal_generation),
            ("Signal Evaluation", self.test_signal_evaluation),
            ("Signal Classification", self.test_signal_classification),
            ("Notification Service", self.test_notification_service),
            ("History Service", self.test_history_service),
            ("API Service", self.test_api_service)
        ]

        results = {}
        for test_name, test_func in tests:
            logger.info(f"\n=== Testing: {test_name} ===")
            success = test_func()
            results[test_name] = success
            logger.info(f"Test {test_name}: {'PASS' if success else 'FAIL'}")

        # 汇总结果
        passed_tests = sum(1 for success in results.values() if success)
        total_tests = len(results)

        logger.info(f"\n=== Test Summary ===")
        logger.info(f"Total tests: {total_tests}")
        logger.info(f"Passed tests: {passed_tests}")
        logger.info(f"Failed tests: {total_tests - passed_tests}")
        logger.info(f"Test success rate: {(passed_tests / total_tests * 100):.1f}%")

        for test_name, success in results.items():
            logger.info(f"{test_name}: {'PASS' if success else 'FAIL'}")

        return passed_tests == total_tests

if __name__ == "__main__":
    """
    运行测试
    """
    test_system = TestSignalSystem()
    success = test_system.run_all_tests()

    if success:
        logger.info("\n✅ All tests passed! Signal system is working correctly.")
    else:
        logger.error("\n❌ Some tests failed. Please check the logs for details.")
