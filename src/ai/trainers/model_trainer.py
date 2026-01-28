# Model Trainer Module

import logging
import numpy as np
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

class ModelTrainer:
    """
    模型训练器
    用于训练各个AI模型
    """

    def __init__(self, config=None):
        """
        初始化模型训练器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 训练参数
        self.epochs = self.config.get('epochs', 100)
        self.batch_size = self.config.get('batch_size', 32)
        self.learning_rate = self.config.get('learning_rate', 0.001)
        self.validation_split = self.config.get('validation_split', 0.2)
        self.early_stopping_patience = self.config.get('early_stopping_patience', 10)

        # 模型保存路径
        self.model_save_path = self.config.get('model_save_path', './models')
        os.makedirs(self.model_save_path, exist_ok=True)

    def train_sentiment_analyzer(self, model, texts, labels, hyperparameter_tuning=False):
        """
        训练情感分析模型

        Args:
            model: 情感分析模型
            texts: 文本数据
            labels: 标签数据
            hyperparameter_tuning: 是否进行超参数调优

        Returns:
            训练结果
        """
        try:
            # 数据预处理
            if hyperparameter_tuning:
                # 超参数调优
                best_params = self._tune_sentiment_analyzer_hyperparameters(model, texts, labels)
                # 更新模型参数
                for param, value in best_params.items():
                    if hasattr(model, param):
                        setattr(model, param, value)

            # 训练模型
            training_result = model.train(texts, labels)

            # 保存训练结果
            if training_result:
                result_path = os.path.join(self.model_save_path, f"sentiment_analyzer_training_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(result_path, 'w', encoding='utf-8') as f:
                    json.dump(training_result, f, ensure_ascii=False, indent=2)

                return {
                    'timestamp': datetime.now().isoformat(),
                    'model_type': 'sentiment_analyzer',
                    'training_result': training_result,
                    'result_path': result_path
                }
            else:
                return {
                    'error': 'Training failed',
                    'timestamp': datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f"Error training sentiment analyzer: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def train_price_predictor(self, model, prices, hyperparameter_tuning=False):
        """
        训练价格预测模型

        Args:
            model: 价格预测模型
            prices: 价格数据
            hyperparameter_tuning: 是否进行超参数调优

        Returns:
            训练结果
        """
        try:
            # 数据预处理
            prices = np.array(prices).reshape(-1, 1)

            # 超参数调优
            if hyperparameter_tuning:
                best_params = self._tune_price_predictor_hyperparameters(model, prices)
                # 更新模型参数
                for param, value in best_params.items():
                    if hasattr(model, param):
                        setattr(model, param, value)

            # 训练模型
            training_result = model.train(prices)

            # 保存训练结果
            if training_result:
                result_path = os.path.join(self.model_save_path, f"price_predictor_training_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(result_path, 'w', encoding='utf-8') as f:
                    json.dump(training_result, f, ensure_ascii=False, indent=2)

                return {
                    'timestamp': datetime.now().isoformat(),
                    'model_type': 'price_predictor',
                    'training_result': training_result,
                    'result_path': result_path
                }
            else:
                return {
                    'error': 'Training failed',
                    'timestamp': datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f"Error training price predictor: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def train_anomaly_detector(self, model, data, hyperparameter_tuning=False):
        """
        训练异常检测模型

        Args:
            model: 异常检测模型
            data: 时间序列数据
            hyperparameter_tuning: 是否进行超参数调优

        Returns:
            训练结果
        """
        try:
            # 数据预处理
            data = np.array(data).reshape(-1, 1)

            # 超参数调优
            if hyperparameter_tuning:
                best_params = self._tune_anomaly_detector_hyperparameters(model, data)
                # 更新模型参数
                for param, value in best_params.items():
                    if hasattr(model, param):
                        setattr(model, param, value)

            # 训练模型
            training_result = model.train(data)

            # 保存训练结果
            if training_result:
                result_path = os.path.join(self.model_save_path, f"anomaly_detector_training_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(result_path, 'w', encoding='utf-8') as f:
                    json.dump(training_result, f, ensure_ascii=False, indent=2)

                return {
                    'timestamp': datetime.now().isoformat(),
                    'model_type': 'anomaly_detector',
                    'training_result': training_result,
                    'result_path': result_path
                }
            else:
                return {
                    'error': 'Training failed',
                    'timestamp': datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f"Error training anomaly detector: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _tune_sentiment_analyzer_hyperparameters(self, model, texts, labels):
        """
        调优情感分析模型超参数

        Args:
            model: 情感分析模型
            texts: 文本数据
            labels: 标签数据

        Returns:
            最佳超参数
        """
        try:
            # 定义超参数搜索空间
            param_grid = {
                'max_sequence_length': [50, 100, 150],
                'vocab_size': [5000, 10000, 20000],
                'embedding_dim': [64, 128, 256],
                'lstm_units': [32, 64, 128],
                'dropout_rate': [0.2, 0.3, 0.4],
                'epochs': [5, 10, 15],
                'batch_size': [16, 32, 64]
            }

            # 简化的超参数调优（实际应用中应该使用更复杂的方法）
            best_params = {}
            best_score = 0

            # 随机搜索几个组合
            for _ in range(5):  # 限制搜索次数
                # 随机选择超参数
                params = {}
                for param, values in param_grid.items():
                    params[param] = np.random.choice(values)

                # 更新模型参数
                for param, value in params.items():
                    if hasattr(model, param):
                        setattr(model, param, value)

                # 训练模型
                result = model.train(texts[:1000], labels[:1000])  # 使用部分数据进行快速评估

                # 评估模型
                if result and 'evaluation' in result:
                    accuracy = result['evaluation'].get('accuracy', 0)
                    if accuracy > best_score:
                        best_score = accuracy
                        best_params = params

            return best_params if best_params else {
                'max_sequence_length': 100,
                'vocab_size': 10000,
                'embedding_dim': 128,
                'lstm_units': 64,
                'dropout_rate': 0.2,
                'epochs': 10,
                'batch_size': 32
            }

        except Exception as e:
            self.logger.error(f"Error tuning sentiment analyzer hyperparameters: {str(e)}")
            return {
                'max_sequence_length': 100,
                'vocab_size': 10000,
                'embedding_dim': 128,
                'lstm_units': 64,
                'dropout_rate': 0.2,
                'epochs': 10,
                'batch_size': 32
            }

    def _tune_price_predictor_hyperparameters(self, model, prices):
        """
        调优价格预测模型超参数

        Args:
            model: 价格预测模型
            prices: 价格数据

        Returns:
            最佳超参数
        """
        try:
            # 定义超参数搜索空间
            param_grid = {
                'look_back': [30, 60, 90],
                'lstm_units': [32, 50, 100],
                'dropout_rate': [0.2, 0.3, 0.4],
                'epochs': [50, 100, 150],
                'batch_size': [16, 32, 64],
                'learning_rate': [0.0001, 0.001, 0.01]
            }

            # 简化的超参数调优
            best_params = {}
            best_score = float('inf')  # 对于RMSE，越小越好

            # 随机搜索几个组合
            for _ in range(5):  # 限制搜索次数
                # 随机选择超参数
                params = {}
                for param, values in param_grid.items():
                    params[param] = np.random.choice(values)

                # 更新模型参数
                for param, value in params.items():
                    if hasattr(model, param):
                        setattr(model, param, value)

                # 训练模型
                result = model.train(prices[:1000])  # 使用部分数据进行快速评估

                # 评估模型
                if result and 'evaluation' in result:
                    mse = result['evaluation'].get('mse', float('inf'))
                    if mse < best_score:
                        best_score = mse
                        best_params = params

            return best_params if best_params else {
                'look_back': 60,
                'lstm_units': 50,
                'dropout_rate': 0.2,
                'epochs': 100,
                'batch_size': 32,
                'learning_rate': 0.001
            }

        except Exception as e:
            self.logger.error(f"Error tuning price predictor hyperparameters: {str(e)}")
            return {
                'look_back': 60,
                'lstm_units': 50,
                'dropout_rate': 0.2,
                'epochs': 100,
                'batch_size': 32,
                'learning_rate': 0.001
            }

    def _tune_anomaly_detector_hyperparameters(self, model, data):
        """
        调优异常检测模型超参数

        Args:
            model: 异常检测模型
            data: 时间序列数据

        Returns:
            最佳超参数
        """
        try:
            # 定义超参数搜索空间
            param_grid = {
                'look_back': [30, 60, 90],
                'lstm_units': [32, 50, 100],
                'dropout_rate': [0.2, 0.3, 0.4],
                'epochs': [50, 100, 150],
                'batch_size': [16, 32, 64],
                'learning_rate': [0.0001, 0.001, 0.01],
                'threshold': [0.03, 0.05, 0.07]
            }

            # 简化的超参数调优
            best_params = {}
            best_score = float('inf')  # 对于MSE，越小越好

            # 随机搜索几个组合
            for _ in range(5):  # 限制搜索次数
                # 随机选择超参数
                params = {}
                for param, values in param_grid.items():
                    params[param] = np.random.choice(values)

                # 更新模型参数
                for param, value in params.items():
                    if hasattr(model, param):
                        setattr(model, param, value)

                # 训练模型
                result = model.train(data[:1000])  # 使用部分数据进行快速评估

                # 评估模型
                if result and 'evaluation' in result:
                    mse = result['evaluation'].get('mse', float('inf'))
                    if mse < best_score:
                        best_score = mse
                        best_params = params

            return best_params if best_params else {
                'look_back': 60,
                'lstm_units': 50,
                'dropout_rate': 0.2,
                'epochs': 100,
                'batch_size': 32,
                'learning_rate': 0.001,
                'threshold': 0.05
            }

        except Exception as e:
            self.logger.error(f"Error tuning anomaly detector hyperparameters: {str(e)}")
            return {
                'look_back': 60,
                'lstm_units': 50,
                'dropout_rate': 0.2,
                'epochs': 100,
                'batch_size': 32,
                'learning_rate': 0.001,
                'threshold': 0.05
            }

    def create_training_callbacks(self, model_name):
        """
        创建训练回调

        Args:
            model_name: 模型名称

        Returns:
            回调列表
        """
        callbacks = []

        # 早停回调
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=self.early_stopping_patience,
            restore_best_weights=True
        )
        callbacks.append(early_stopping)

        # 模型检查点回调
        checkpoint_path = os.path.join(self.model_save_path, f"{model_name}_best_model.h5")
        model_checkpoint = ModelCheckpoint(
            checkpoint_path,
            monitor='val_loss',
            save_best_only=True,
            mode='min'
        )
        callbacks.append(model_checkpoint)

        # TensorBoard回调
        log_dir = os.path.join(self.model_save_path, 'logs', f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        tensorboard = TensorBoard(log_dir=log_dir, histogram_freq=1)
        callbacks.append(tensorboard)

        return callbacks

    def preprocess_text_data(self, texts):
        """
        预处理文本数据

        Args:
            texts: 文本数据

        Returns:
            预处理后的文本数据
        """
        try:
            import re

            processed_texts = []
            for text in texts:
                # 转换为小写
                text = text.lower()
                # 移除特殊字符
                text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
                # 移除多余的空格
                text = ' '.join(text.split())
                processed_texts.append(text)

            return processed_texts

        except Exception as e:
            self.logger.error(f"Error preprocessing text data: {str(e)}")
            return texts

    def preprocess_time_series_data(self, data):
        """
        预处理时间序列数据

        Args:
            data: 时间序列数据

        Returns:
            预处理后的数据和缩放器
        """
        try:
            # 转换为 numpy 数组
            data = np.array(data).reshape(-1, 1)

            # 数据归一化
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(data)

            return scaled_data, scaler

        except Exception as e:
            self.logger.error(f"Error preprocessing time series data: {str(e)}")
            return data, None

    def generate_training_report(self, training_results, report_path=None):
        """
        生成训练报告

        Args:
            training_results: 训练结果列表
            report_path: 报告保存路径

        Returns:
            报告路径
        """
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'report_type': 'training',
                'training_results': training_results,
                'summary': {
                    'total_models_trained': len(training_results),
                    'model_types': list(set([result.get('model_type') for result in training_results]))
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
            self.logger.error(f"Error generating training report: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
