# Signal Classifier

import logging
from typing import Dict, List, Optional, Any

class SignalClassifier:
    """
    信号分类器
    对信号进行多维度分类和级别评估
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化信号分类器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 分类参数
        self.strength_thresholds = self.config.get('strength_thresholds', {
            'extreme': 9,
            'strong': 7,
            'medium': 5,
            'weak': 3,
            'very_weak': 0
        })

        self.confidence_thresholds = self.config.get('confidence_thresholds', {
            'high': 0.8,
            'medium': 0.5,
            'low': 0.3
        })

    def classify_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        分类信号

        Args:
            signal: 信号对象

        Returns:
            分类结果
        """
        try:
            # 验证信号
            if not self._validate_signal(signal):
                self.logger.error("Invalid signal for classification")
                return None

            # 分类结果
            classification = {
                'signal_id': signal['signal_id'],
                'strength_category': self._classify_strength(signal['strength']),
                'confidence_category': self._classify_confidence(signal['confidence']),
                'level': self._classify_level(signal),
                'risk_level': self._classify_risk(signal),
                'time_sensitivity': self._classify_time_sensitivity(signal),
                'asset_class': self._classify_asset(signal),
                'trend_alignment': self._classify_trend_alignment(signal),
                'comprehensive_category': self._classify_comprehensive(signal)
            }

            self.logger.info(f"Classified signal {signal['signal_id']} as {classification['level']} level")

            return classification

        except Exception as e:
            self.logger.error(f"Error classifying signal: {str(e)}")
            return None

    def classify_multiple_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        分类多个信号

        Args:
            signals: 信号列表

        Returns:
            分类结果列表
        """
        try:
            classified_signals = []
            for signal in signals:
                classification = self.classify_signal(signal)
                if classification:
                    signal_with_classification = signal.copy()
                    signal_with_classification['classification'] = classification
                    classified_signals.append(signal_with_classification)

            return classified_signals

        except Exception as e:
            self.logger.error(f"Error classifying multiple signals: {str(e)}")
            return []

    def _validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        验证信号

        Args:
            signal: 信号对象

        Returns:
            是否有效
        """
        try:
            required_fields = ['signal_id', 'asset', 'type', 'strength', 'confidence']
            for field in required_fields:
                if field not in signal:
                    self.logger.error(f"Missing required field {field} in signal")
                    return False

            if not 1 <= signal['strength'] <= 10:
                self.logger.error(f"Invalid signal strength: {signal['strength']}")
                return False

            if not 0 <= signal['confidence'] <= 1:
                self.logger.error(f"Invalid signal confidence: {signal['confidence']}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating signal: {str(e)}")
            return False

    def _classify_strength(self, strength: int) -> str:
        """
        分类信号强度

        Args:
            strength: 信号强度

        Returns:
            强度类别
        """
        if strength >= self.strength_thresholds['extreme']:
            return 'extreme'
        elif strength >= self.strength_thresholds['strong']:
            return 'strong'
        elif strength >= self.strength_thresholds['medium']:
            return 'medium'
        elif strength >= self.strength_thresholds['weak']:
            return 'weak'
        else:
            return 'very_weak'

    def _classify_confidence(self, confidence: float) -> str:
        """
        分类信号置信度

        Args:
            confidence: 信号置信度

        Returns:
            置信度类别
        """
        if confidence >= self.confidence_thresholds['high']:
            return 'high'
        elif confidence >= self.confidence_thresholds['medium']:
            return 'medium'
        elif confidence >= self.confidence_thresholds['low']:
            return 'low'
        else:
            return 'very_low'

    def _classify_level(self, signal: Dict[str, Any]) -> str:
        """
        分类信号级别

        Args:
            signal: 信号对象

        Returns:
            信号级别
        """
        strength = signal['strength']
        confidence = signal['confidence']

        # 计算综合分数
        composite_score = (strength / 10) * 0.6 + confidence * 0.4

        if composite_score >= 0.9:
            return 'extreme'
        elif composite_score >= 0.7:
            return 'strong'
        elif composite_score >= 0.5:
            return 'medium'
        elif composite_score >= 0.3:
            return 'weak'
        else:
            return 'very_weak'

    def _classify_risk(self, signal: Dict[str, Any]) -> str:
        """
        分类信号风险等级

        Args:
            signal: 信号对象

        Returns:
            风险等级
        """
        signal_type = signal['type']
        strength = signal['strength']
        confidence = signal['confidence']

        # 基础风险评估
        base_risk = 0.5

        # 根据信号类型调整风险
        if signal_type == 'sell':
            base_risk -= 0.1  # 卖出信号风险较低
        elif signal_type == 'buy':
            base_risk += 0.1  # 买入信号风险较高
        elif signal_type == 'alert':
            base_risk += 0.2  # 预警信号风险较高

        # 根据信号强度调整风险
        if strength >= 8:
            base_risk += 0.1  # 高强度信号风险较高
        elif strength <= 3:
            base_risk -= 0.1  # 低强度信号风险较低

        # 根据置信度调整风险
        if confidence >= 0.8:
            base_risk -= 0.1  # 高置信度风险较低
        elif confidence <= 0.4:
            base_risk += 0.1  # 低置信度风险较高

        # 确定风险等级
        if base_risk >= 0.7:
            return 'high'
        elif base_risk >= 0.4:
            return 'medium'
        else:
            return 'low'

    def _classify_time_sensitivity(self, signal: Dict[str, Any]) -> str:
        """
        分类信号时间敏感度

        Args:
            signal: 信号对象

        Returns:
            时间敏感度
        """
        signal_type = signal['type']
        strength = signal['strength']
        confidence = signal['confidence']

        # 计算时间敏感度分数
        sensitivity_score = 0.5

        # 根据信号类型调整
        if signal_type == 'alert':
            sensitivity_score = 0.9
        elif signal_type == 'buy' or signal_type == 'sell':
            sensitivity_score = 0.7
        elif signal_type == 'hold':
            sensitivity_score = 0.3

        # 根据强度和置信度调整
        if strength >= 8 and confidence >= 0.8:
            sensitivity_score = min(1.0, sensitivity_score + 0.2)
        elif strength <= 3 or confidence <= 0.4:
            sensitivity_score = max(0.1, sensitivity_score - 0.2)

        # 确定时间敏感度等级
        if sensitivity_score >= 0.8:
            return 'urgent'
        elif sensitivity_score >= 0.5:
            return 'time-sensitive'
        else:
            return 'non-urgent'

    def _classify_asset(self, signal: Dict[str, Any]) -> str:
        """
        分类资产类型

        Args:
            signal: 信号对象

        Returns:
            资产类型
        """
        asset = signal['asset'].upper()

        # 主流加密货币
        major_cryptos = ['BTC', 'ETH']
        if asset in major_cryptos:
            return 'major_crypto'

        # 二线加密货币
        secondary_cryptos = ['SOL', 'ADA', 'DOT', 'DOGE', 'SHIB']
        if asset in secondary_cryptos:
            return 'secondary_crypto'

        # 稳定币
        stablecoins = ['USDT', 'USDC', 'DAI', 'BUSD']
        if asset in stablecoins:
            return 'stablecoin'

        # 其他加密货币
        if asset.endswith('BTC') or asset.endswith('ETH') or asset.endswith('SOL'):
            return 'derivative_crypto'

        # 非加密货币资产
        if asset in ['GOLD', 'SILVER', 'USD', 'EUR', 'JPY']:
            return 'traditional_asset'

        # 默认分类
        return 'other_crypto'

    def _classify_trend_alignment(self, signal: Dict[str, Any]) -> str:
        """
        分类信号与市场趋势的一致性

        Args:
            signal: 信号对象

        Returns:
            趋势一致性
        """
        signal_type = signal['type']
        market_data = signal.get('market_data', {})
        market_trend = market_data.get('market_trend', 'neutral')

        # 评估趋势一致性
        if signal_type == 'buy' and market_trend == 'up':
            return 'strongly_aligned'
        elif signal_type == 'sell' and market_trend == 'down':
            return 'strongly_aligned'
        elif signal_type == 'buy' and market_trend == 'down':
            return 'opposite'
        elif signal_type == 'sell' and market_trend == 'up':
            return 'opposite'
        elif signal_type == 'hold' and market_trend == 'neutral':
            return 'aligned'
        else:
            return 'partially_aligned'

    def _classify_comprehensive(self, signal: Dict[str, Any]) -> str:
        """
        综合分类信号

        Args:
            signal: 信号对象

        Returns:
            综合分类
        """
        level = self._classify_level(signal)
        risk_level = self._classify_risk(signal)
        time_sensitivity = self._classify_time_sensitivity(signal)

        # 综合分类逻辑
        if level in ['extreme', 'strong'] and risk_level in ['medium', 'low']:
            return 'high_quality'
        elif level in ['extreme', 'strong'] and risk_level == 'high':
            return 'high_risk_high_reward'
        elif level == 'medium' and risk_level == 'medium':
            return 'balanced'
        elif level in ['weak', 'very_weak'] and risk_level == 'low':
            return 'low_impact'
        elif level in ['weak', 'very_weak'] and risk_level == 'high':
            return 'low_confidence_high_risk'
        else:
            return 'standard'

    def get_signal_statistics(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取信号分类统计信息

        Args:
            signals: 信号列表

        Returns:
            统计信息
        """
        try:
            if not signals:
                return {
                    'total_signals': 0,
                    'level_distribution': {},
                    'risk_distribution': {},
                    'type_distribution': {},
                    'asset_class_distribution': {},
                    'time_sensitivity_distribution': {}
                }

            # 分类所有信号
            classified_signals = self.classify_multiple_signals(signals)

            # 计算基本统计
            total_signals = len(classified_signals)

            # 计算级别分布
            level_distribution = {}
            for signal in classified_signals:
                level = signal['classification']['level']
                level_distribution[level] = level_distribution.get(level, 0) + 1

            # 计算风险分布
            risk_distribution = {}
            for signal in classified_signals:
                risk = signal['classification']['risk_level']
                risk_distribution[risk] = risk_distribution.get(risk, 0) + 1

            # 计算类型分布
            type_distribution = {}
            for signal in classified_signals:
                signal_type = signal['type']
                type_distribution[signal_type] = type_distribution.get(signal_type, 0) + 1

            # 计算资产类别分布
            asset_class_distribution = {}
            for signal in classified_signals:
                asset_class = signal['classification']['asset_class']
                asset_class_distribution[asset_class] = asset_class_distribution.get(asset_class, 0) + 1

            # 计算时间敏感度分布
            time_sensitivity_distribution = {}
            for signal in classified_signals:
                sensitivity = signal['classification']['time_sensitivity']
                time_sensitivity_distribution[sensitivity] = time_sensitivity_distribution.get(sensitivity, 0) + 1

            return {
                'total_signals': total_signals,
                'level_distribution': level_distribution,
                'risk_distribution': risk_distribution,
                'type_distribution': type_distribution,
                'asset_class_distribution': asset_class_distribution,
                'time_sensitivity_distribution': time_sensitivity_distribution
            }

        except Exception as e:
            self.logger.error(f"Error getting signal statistics: {str(e)}")
            return {}

    def update_classification_config(self, config: Dict[str, Any]) -> bool:
        """
        更新分类配置

        Args:
            config: 配置参数

        Returns:
            是否成功
        """
        try:
            if 'strength_thresholds' in config:
                self.strength_thresholds = config['strength_thresholds']

            if 'confidence_thresholds' in config:
                self.confidence_thresholds = config['confidence_thresholds']

            self.logger.info("Updated classification config")
            return True

        except Exception as e:
            self.logger.error(f"Error updating classification config: {str(e)}")
            return False
