# Signal Generator

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

class SignalGenerator:
    """
    信号生成器
    基于 AI 模型分析结果和市场数据生成信号
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化信号生成器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 信号生成参数
        self.min_confidence = self.config.get('min_confidence', 0.5)
        self.signal_expiry_hours = self.config.get('signal_expiry_hours', 24)

    def generate_signal(self,
                      asset: str,
                      signal_type: str,
                      strength: int,
                      confidence: float,
                      trigger_conditions: Dict[str, Any],
                      ai_analysis: Optional[Dict[str, Any]] = None,
                      market_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        生成信号

        Args:
            asset: 资产名称 (e.g., 'BTC', 'ETH')
            signal_type: 信号类型 (e.g., 'buy', 'sell', 'hold', 'alert')
            strength: 信号强度 (1-10)
            confidence: 信号置信度 (0-1)
            trigger_conditions: 触发条件
            ai_analysis: AI 模型分析结果
            market_data: 市场数据

        Returns:
            信号对象
        """
        try:
            # 验证参数
            if not 1 <= strength <= 10:
                raise ValueError("Signal strength must be between 1 and 10")

            if not 0 <= confidence <= 1:
                raise ValueError("Signal confidence must be between 0 and 1")

            # 检查最小置信度
            if confidence < self.min_confidence:
                self.logger.warning(f"Signal confidence {confidence} below threshold {self.min_confidence}, skipping signal generation")
                return None

            # 生成信号 ID
            signal_id = f"signal_{uuid.uuid4().hex[:8]}"

            # 计算信号有效期
            timestamp = datetime.now()
            expiry_time = timestamp

            # 构建信号对象
            signal = {
                'signal_id': signal_id,
                'asset': asset,
                'type': signal_type,
                'strength': strength,
                'confidence': confidence,
                'trigger_conditions': trigger_conditions,
                'ai_analysis': ai_analysis or {},
                'market_data': market_data or {},
                'timestamp': timestamp.isoformat(),
                'expiry_time': expiry_time.isoformat(),
                'status': 'active',
                'metadata': {
                    'source': 'ai_generated',
                    'version': '1.0'
                }
            }

            # 计算信号级别
            signal['level'] = self._calculate_signal_level(strength, confidence)

            # 生成信号描述
            signal['description'] = self._generate_signal_description(signal)

            self.logger.info(f"Generated {signal_type} signal for {asset} with strength {strength} and confidence {confidence}")

            return signal

        except Exception as e:
            self.logger.error(f"Error generating signal: {str(e)}")
            return None

    def generate_from_ai_analysis(self, ai_analysis: Dict[str, Any], market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        基于 AI 模型分析结果生成信号

        Args:
            ai_analysis: AI 模型分析结果
            market_data: 市场数据

        Returns:
            信号列表
        """
        try:
            signals = []

            # 提取 AI 分析结果
            sentiment_analysis = ai_analysis.get('sentiment_analysis', {})
            price_prediction = ai_analysis.get('price_prediction', {})
            anomaly_detection = ai_analysis.get('anomaly_detection', {})

            # 处理情感分析结果
            if sentiment_analysis:
                sentiment_signal = self._generate_from_sentiment(sentiment_analysis, market_data)
                if sentiment_signal:
                    signals.append(sentiment_signal)

            # 处理价格预测结果
            if price_prediction:
                price_signal = self._generate_from_price_prediction(price_prediction, market_data)
                if price_signal:
                    signals.append(price_signal)

            # 处理异常检测结果
            if anomaly_detection:
                anomaly_signal = self._generate_from_anomaly_detection(anomaly_detection, market_data)
                if anomaly_signal:
                    signals.append(anomaly_signal)

            return signals

        except Exception as e:
            self.logger.error(f"Error generating signals from AI analysis: {str(e)}")
            return []

    def _generate_from_sentiment(self, sentiment_analysis: Dict[str, Any], market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        基于情感分析结果生成信号

        Args:
            sentiment_analysis: 情感分析结果
            market_data: 市场数据

        Returns:
            信号对象
        """
        try:
            asset = market_data.get('asset', 'BTC')
            sentiment_score = sentiment_analysis.get('average_sentiment', 0)
            confidence = sentiment_analysis.get('confidence', 0.5)

            # 基于情感分数确定信号类型和强度
            if sentiment_score > 0.3:
                # 积极情感
                signal_type = 'buy'
                strength = min(10, int(5 + sentiment_score * 10))
            elif sentiment_score < -0.3:
                # 消极情感
                signal_type = 'sell'
                strength = min(10, int(5 + abs(sentiment_score) * 10))
            else:
                # 中性情感
                signal_type = 'hold'
                strength = 3

            trigger_conditions = {
                'sentiment_score': sentiment_score,
                'confidence': confidence,
                'threshold': 0.3
            }

            return self.generate_signal(
                asset=asset,
                signal_type=signal_type,
                strength=strength,
                confidence=confidence,
                trigger_conditions=trigger_conditions,
                ai_analysis={'sentiment_analysis': sentiment_analysis},
                market_data=market_data
            )

        except Exception as e:
            self.logger.error(f"Error generating signal from sentiment analysis: {str(e)}")
            return None

    def _generate_from_price_prediction(self, price_prediction: Dict[str, Any], market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        基于价格预测结果生成信号

        Args:
            price_prediction: 价格预测结果
            market_data: 市场数据

        Returns:
            信号对象
        """
        try:
            asset = market_data.get('asset', 'BTC')
            predicted_trend = price_prediction.get('predicted_trend', 'stable')
            predicted_change = price_prediction.get('predicted_change', 0)
            confidence = price_prediction.get('confidence', 0.5)

            # 基于价格预测确定信号类型和强度
            if predicted_trend == 'up' and predicted_change > 0.02:
                # 上涨趋势
                signal_type = 'buy'
                strength = min(10, int(5 + predicted_change * 200))
            elif predicted_trend == 'down' and predicted_change < -0.02:
                # 下跌趋势
                signal_type = 'sell'
                strength = min(10, int(5 + abs(predicted_change) * 200))
            else:
                # 稳定趋势
                signal_type = 'hold'
                strength = 3

            trigger_conditions = {
                'predicted_trend': predicted_trend,
                'predicted_change': predicted_change,
                'confidence': confidence,
                'threshold': 0.02
            }

            return self.generate_signal(
                asset=asset,
                signal_type=signal_type,
                strength=strength,
                confidence=confidence,
                trigger_conditions=trigger_conditions,
                ai_analysis={'price_prediction': price_prediction},
                market_data=market_data
            )

        except Exception as e:
            self.logger.error(f"Error generating signal from price prediction: {str(e)}")
            return None

    def _generate_from_anomaly_detection(self, anomaly_detection: Dict[str, Any], market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        基于异常检测结果生成信号

        Args:
            anomaly_detection: 异常检测结果
            market_data: 市场数据

        Returns:
            信号对象
        """
        try:
            asset = market_data.get('asset', 'BTC')
            anomaly_risk = anomaly_detection.get('anomaly_risk', 'low')
            anomaly_count = anomaly_detection.get('anomaly_count', 0)
            confidence = 0.7  # 异常检测的置信度

            # 基于异常风险确定信号类型和强度
            if anomaly_risk == 'high':
                signal_type = 'alert'
                strength = 8
            elif anomaly_risk == 'medium':
                signal_type = 'alert'
                strength = 5
            else:
                # 低风险，不生成信号
                return None

            trigger_conditions = {
                'anomaly_risk': anomaly_risk,
                'anomaly_count': anomaly_count,
                'threshold': 'medium'
            }

            return self.generate_signal(
                asset=asset,
                signal_type=signal_type,
                strength=strength,
                confidence=confidence,
                trigger_conditions=trigger_conditions,
                ai_analysis={'anomaly_detection': anomaly_detection},
                market_data=market_data
            )

        except Exception as e:
            self.logger.error(f"Error generating signal from anomaly detection: {str(e)}")
            return None

    def _calculate_signal_level(self, strength: int, confidence: float) -> str:
        """
        计算信号级别

        Args:
            strength: 信号强度
            confidence: 信号置信度

        Returns:
            信号级别
        """
        combined_score = (strength / 10) * 0.7 + confidence * 0.3

        if combined_score >= 0.9:
            return 'extreme'
        elif combined_score >= 0.7:
            return 'strong'
        elif combined_score >= 0.5:
            return 'medium'
        elif combined_score >= 0.3:
            return 'weak'
        else:
            return 'very_weak'

    def _generate_signal_description(self, signal: Dict[str, Any]) -> str:
        """
        生成信号描述

        Args:
            signal: 信号对象

        Returns:
            信号描述
        """
        asset = signal['asset']
        signal_type = signal['type']
        strength = signal['strength']
        confidence = signal['confidence']
        level = signal['level']

        descriptions = {
            'buy': f"Strong {level} buy signal for {asset} with strength {strength}/10 and confidence {confidence:.2f}",
            'sell': f"Strong {level} sell signal for {asset} with strength {strength}/10 and confidence {confidence:.2f}",
            'hold': f"Neutral hold signal for {asset} with strength {strength}/10 and confidence {confidence:.2f}",
            'alert': f"{level} alert signal for {asset} with strength {strength}/10 and confidence {confidence:.2f}"
        }

        return descriptions.get(signal_type, f"{signal_type} signal for {asset}")

    def validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        验证信号有效性

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

            # 检查信号类型
            valid_types = ['buy', 'sell', 'hold', 'alert', 'opportunity', 'risk']
            if signal['type'] not in valid_types:
                self.logger.error(f"Invalid signal type: {signal['type']}")
                return False

            # 检查信号状态
            if signal.get('status') not in ['active', 'expired', 'canceled']:
                self.logger.error(f"Invalid signal status: {signal.get('status')}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating signal: {str(e)}")
            return False

    def update_signal(self, signal: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新信号

        Args:
            signal: 原始信号
            updates: 更新内容

        Returns:
            更新后的信号
        """
        try:
            # 复制信号
            updated_signal = signal.copy()

            # 应用更新
            for key, value in updates.items():
                if key in ['strength', 'confidence']:
                    # 验证数值更新
                    if key == 'strength' and not 1 <= value <= 10:
                        raise ValueError("Signal strength must be between 1 and 10")
                    elif key == 'confidence' and not 0 <= value <= 1:
                        raise ValueError("Signal confidence must be between 0 and 1")

                updated_signal[key] = value

            # 如果更新了强度或置信度，重新计算级别
            if 'strength' in updates or 'confidence' in updates:
                updated_signal['level'] = self._calculate_signal_level(
                    updated_signal['strength'],
                    updated_signal['confidence']
                )
                updated_signal['description'] = self._generate_signal_description(updated_signal)

            # 更新时间戳
            updated_signal['updated_at'] = datetime.now().isoformat()

            return updated_signal

        except Exception as e:
            self.logger.error(f"Error updating signal: {str(e)}")
            return signal
