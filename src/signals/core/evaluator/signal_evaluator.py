# Signal Evaluator

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

class SignalEvaluator:
    """
    信号评估器
    评估信号的可靠性和质量
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化信号评估器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 评估参数
        self.weight_strength = self.config.get('weight_strength', 0.4)
        self.weight_confidence = self.config.get('weight_confidence', 0.3)
        self.weight_ai_analysis = self.config.get('weight_ai_analysis', 0.2)
        self.weight_market_context = self.config.get('weight_market_context', 0.1)

    def evaluate_signal(self, signal: Dict[str, Any], historical_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        评估信号

        Args:
            signal: 信号对象
            historical_data: 历史数据

        Returns:
            评估结果
        """
        try:
            # 验证信号
            if not self._validate_signal(signal):
                self.logger.error("Invalid signal for evaluation")
                return None

            # 计算各维度评估分数
            strength_score = self._evaluate_strength(signal)
            confidence_score = self._evaluate_confidence(signal)
            ai_analysis_score = self._evaluate_ai_analysis(signal)
            market_context_score = self._evaluate_market_context(signal, historical_data)

            # 计算综合评估分数
            overall_score = (
                strength_score * self.weight_strength +
                confidence_score * self.weight_confidence +
                ai_analysis_score * self.weight_ai_analysis +
                market_context_score * self.weight_market_context
            )

            # 确定评估等级
            evaluation_level = self._get_evaluation_level(overall_score)

            # 生成评估结果
            evaluation = {
                'signal_id': signal['signal_id'],
                'overall_score': overall_score,
                'evaluation_level': evaluation_level,
                'dimension_scores': {
                    'strength': strength_score,
                    'confidence': confidence_score,
                    'ai_analysis': ai_analysis_score,
                    'market_context': market_context_score
                },
                'weights': {
                    'strength': self.weight_strength,
                    'confidence': self.weight_confidence,
                    'ai_analysis': self.weight_ai_analysis,
                    'market_context': self.weight_market_context
                },
                'timestamp': datetime.now().isoformat(),
                'recommendation': self._generate_recommendation(signal, evaluation_level, overall_score)
            }

            self.logger.info(f"Evaluated signal {signal['signal_id']}: {evaluation_level} (score: {overall_score:.2f})")

            return evaluation

        except Exception as e:
            self.logger.error(f"Error evaluating signal: {str(e)}")
            return None

    def evaluate_multiple_signals(self, signals: List[Dict[str, Any]], historical_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        评估多个信号

        Args:
            signals: 信号列表
            historical_data: 历史数据

        Returns:
            评估结果列表
        """
        evaluations = []
        for signal in signals:
            evaluation = self.evaluate_signal(signal, historical_data)
            if evaluation:
                evaluations.append(evaluation)
        return evaluations

    def _validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        验证信号

        Args:
            signal: 信号对象

        Returns:
            是否有效
        """
        try:
            # 检查必要字段
            required_fields = ['signal_id', 'asset', 'type', 'strength', 'confidence', 'timestamp']
            for field in required_fields:
                if field not in signal:
                    self.logger.error(f"Missing required field {field} in signal")
                    return False

            # 检查信号强度
            if not 1 <= signal['strength'] <= 10:
                self.logger.error(f"Invalid signal strength: {signal['strength']}")
                return False

            # 检查信号置信度
            if not 0 <= signal['confidence'] <= 1:
                self.logger.error(f"Invalid signal confidence: {signal['confidence']}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating signal: {str(e)}")
            return False

    def _evaluate_strength(self, signal: Dict[str, Any]) -> float:
        """
        评估信号强度

        Args:
            signal: 信号对象

        Returns:
            强度评估分数 (0-1)
        """
        try:
            strength = signal['strength']
            # 将强度 (1-10) 映射到 (0-1)
            return strength / 10.0

        except Exception as e:
            self.logger.error(f"Error evaluating strength: {str(e)}")
            return 0.5

    def _evaluate_confidence(self, signal: Dict[str, Any]) -> float:
        """
        评估信号置信度

        Args:
            signal: 信号对象

        Returns:
            置信度评估分数 (0-1)
        """
        try:
            confidence = signal['confidence']
            # 置信度已经是 (0-1) 范围
            return confidence

        except Exception as e:
            self.logger.error(f"Error evaluating confidence: {str(e)}")
            return 0.5

    def _evaluate_ai_analysis(self, signal: Dict[str, Any]) -> float:
        """
        评估 AI 分析质量

        Args:
            signal: 信号对象

        Returns:
            AI 分析评估分数 (0-1)
        """
        try:
            ai_analysis = signal.get('ai_analysis', {})
            if not ai_analysis:
                return 0.5

            # 计算 AI 分析覆盖的维度
            analysis_dimensions = 0
            score_sum = 0

            # 评估情感分析
            if 'sentiment_analysis' in ai_analysis:
                sentiment_analysis = ai_analysis['sentiment_analysis']
                if 'confidence' in sentiment_analysis:
                    score_sum += sentiment_analysis['confidence']
                    analysis_dimensions += 1

            # 评估价格预测
            if 'price_prediction' in ai_analysis:
                price_prediction = ai_analysis['price_prediction']
                if 'confidence' in price_prediction:
                    score_sum += price_prediction['confidence']
                    analysis_dimensions += 1

            # 评估异常检测
            if 'anomaly_detection' in ai_analysis:
                anomaly_detection = ai_analysis['anomaly_detection']
                if 'anomaly_risk' in anomaly_detection:
                    # 将异常风险映射到分数
                    risk_score = {
                        'low': 0.3,
                        'medium': 0.6,
                        'high': 0.9
                    }.get(anomaly_detection['anomaly_risk'], 0.5)
                    score_sum += risk_score
                    analysis_dimensions += 1

            # 计算平均分数
            if analysis_dimensions > 0:
                return score_sum / analysis_dimensions
            else:
                return 0.5

        except Exception as e:
            self.logger.error(f"Error evaluating AI analysis: {str(e)}")
            return 0.5

    def _evaluate_market_context(self, signal: Dict[str, Any], historical_data: Optional[Dict[str, Any]]) -> float:
        """
        评估市场背景

        Args:
            signal: 信号对象
            historical_data: 历史数据

        Returns:
            市场背景评估分数 (0-1)
        """
        try:
            if not historical_data:
                return 0.5

            asset = signal['asset']
            signal_type = signal['type']

            # 检查资产历史数据
            if asset not in historical_data:
                return 0.5

            asset_data = historical_data[asset]

            # 评估市场趋势与信号的一致性
            market_trend = asset_data.get('market_trend', 'neutral')
            trend_consistency = 0.5

            if signal_type == 'buy' and market_trend == 'up':
                trend_consistency = 0.9
            elif signal_type == 'sell' and market_trend == 'down':
                trend_consistency = 0.9
            elif signal_type == 'buy' and market_trend == 'down':
                trend_consistency = 0.3
            elif signal_type == 'sell' and market_trend == 'up':
                trend_consistency = 0.3

            # 评估市场 volatility
            volatility = asset_data.get('volatility', 0.02)
            volatility_score = max(0.1, min(0.9, 1 - volatility * 10))

            # 评估市场流动性
            liquidity = asset_data.get('liquidity', 0.5)
            liquidity_score = liquidity

            # 计算市场背景综合分数
            market_context_score = (trend_consistency + volatility_score + liquidity_score) / 3

            return market_context_score

        except Exception as e:
            self.logger.error(f"Error evaluating market context: {str(e)}")
            return 0.5

    def _get_evaluation_level(self, score: float) -> str:
        """
        获取评估等级

        Args:
            score: 评估分数

        Returns:
            评估等级
        """
        if score >= 0.9:
            return 'excellent'
        elif score >= 0.75:
            return 'very_good'
        elif score >= 0.6:
            return 'good'
        elif score >= 0.45:
            return 'fair'
        elif score >= 0.3:
            return 'poor'
        else:
            return 'very_poor'

    def _generate_recommendation(self, signal: Dict[str, Any], evaluation_level: str, overall_score: float) -> Dict[str, Any]:
        """
        生成推荐

        Args:
            signal: 信号对象
            evaluation_level: 评估等级
            overall_score: 综合分数

        Returns:
            推荐
        """
        signal_type = signal['type']

        # 基于评估等级生成推荐
        if evaluation_level in ['excellent', 'very_good']:
            action = 'strongly_recommended'
            confidence = min(1.0, overall_score * 1.1)
        elif evaluation_level == 'good':
            action = 'recommended'
            confidence = overall_score
        elif evaluation_level == 'fair':
            action = 'cautiously_recommended'
            confidence = max(0.5, overall_score * 0.9)
        else:
            action = 'not_recommended'
            confidence = min(0.5, overall_score)

        # 生成推荐理由
        reasons = []
        if evaluation_level in ['excellent', 'very_good']:
            reasons.append(f"Strong {signal_type} signal with high confidence")
            reasons.append("Multiple indicators confirm the signal")
        elif evaluation_level == 'good':
            reasons.append(f"Decent {signal_type} signal with reasonable confidence")
            reasons.append("Most indicators support the signal")
        elif evaluation_level == 'fair':
            reasons.append(f"Mixed signals for {signal_type} action")
            reasons.append("Some indicators support the signal, but not all")
        else:
            reasons.append(f"Weak {signal_type} signal with low confidence")
            reasons.append("Few indicators support the signal")

        return {
            'action': action,
            'confidence': confidence,
            'reasons': reasons,
            'signal_type': signal_type,
            'evaluation_level': evaluation_level
        }

    def compare_signals(self, signals: List[Dict[str, Any]], historical_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        比较多个信号

        Args:
            signals: 信号列表
            historical_data: 历史数据

        Returns:
            排序后的信号列表
        """
        try:
            # 评估每个信号
            evaluated_signals = []
            for signal in signals:
                evaluation = self.evaluate_signal(signal, historical_data)
                if evaluation:
                    signal_with_evaluation = signal.copy()
                    signal_with_evaluation['evaluation'] = evaluation
                    evaluated_signals.append(signal_with_evaluation)

            # 按综合评估分数排序
            sorted_signals = sorted(
                evaluated_signals,
                key=lambda x: x['evaluation']['overall_score'],
                reverse=True
            )

            return sorted_signals

        except Exception as e:
            self.logger.error(f"Error comparing signals: {str(e)}")
            return []

    def get_signal_statistics(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取信号统计信息

        Args:
            signals: 信号列表

        Returns:
            统计信息
        """
        try:
            if not signals:
                return {
                    'total_signals': 0,
                    'average_strength': 0,
                    'average_confidence': 0,
                    'signal_type_distribution': {},
                    'strength_distribution': {},
                    'confidence_distribution': {}
                }

            # 计算基本统计
            total_signals = len(signals)
            average_strength = sum(s['strength'] for s in signals) / total_signals
            average_confidence = sum(s['confidence'] for s in signals) / total_signals

            # 计算信号类型分布
            signal_type_distribution = {}
            for signal in signals:
                signal_type = signal['type']
                if signal_type not in signal_type_distribution:
                    signal_type_distribution[signal_type] = 0
                signal_type_distribution[signal_type] += 1

            # 计算强度分布
            strength_distribution = {
                'high': 0,  # 8-10
                'medium': 0,  # 4-7
                'low': 0  # 1-3
            }
            for signal in signals:
                strength = signal['strength']
                if strength >= 8:
                    strength_distribution['high'] += 1
                elif strength >= 4:
                    strength_distribution['medium'] += 1
                else:
                    strength_distribution['low'] += 1

            # 计算置信度分布
            confidence_distribution = {
                'high': 0,  # 0.8-1.0
                'medium': 0,  # 0.5-0.79
                'low': 0  # 0.0-0.49
            }
            for signal in signals:
                confidence = signal['confidence']
                if confidence >= 0.8:
                    confidence_distribution['high'] += 1
                elif confidence >= 0.5:
                    confidence_distribution['medium'] += 1
                else:
                    confidence_distribution['low'] += 1

            return {
                'total_signals': total_signals,
                'average_strength': average_strength,
                'average_confidence': average_confidence,
                'signal_type_distribution': signal_type_distribution,
                'strength_distribution': strength_distribution,
                'confidence_distribution': confidence_distribution
            }

        except Exception as e:
            self.logger.error(f"Error getting signal statistics: {str(e)}")
            return {}
