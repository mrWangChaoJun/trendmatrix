# Model Evaluator Module

import logging
import numpy as np
import json
from datetime import datetime
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    mean_squared_error, mean_absolute_error, r2_score
)

class ModelEvaluator:
    """
    模型评估器
    用于评估各个AI模型的性能
    """

    def __init__(self, config=None):
        """
        初始化模型评估器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def evaluate_sentiment_analyzer(self, model, test_texts, test_labels):
        """
        评估情感分析模型

        Args:
            model: 情感分析模型
            test_texts: 测试文本数据
            test_labels: 测试标签数据

        Returns:
            评估结果
        """
        try:
            # 预测
            predictions = model.predict(test_texts)

            # 提取预测标签
            predicted_labels = []
            for pred in predictions:
                if pred['sentiment'] == 'positive':
                    predicted_labels.append(2)
                elif pred['sentiment'] == 'negative':
                    predicted_labels.append(0)
                else:
                    predicted_labels.append(1)

            # 计算评估指标
            accuracy = accuracy_score(test_labels, predicted_labels)
            precision = precision_score(test_labels, predicted_labels, average='weighted')
            recall = recall_score(test_labels, predicted_labels, average='weighted')
            f1 = f1_score(test_labels, predicted_labels, average='weighted')

            # 生成分类报告
            class_report = classification_report(test_labels, predicted_labels, output_dict=True)

            # 生成混淆矩阵
            conf_matrix = confusion_matrix(test_labels, predicted_labels).tolist()

            # 分析情感分布
            sentiment_counts = {
                'positive': sum(1 for label in test_labels if label == 2),
                'neutral': sum(1 for label in test_labels if label == 1),
                'negative': sum(1 for label in test_labels if label == 0)
            }

            return {
                'timestamp': datetime.now().isoformat(),
                'model_type': 'sentiment_analyzer',
                'metrics': {
                    'accuracy': float(accuracy),
                    'precision': float(precision),
                    'recall': float(recall),
                    'f1_score': float(f1)
                },
                'classification_report': class_report,
                'confusion_matrix': conf_matrix,
                'sentiment_distribution': sentiment_counts,
                'test_size': len(test_texts)
            }

        except Exception as e:
            self.logger.error(f"Error evaluating sentiment analyzer: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def evaluate_price_predictor(self, model, test_prices, look_back=60):
        """
        评估价格预测模型

        Args:
            model: 价格预测模型
            test_prices: 测试价格数据
            look_back: 回溯窗口大小

        Returns:
            评估结果
        """
        try:
            # 数据预处理
            test_prices = np.array(test_prices).reshape(-1, 1)

            # 确保有足够的数据
            if len(test_prices) <= look_back:
                return {
                    'error': 'Insufficient test data',
                    'timestamp': datetime.now().isoformat()
                }

            # 创建测试数据
            X_test, y_test = self._create_dataset(test_prices, look_back)

            # 预测
            predictions = []
            for i in range(len(X_test)):
                # 预测下一个值
                pred = model.predict(X_test[i].tolist())
                if pred:
                    predictions.append(pred[0]['price'])
                else:
                    predictions.append(0)

            # 计算评估指标
            mse = mean_squared_error(y_test, predictions)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            # 计算平均绝对百分比误差
            mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

            # 分析预测偏差
            errors = y_test - predictions
            avg_error = np.mean(errors)
            std_error = np.std(errors)

            # 计算方向准确率
            direction_accuracy = self._calculate_direction_accuracy(y_test, predictions)

            return {
                'timestamp': datetime.now().isoformat(),
                'model_type': 'price_predictor',
                'metrics': {
                    'mse': float(mse),
                    'rmse': float(rmse),
                    'mae': float(mae),
                    'r2': float(r2),
                    'mape': float(mape),
                    'direction_accuracy': float(direction_accuracy)
                },
                'error_analysis': {
                    'average_error': float(avg_error),
                    'std_error': float(std_error),
                    'min_error': float(np.min(errors)),
                    'max_error': float(np.max(errors))
                },
                'test_size': len(X_test),
                'look_back': look_back
            }

        except Exception as e:
            self.logger.error(f"Error evaluating price predictor: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def evaluate_anomaly_detector(self, model, test_data, actual_anomalies=None):
        """
        评估异常检测模型

        Args:
            model: 异常检测模型
            test_data: 测试数据
            actual_anomalies: 实际异常标签（可选）

        Returns:
            评估结果
        """
        try:
            # 检测异常
            detection_results = model.predict(test_data)

            # 提取异常检测结果
            predicted_anomalies = [result['is_anomaly'] for result in detection_results]
            errors = [result['error'] for result in detection_results]

            # 计算异常检测指标
            anomaly_count = sum(predicted_anomalies)
            anomaly_ratio = anomaly_count / len(predicted_anomalies)
            avg_error = np.mean(errors)
            std_error = np.std(errors)

            metrics = {
                'anomaly_count': anomaly_count,
                'anomaly_ratio': float(anomaly_ratio),
                'average_error': float(avg_error),
                'std_error': float(std_error),
                'test_size': len(test_data)
            }

            # 如果提供了实际异常标签，计算分类指标
            if actual_anomalies is not None and len(actual_anomalies) == len(predicted_anomalies):
                accuracy = accuracy_score(actual_anomalies, predicted_anomalies)
                precision = precision_score(actual_anomalies, predicted_anomalies, zero_division=0)
                recall = recall_score(actual_anomalies, predicted_anomalies, zero_division=0)
                f1 = f1_score(actual_anomalies, predicted_anomalies, zero_division=0)

                metrics.update({
                    'accuracy': float(accuracy),
                    'precision': float(precision),
                    'recall': float(recall),
                    'f1_score': float(f1)
                })

                # 生成混淆矩阵
                conf_matrix = confusion_matrix(actual_anomalies, predicted_anomalies).tolist()
                metrics['confusion_matrix'] = conf_matrix

            # 分析异常分布
            anomaly_indices = [i for i, is_anomaly in enumerate(predicted_anomalies) if is_anomaly]

            return {
                'timestamp': datetime.now().isoformat(),
                'model_type': 'anomaly_detector',
                'metrics': metrics,
                'anomaly_indices': anomaly_indices,
                'threshold': model.threshold
            }

        except Exception as e:
            self.logger.error(f"Error evaluating anomaly detector: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def evaluate_trend_identifier(self, trend_identifier, test_data):
        """
        评估趋势识别器

        Args:
            trend_identifier: 趋势识别器
            test_data: 测试数据

        Returns:
            评估结果
        """
        try:
            # 提取测试数据
            social_media_data = test_data.get('social_media_data')
            price_data = test_data.get('price_data')
            market_data = test_data.get('market_data')

            # 识别趋势
            trend_results = trend_identifier.identify_trends(
                social_media_data=social_media_data,
                price_data=price_data,
                market_data=market_data
            )

            # 分析趋势识别结果
            trend_analysis = trend_results.get('trend_analysis', {})
            recommendations = trend_results.get('recommendations', [])
            models = trend_results.get('models', {})

            # 计算模型使用情况
            model_usage = {
                'sentiment_analyzer_used': models.get('sentiment_analysis') is not None,
                'price_predictor_used': models.get('price_prediction') is not None,
                'anomaly_detector_used': models.get('anomaly_detection') is not None
            }

            # 分析推荐
            recommendation_types = {}
            for rec in recommendations:
                rec_type = rec.get('type')
                if rec_type not in recommendation_types:
                    recommendation_types[rec_type] = 0
                recommendation_types[rec_type] += 1

            return {
                'timestamp': datetime.now().isoformat(),
                'model_type': 'trend_identifier',
                'trend_analysis': trend_analysis,
                'recommendation_analysis': {
                    'total_recommendations': len(recommendations),
                    'recommendation_types': recommendation_types
                },
                'model_usage': model_usage,
                'test_data_availability': {
                    'social_media_data_available': social_media_data is not None,
                    'price_data_available': price_data is not None,
                    'market_data_available': market_data is not None
                }
            }

        except Exception as e:
            self.logger.error(f"Error evaluating trend identifier: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _create_dataset(self, dataset, look_back=60):
        """
        创建时间序列数据集

        Args:
            dataset: 原始数据集
            look_back: 回溯窗口大小

        Returns:
            X, y: 特征和标签
        """
        X, y = [], []
        for i in range(len(dataset) - look_back):
            a = dataset[i:(i + look_back), 0]
            X.append(a)
            y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(y)

    def _calculate_direction_accuracy(self, actual, predicted):
        """
        计算方向准确率

        Args:
            actual: 实际值
            predicted: 预测值

        Returns:
            方向准确率
        """
        if len(actual) < 2 or len(predicted) < 2:
            return 0

        actual_directions = []
        predicted_directions = []

        for i in range(1, len(actual)):
            actual_dir = 1 if actual[i] > actual[i-1] else 0
            predicted_dir = 1 if predicted[i] > predicted[i-1] else 0
            actual_directions.append(actual_dir)
            predicted_directions.append(predicted_dir)

        if actual_directions:
            return accuracy_score(actual_directions, predicted_directions)
        else:
            return 0

    def compare_models(self, model_evaluations):
        """
        比较多个模型的评估结果

        Args:
            model_evaluations: 模型评估结果列表

        Returns:
            比较结果
        """
        try:
            if not model_evaluations:
                return {
                    'error': 'No model evaluations provided',
                    'timestamp': datetime.now().isoformat()
                }

            # 按模型类型分组
            evaluations_by_type = {}
            for eval_result in model_evaluations:
                model_type = eval_result.get('model_type')
                if model_type not in evaluations_by_type:
                    evaluations_by_type[model_type] = []
                evaluations_by_type[model_type].append(eval_result)

            # 分析每个模型类型的最佳表现
            best_models = {}
            for model_type, evaluations in evaluations_by_type.items():
                if model_type == 'sentiment_analyzer':
                    # 情感分析模型按F1分数排序
                    best = max(evaluations, key=lambda x: x.get('metrics', {}).get('f1_score', 0))
                elif model_type == 'price_predictor':
                    # 价格预测模型按RMSE排序
                    best = min(evaluations, key=lambda x: x.get('metrics', {}).get('rmse', float('inf')))
                elif model_type == 'anomaly_detector':
                    # 异常检测模型按F1分数排序
                    best = max(evaluations, key=lambda x: x.get('metrics', {}).get('f1_score', 0))
                else:
                    best = evaluations[0]

                best_models[model_type] = best

            return {
                'timestamp': datetime.now().isoformat(),
                'model_comparison': {
                    'total_models_evaluated': len(model_evaluations),
                    'models_by_type': evaluations_by_type,
                    'best_models': best_models
                }
            }

        except Exception as e:
            self.logger.error(f"Error comparing models: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def generate_evaluation_report(self, evaluations, report_path=None):
        """
        生成评估报告

        Args:
            evaluations: 评估结果列表
            report_path: 报告保存路径

        Returns:
            报告路径
        """
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'report_type': 'model_evaluation',
                'evaluations': evaluations,
                'summary': {
                    'total_evaluations': len(evaluations),
                    'model_types': list(set([eval.get('model_type') for eval in evaluations]))
                }
            }

            # 保存报告
            if report_path:
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                return {
                    'report_path': report_path,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return report

        except Exception as e:
            self.logger.error(f"Error generating evaluation report: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
