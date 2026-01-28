# Trend Predictor Module

import logging
import numpy as np
from datetime import datetime, timedelta
import json
import os

from ..models.nlp.sentiment_analyzer import SentimentAnalyzer
from ..models.time_series.price_predictor import PricePredictor
from ..models.anomaly.anomaly_detector import AnomalyDetector
from ..models.trend_identifier import TrendIdentifier

class TrendPredictor:
    """
    趋势预测器
    整合各个模型的预测结果，提供统一的预测接口
    """

    def __init__(self, config=None):
        """
        初始化趋势预测器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 初始化各个模型
        self.sentiment_analyzer = SentimentAnalyzer(self.config.get('sentiment_analyzer', {}))
        self.price_predictor = PricePredictor(self.config.get('price_predictor', {}))
        self.anomaly_detector = AnomalyDetector(self.config.get('anomaly_detector', {}))
        self.trend_identifier = TrendIdentifier(self.config.get('trend_identifier', {}))

        # 预测参数
        self.prediction_days = self.config.get('prediction_days', 7)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.7)

    def predict_market_trend(self, social_media_data=None, price_data=None, market_data=None):
        """
        预测市场趋势

        Args:
            social_media_data: 社交媒体数据
            price_data: 价格数据
            market_data: 市场数据

        Returns:
            市场趋势预测结果
        """
        try:
            results = {
                'timestamp': datetime.now().isoformat(),
                'prediction_horizon': f'{self.prediction_days} days',
                'models': {},
                'market_trend': {},
                'predictions': [],
                'confidence': 0
            }

            # 1. 分析社交媒体情感趋势
            if social_media_data:
                sentiment_prediction = self._predict_sentiment_trend(social_media_data)
                results['models']['sentiment_prediction'] = sentiment_prediction
            else:
                results['models']['sentiment_prediction'] = None

            # 2. 预测价格趋势
            if price_data:
                price_prediction = self._predict_price_movement(price_data)
                results['models']['price_prediction'] = price_prediction
            else:
                results['models']['price_prediction'] = None

            # 3. 检测潜在异常
            if market_data:
                anomaly_prediction = self._predict_anomalies(market_data)
                results['models']['anomaly_prediction'] = anomaly_prediction
            else:
                results['models']['anomaly_prediction'] = None

            # 4. 整合趋势分析
            trend_analysis = self.trend_identifier.identify_trends(
                social_media_data=social_media_data,
                price_data=price_data,
                market_data=market_data
            )
            results['market_trend'] = trend_analysis

            # 5. 生成综合预测
            comprehensive_predictions = self._generate_comprehensive_predictions(
                sentiment_prediction,
                price_prediction,
                anomaly_prediction,
                trend_analysis
            )
            results['predictions'] = comprehensive_predictions

            # 6. 计算整体置信度
            results['confidence'] = self._calculate_overall_confidence(results['models'])

            # 7. 生成投资建议
            results['investment_advice'] = self._generate_investment_advice(results)

            # 保存预测结果
            result_path = os.path.join('.', f"market_trend_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            results['result_path'] = result_path

            return results

        except Exception as e:
            self.logger.error(f"Error predicting market trend: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _predict_sentiment_trend(self, social_media_data):
        """
        预测情感趋势

        Args:
            social_media_data: 社交媒体数据

        Returns:
            情感趋势预测结果
        """
        try:
            # 提取文本数据
            texts = []
            if isinstance(social_media_data, list):
                for item in social_media_data:
                    if isinstance(item, dict) and 'text' in item:
                        texts.append(item['text'])
                    elif isinstance(item, str):
                        texts.append(item)
            elif isinstance(social_media_data, str):
                texts = [social_media_data]

            if not texts:
                return {'error': 'No text data provided'}

            # 预测情感
            sentiment_results = self.sentiment_analyzer.predict(texts)

            # 分析情感趋势
            sentiment_counts = {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            }

            total_confidence = 0
            for result in sentiment_results:
                sentiment_counts[result['sentiment']] += 1
                total_confidence += result['confidence']

            # 计算情感趋势
            total = sum(sentiment_counts.values())
            sentiment_trend = {
                'positive_ratio': sentiment_counts['positive'] / total if total > 0 else 0,
                'neutral_ratio': sentiment_counts['neutral'] / total if total > 0 else 0,
                'negative_ratio': sentiment_counts['negative'] / total if total > 0 else 0,
                'average_confidence': total_confidence / len(sentiment_results) if sentiment_results else 0,
                'dominant_sentiment': max(sentiment_counts, key=sentiment_counts.get)
            }

            # 预测未来情感趋势（基于当前情感分布）
            future_sentiment = self._predict_future_sentiment(sentiment_trend)

            return {
                'current_sentiment': sentiment_trend,
                'future_sentiment': future_sentiment,
                'total_analyzed': len(sentiment_results),
                'detailed_results': sentiment_results[:5]  # 只返回前5个结果
            }

        except Exception as e:
            self.logger.error(f"Error predicting sentiment trend: {str(e)}")
            return {'error': str(e)}

    def _predict_price_movement(self, price_data):
        """
        预测价格走势

        Args:
            price_data: 价格数据

        Returns:
            价格走势预测结果
        """
        try:
            # 预测未来价格
            price_predictions = self.price_predictor.predict(price_data, days=self.prediction_days)

            # 分析当前价格趋势
            if len(price_data) >= 2:
                current_price = price_data[-1]
                previous_price = price_data[-2]
                recent_change = (current_price - previous_price) / previous_price
                recent_trend = 'up' if recent_change > 0 else 'down' if recent_change < 0 else 'stable'
            else:
                recent_change = 0
                recent_trend = 'stable'

            # 分析预测价格趋势
            if price_predictions:
                predicted_prices = [p['price'] for p in price_predictions]
                predicted_change = (predicted_prices[-1] - predicted_prices[0]) / predicted_prices[0]
                predicted_trend = 'up' if predicted_change > 0 else 'down' if predicted_change < 0 else 'stable'
                price_volatility = np.std(predicted_prices) / np.mean(predicted_prices) if predicted_prices else 0
            else:
                predicted_change = 0
                predicted_trend = 'stable'
                price_volatility = 0

            # 计算价格预测置信度
            confidence = self._calculate_price_prediction_confidence(price_data, predicted_prices)

            return {
                'current_price': price_data[-1] if price_data else None,
                'recent_change': float(recent_change),
                'recent_trend': recent_trend,
                'predicted_prices': price_predictions,
                'predicted_change': float(predicted_change),
                'predicted_trend': predicted_trend,
                'price_volatility': float(price_volatility),
                'confidence': float(confidence)
            }

        except Exception as e:
            self.logger.error(f"Error predicting price movement: {str(e)}")
            return {'error': str(e)}

    def _predict_anomalies(self, market_data):
        """
        预测潜在异常

        Args:
            market_data: 市场数据

        Returns:
            异常预测结果
        """
        try:
            # 检测异常
            anomaly_results = self.anomaly_detector.predict(market_data)

            # 分析异常情况
            anomalies = [result for result in anomaly_results if result['is_anomaly']]
            anomaly_ratio = len(anomalies) / len(anomaly_results) if anomaly_results else 0

            # 预测未来异常风险
            anomaly_risk = self._predict_anomaly_risk(anomalies, market_data)

            return {
                'anomaly_count': len(anomalies),
                'anomaly_ratio': float(anomaly_ratio),
                'anomaly_risk': anomaly_risk,
                'detailed_results': anomaly_results[:5],  # 只返回前5个结果
                'threshold': self.anomaly_detector.threshold
            }

        except Exception as e:
            self.logger.error(f"Error predicting anomalies: {str(e)}")
            return {'error': str(e)}

    def _predict_future_sentiment(self, current_sentiment):
        """
        预测未来情感趋势

        Args:
            current_sentiment: 当前情感趋势

        Returns:
            未来情感趋势预测
        """
        try:
            # 基于当前情感分布预测未来趋势
            # 简单的趋势外推（实际应用中可以使用更复杂的方法）
            future_sentiment = {
                'positive_ratio': current_sentiment['positive_ratio'],
                'neutral_ratio': current_sentiment['neutral_ratio'],
                'negative_ratio': current_sentiment['negative_ratio'],
                'confidence': current_sentiment['average_confidence'] * 0.8  # 未来预测置信度降低
            }

            # 根据主导情感调整预测
            if current_sentiment['dominant_sentiment'] == 'positive':
                # 积极情感可能会持续
                future_sentiment['positive_ratio'] = min(1.0, future_sentiment['positive_ratio'] * 1.1)
                future_sentiment['negative_ratio'] = max(0.0, future_sentiment['negative_ratio'] * 0.9)
            elif current_sentiment['dominant_sentiment'] == 'negative':
                # 消极情感可能会持续
                future_sentiment['negative_ratio'] = min(1.0, future_sentiment['negative_ratio'] * 1.1)
                future_sentiment['positive_ratio'] = max(0.0, future_sentiment['positive_ratio'] * 0.9)

            return future_sentiment

        except Exception as e:
            self.logger.error(f"Error predicting future sentiment: {str(e)}")
            return current_sentiment

    def _calculate_price_prediction_confidence(self, historical_prices, predicted_prices):
        """
        计算价格预测置信度

        Args:
            historical_prices: 历史价格数据
            predicted_prices: 预测价格数据

        Returns:
            置信度分数
        """
        try:
            if not historical_prices or not predicted_prices:
                return 0.5

            # 基于历史价格波动性计算置信度
            historical_volatility = np.std(historical_prices[-30:]) / np.mean(historical_prices[-30:]) if len(historical_prices) >= 30 else 0

            # 基于预测价格趋势的一致性计算置信度
            if len(predicted_prices) >= 2:
                price_changes = np.diff(predicted_prices)
                trend_consistency = np.sum(price_changes > 0) / len(price_changes) if len(price_changes) > 0 else 0.5
                trend_consistency = max(trend_consistency, 1 - trend_consistency)  # 转换为一致性分数
            else:
                trend_consistency = 0.5

            # 综合计算置信度
            confidence = (1 - historical_volatility) * 0.6 + trend_consistency * 0.4
            confidence = max(0.1, min(1.0, confidence))

            return confidence

        except Exception as e:
            self.logger.error(f"Error calculating price prediction confidence: {str(e)}")
            return 0.5

    def _predict_anomaly_risk(self, anomalies, market_data):
        """
        预测异常风险

        Args:
            anomalies: 检测到的异常
            market_data: 市场数据

        Returns:
            异常风险等级
        """
        try:
            if not anomalies:
                return 'low'

            # 基于异常数量和严重程度计算风险
            anomaly_count = len(anomalies)
            average_error = np.mean([a['error'] for a in anomalies]) if anomalies else 0

            # 计算风险等级
            if anomaly_count > 5 and average_error > 0.1:
                return 'high'
            elif anomaly_count > 2 or average_error > 0.05:
                return 'medium'
            else:
                return 'low'

        except Exception as e:
            self.logger.error(f"Error predicting anomaly risk: {str(e)}")
            return 'medium'

    def _generate_comprehensive_predictions(self, sentiment_prediction, price_prediction, anomaly_prediction, trend_analysis):
        """
        生成综合预测

        Args:
            sentiment_prediction: 情感预测结果
            price_prediction: 价格预测结果
            anomaly_prediction: 异常预测结果
            trend_analysis: 趋势分析结果

        Returns:
            综合预测结果
        """
        try:
            predictions = []

            # 基于趋势分析生成预测
            trend_direction = trend_analysis.get('trend_analysis', {}).get('trend_direction', 'neutral')
            trend_score = trend_analysis.get('trend_analysis', {}).get('trend_score', 0)
            confidence = trend_analysis.get('trend_analysis', {}).get('confidence', 0)

            # 生成每日预测
            for i in range(1, self.prediction_days + 1):
                # 计算每日趋势强度（简单线性衰减）
                daily_trend_strength = trend_score * (1 - (i - 1) / (self.prediction_days * 2))

                # 确定每日趋势方向
                if daily_trend_strength > 0.1:
                    daily_direction = 'bullish'
                elif daily_trend_strength < -0.1:
                    daily_direction = 'bearish'
                else:
                    daily_direction = 'neutral'

                # 计算每日置信度（随时间衰减）
                daily_confidence = confidence * (1 - (i - 1) / self.prediction_days)

                # 添加预测结果
                predictions.append({
                    'day': i,
                    'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                    'trend_direction': daily_direction,
                    'trend_strength': float(daily_trend_strength),
                    'confidence': float(daily_confidence),
                    'factors': {
                        'sentiment': sentiment_prediction.get('future_sentiment', {}).get('dominant_sentiment') if sentiment_prediction else None,
                        'price_trend': price_prediction.get('predicted_trend') if price_prediction else None,
                        'anomaly_risk': anomaly_prediction.get('anomaly_risk') if anomaly_prediction else None
                    }
                })

            return predictions

        except Exception as e:
            self.logger.error(f"Error generating comprehensive predictions: {str(e)}")
            return []

    def _calculate_overall_confidence(self, model_results):
        """
        计算整体置信度

        Args:
            model_results: 各个模型的结果

        Returns:
            整体置信度分数
        """
        try:
            confidences = []

            # 情感分析置信度
            if model_results.get('sentiment_prediction') and 'future_sentiment' in model_results['sentiment_prediction']:
                sentiment_confidence = model_results['sentiment_prediction']['future_sentiment'].get('confidence', 0)
                confidences.append(sentiment_confidence)

            # 价格预测置信度
            if model_results.get('price_prediction') and 'confidence' in model_results['price_prediction']:
                price_confidence = model_results['price_prediction']['confidence']
                confidences.append(price_confidence)

            # 异常检测置信度（反向）
            if model_results.get('anomaly_prediction') and 'anomaly_risk' in model_results['anomaly_prediction']:
                anomaly_risk = model_results['anomaly_prediction']['anomaly_risk']
                if anomaly_risk == 'low':
                    anomaly_confidence = 0.9
                elif anomaly_risk == 'medium':
                    anomaly_confidence = 0.7
                else:
                    anomaly_confidence = 0.5
                confidences.append(anomaly_confidence)

            # 计算平均置信度
            if confidences:
                overall_confidence = np.mean(confidences)
            else:
                overall_confidence = 0.5

            return float(overall_confidence)

        except Exception as e:
            self.logger.error(f"Error calculating overall confidence: {str(e)}")
            return 0.5

    def _generate_investment_advice(self, prediction_results):
        """
        生成投资建议

        Args:
            prediction_results: 预测结果

        Returns:
            投资建议
        """
        try:
            advice = []

            # 获取关键预测信息
            trend_direction = prediction_results.get('market_trend', {}).get('trend_analysis', {}).get('trend_direction', 'neutral')
            confidence = prediction_results.get('confidence', 0)
            predictions = prediction_results.get('predictions', [])

            # 基于趋势方向生成建议
            if trend_direction == 'bullish' and confidence >= self.confidence_threshold:
                advice.append({
                    'type': 'investment',
                    'action': 'buy',
                    'confidence': float(confidence),
                    'reason': 'Strong bullish trend predicted with high confidence',
                    'timeframe': f'{self.prediction_days}-day horizon'
                })

                advice.append({
                    'type': 'strategy',
                    'action': 'hold',
                    'confidence': float(confidence * 0.8),
                    'reason': 'Expected continued uptrend',
                    'timeframe': 'Medium-term'
                })

            elif trend_direction == 'bearish' and confidence >= self.confidence_threshold:
                advice.append({
                    'type': 'investment',
                    'action': 'sell',
                    'confidence': float(confidence),
                    'reason': 'Strong bearish trend predicted with high confidence',
                    'timeframe': f'{self.prediction_days}-day horizon'
                })

                advice.append({
                    'type': 'strategy',
                    'action': 'hedge',
                    'confidence': float(confidence * 0.7),
                    'reason': 'Protect against further downside',
                    'timeframe': 'Short-term'
                })

            else:
                advice.append({
                    'type': 'investment',
                    'action': 'hold',
                    'confidence': 0.8,
                    'reason': 'Neutral or uncertain trend predicted',
                    'timeframe': 'Wait for clearer signals'
                })

                advice.append({
                    'type': 'strategy',
                    'action': 'diversify',
                    'confidence': 0.7,
                    'reason': 'Reduce risk during uncertain market conditions',
                    'timeframe': 'Ongoing'
                })

            # 基于异常风险添加警告
            anomaly_risk = prediction_results.get('models', {}).get('anomaly_prediction', {}).get('anomaly_risk')
            if anomaly_risk == 'high':
                advice.append({
                    'type': 'warning',
                    'action': 'monitor',
                    'confidence': 0.9,
                    'reason': 'High anomaly risk detected, potential market volatility',
                    'timeframe': 'Immediate'
                })

            return advice

        except Exception as e:
            self.logger.error(f"Error generating investment advice: {str(e)}")
            return []

    def save_prediction_results(self, results, file_path=None):
        """
        保存预测结果

        Args:
            results: 预测结果
            file_path: 保存路径

        Returns:
            保存路径
        """
        try:
            if not file_path:
                file_path = os.path.join('.', f"trend_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            return file_path

        except Exception as e:
            self.logger.error(f"Error saving prediction results: {str(e)}")
            return None
