# Trend Identifier Module

import logging
import numpy as np
from datetime import datetime

from .nlp.sentiment_analyzer import SentimentAnalyzer
from .time_series.price_predictor import PricePredictor
from .anomaly.anomaly_detector import AnomalyDetector

class TrendIdentifier:
    """
    趋势识别整合模块
    整合多个AI模型的结果，识别加密货币市场趋势
    """

    def __init__(self, config=None):
        """
        初始化趋势识别器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 初始化各个模型
        self.sentiment_analyzer = SentimentAnalyzer(self.config.get('sentiment_analyzer', {}))
        self.price_predictor = PricePredictor(self.config.get('price_predictor', {}))
        self.anomaly_detector = AnomalyDetector(self.config.get('anomaly_detector', {}))

        # 趋势识别参数
        self.sentiment_weight = self.config.get('sentiment_weight', 0.4)
        self.price_weight = self.config.get('price_weight', 0.4)
        self.anomaly_weight = self.config.get('anomaly_weight', 0.2)

    def identify_trends(self, social_media_data=None, price_data=None, market_data=None):
        """
        识别市场趋势

        Args:
            social_media_data: 社交媒体数据
            price_data: 价格数据
            market_data: 市场数据

        Returns:
            趋势识别结果
        """
        try:
            results = {
                'timestamp': datetime.now().isoformat(),
                'models': {},
                'trend_analysis': {},
                'recommendations': []
            }

            # 1. 分析社交媒体情感
            if social_media_data:
                sentiment_results = self._analyze_sentiment(social_media_data)
                results['models']['sentiment_analysis'] = sentiment_results
            else:
                results['models']['sentiment_analysis'] = None

            # 2. 预测价格趋势
            if price_data:
                price_results = self._predict_price_trend(price_data)
                results['models']['price_prediction'] = price_results
            else:
                results['models']['price_prediction'] = None

            # 3. 检测市场异常
            if market_data:
                anomaly_results = self._detect_anomalies(market_data)
                results['models']['anomaly_detection'] = anomaly_results
            else:
                results['models']['anomaly_detection'] = None

            # 4. 整合分析结果
            trend_score, trend_direction = self._integrate_results(results['models'])
            results['trend_analysis']['trend_score'] = trend_score
            results['trend_analysis']['trend_direction'] = trend_direction
            results['trend_analysis']['confidence'] = self._calculate_confidence(results['models'])

            # 5. 生成推荐
            results['recommendations'] = self._generate_recommendations(trend_score, trend_direction, results['models'])

            return results

        except Exception as e:
            self.logger.error(f"Error identifying trends: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _analyze_sentiment(self, social_media_data):
        """
        分析社交媒体情感

        Args:
            social_media_data: 社交媒体数据

        Returns:
            情感分析结果
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

            # 计算总体情感分数
            sentiment_score = 0
            total_confidence = 0

            for result in sentiment_results:
                if result['sentiment'] == 'positive':
                    sentiment_score += result['confidence']
                elif result['sentiment'] == 'negative':
                    sentiment_score -= result['confidence']
                total_confidence += result['confidence']

            if total_confidence > 0:
                average_sentiment = sentiment_score / total_confidence
            else:
                average_sentiment = 0

            # 分析情感分布
            sentiment_counts = {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            }

            for result in sentiment_results:
                sentiment_counts[result['sentiment']] += 1

            return {
                'average_sentiment': average_sentiment,
                'sentiment_counts': sentiment_counts,
                'detailed_results': sentiment_results[:10],  # 只返回前10个结果
                'total_analyzed': len(sentiment_results)
            }

        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return {'error': str(e)}

    def _predict_price_trend(self, price_data):
        """
        预测价格趋势

        Args:
            price_data: 价格数据

        Returns:
            价格预测结果
        """
        try:
            # 确保价格数据格式正确
            if isinstance(price_data, list):
                # 预测未来7天价格
                predictions = self.price_predictor.predict(price_data, days=7)

                # 计算价格趋势
                if len(price_data) >= 2:
                    current_price = price_data[-1]
                    previous_price = price_data[-2]
                    recent_trend = (current_price - previous_price) / previous_price
                else:
                    recent_trend = 0

                # 计算预测趋势
                if predictions:
                    predicted_prices = [p['price'] for p in predictions]
                    predicted_trend = (predicted_prices[-1] - predicted_prices[0]) / predicted_prices[0]
                else:
                    predicted_trend = 0

                return {
                    'recent_trend': recent_trend,
                    'predicted_trend': predicted_trend,
                    'predictions': predictions,
                    'current_price': price_data[-1] if price_data else None
                }
            else:
                return {'error': 'Price data must be a list'}

        except Exception as e:
            self.logger.error(f"Error predicting price trend: {str(e)}")
            return {'error': str(e)}

    def _detect_anomalies(self, market_data):
        """
        检测市场异常

        Args:
            market_data: 市场数据

        Returns:
            异常检测结果
        """
        try:
            # 确保市场数据格式正确
            if isinstance(market_data, list):
                anomaly_results = self.anomaly_detector.predict(market_data)

                # 分析异常情况
                anomalies = [result for result in anomaly_results if result['is_anomaly']]
                anomaly_ratio = len(anomalies) / len(anomaly_results) if anomaly_results else 0

                # 计算异常强度
                if anomalies:
                    average_error = np.mean([a['error'] for a in anomalies])
                    max_error = np.max([a['error'] for a in anomalies])
                else:
                    average_error = 0
                    max_error = 0

                return {
                    'anomaly_count': len(anomalies),
                    'anomaly_ratio': anomaly_ratio,
                    'average_anomaly_error': average_error,
                    'max_anomaly_error': max_error,
                    'detailed_results': anomaly_results[:10]  # 只返回前10个结果
                }
            else:
                return {'error': 'Market data must be a list'}

        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {str(e)}")
            return {'error': str(e)}

    def _integrate_results(self, model_results):
        """
        整合各个模型的结果

        Args:
            model_results: 各个模型的结果

        Returns:
            综合趋势分数和方向
        """
        try:
            # 初始化权重和分数
            weights = []
            scores = []

            # 1. 处理情感分析结果
            if model_results.get('sentiment_analysis') and 'average_sentiment' in model_results['sentiment_analysis']:
                sentiment_score = model_results['sentiment_analysis']['average_sentiment']
                weights.append(self.sentiment_weight)
                scores.append(sentiment_score * self.sentiment_weight)

            # 2. 处理价格预测结果
            if model_results.get('price_prediction') and 'predicted_trend' in model_results['price_prediction']:
                price_score = model_results['price_prediction']['predicted_trend']
                # 标准化价格趋势分数到 [-1, 1] 范围
                price_score = max(-1, min(1, price_score * 10))  # 假设10%的变化是显著的
                weights.append(self.price_weight)
                scores.append(price_score * self.price_weight)

            # 3. 处理异常检测结果
            if model_results.get('anomaly_detection') and 'anomaly_ratio' in model_results['anomaly_detection']:
                anomaly_ratio = model_results['anomaly_detection']['anomaly_ratio']
                # 异常检测分数：异常比例高时降低整体分数的置信度
                anomaly_score = 1 - (anomaly_ratio * 2)  # 异常比例越高，分数越低
                weights.append(self.anomaly_weight)
                scores.append(anomaly_score * self.anomaly_weight)

            # 计算综合分数
            if weights:
                total_weight = sum(weights)
                trend_score = sum(scores) / total_weight
            else:
                trend_score = 0

            # 确定趋势方向
            if trend_score > 0.2:
                trend_direction = 'bullish'
            elif trend_score < -0.2:
                trend_direction = 'bearish'
            else:
                trend_direction = 'neutral'

            return trend_score, trend_direction

        except Exception as e:
            self.logger.error(f"Error integrating results: {str(e)}")
            return 0, 'neutral'

    def _calculate_confidence(self, model_results):
        """
        计算趋势分析的置信度

        Args:
            model_results: 各个模型的结果

        Returns:
            置信度分数
        """
        try:
            confidence = 0
            model_count = 0

            # 情感分析置信度
            if model_results.get('sentiment_analysis') and 'total_analyzed' in model_results['sentiment_analysis']:
                total_analyzed = model_results['sentiment_analysis']['total_analyzed']
                if total_analyzed > 0:
                    # 基于分析的数据量计算置信度
                    sentiment_confidence = min(1.0, total_analyzed / 100)  # 分析100条数据时达到最大置信度
                    confidence += sentiment_confidence
                    model_count += 1

            # 价格预测置信度
            if model_results.get('price_prediction') and 'predictions' in model_results['price_prediction']:
                predictions = model_results['price_prediction']['predictions']
                if predictions:
                    # 基于价格数据的长度计算置信度
                    price_confidence = 0.7  # 固定置信度
                    confidence += price_confidence
                    model_count += 1

            # 异常检测置信度
            if model_results.get('anomaly_detection') and 'anomaly_count' in model_results['anomaly_detection']:
                anomaly_count = model_results['anomaly_detection']['anomaly_count']
                # 基于异常检测结果计算置信度
                anomaly_confidence = 0.6  # 固定置信度
                confidence += anomaly_confidence
                model_count += 1

            # 计算平均置信度
            if model_count > 0:
                average_confidence = confidence / model_count
            else:
                average_confidence = 0

            return average_confidence

        except Exception as e:
            self.logger.error(f"Error calculating confidence: {str(e)}")
            return 0

    def _generate_recommendations(self, trend_score, trend_direction, model_results):
        """
        基于趋势分析生成推荐

        Args:
            trend_score: 趋势分数
            trend_direction: 趋势方向
            model_results: 各个模型的结果

        Returns:
            推荐列表
        """
        try:
            recommendations = []

            # 基于趋势方向生成推荐
            if trend_direction == 'bullish':
                recommendations.append({
                    'type': 'investment',
                    'action': 'buy',
                    'confidence': min(1.0, trend_score * 5),
                    'reason': 'Positive market trend detected'
                })

                # 检查是否有异常
                if model_results.get('anomaly_detection') and model_results['anomaly_detection'].get('anomaly_ratio', 0) > 0.3:
                    recommendations.append({
                        'type': 'warning',
                        'action': 'monitor',
                        'confidence': 0.7,
                        'reason': 'High anomaly ratio detected, monitor for potential market reversal'
                    })

            elif trend_direction == 'bearish':
                recommendations.append({
                    'type': 'investment',
                    'action': 'sell',
                    'confidence': min(1.0, abs(trend_score) * 5),
                    'reason': 'Negative market trend detected'
                })

                recommendations.append({
                    'type': 'strategy',
                    'action': 'short',
                    'confidence': min(1.0, abs(trend_score) * 3),
                    'reason': 'Consider shorting opportunities during bearish trends'
                })

            else:  # neutral
                recommendations.append({
                    'type': 'investment',
                    'action': 'hold',
                    'confidence': 0.8,
                    'reason': 'Neutral market trend detected'
                })

                recommendations.append({
                    'type': 'strategy',
                    'action': 'accumulate',
                    'confidence': 0.6,
                    'reason': 'Consider dollar-cost averaging during neutral trends'
                })

            # 基于情感分析生成推荐
            if model_results.get('sentiment_analysis') and 'sentiment_counts' in model_results['sentiment_analysis']:
                sentiment_counts = model_results['sentiment_analysis']['sentiment_counts']
                total = sum(sentiment_counts.values())

                if total > 0:
                    positive_ratio = sentiment_counts['positive'] / total
                    negative_ratio = sentiment_counts['negative'] / total

                    if positive_ratio > 0.6:
                        recommendations.append({
                            'type': 'sentiment',
                            'action': 'buy',
                            'confidence': min(1.0, positive_ratio),
                            'reason': 'Strong positive sentiment detected on social media'
                        })
                    elif negative_ratio > 0.6:
                        recommendations.append({
                            'type': 'sentiment',
                            'action': 'sell',
                            'confidence': min(1.0, negative_ratio),
                            'reason': 'Strong negative sentiment detected on social media'
                        })

            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def train_models(self, sentiment_data=None, price_data=None, market_data=None):
        """
        训练所有模型

        Args:
            sentiment_data: 情感分析训练数据
            price_data: 价格预测训练数据
            market_data: 异常检测训练数据

        Returns:
            训练结果
        """
        try:
            training_results = {
                'timestamp': datetime.now().isoformat(),
                'models': {}
            }

            # 训练情感分析模型
            if sentiment_data and isinstance(sentiment_data, dict) and 'texts' in sentiment_data and 'labels' in sentiment_data:
                sentiment_result = self.sentiment_analyzer.train(
                    sentiment_data['texts'],
                    sentiment_data['labels']
                )
                training_results['models']['sentiment_analyzer'] = sentiment_result

            # 训练价格预测模型
            if price_data and isinstance(price_data, list):
                price_result = self.price_predictor.train(price_data)
                training_results['models']['price_predictor'] = price_result

            # 训练异常检测模型
            if market_data and isinstance(market_data, list):
                anomaly_result = self.anomaly_detector.train(market_data)
                training_results['models']['anomaly_detector'] = anomaly_result

            return training_results

        except Exception as e:
            self.logger.error(f"Error training models: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
