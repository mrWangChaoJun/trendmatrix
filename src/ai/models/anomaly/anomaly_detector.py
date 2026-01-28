# Anomaly Detector Model

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_recall_fscore_support

from ...utils.base_model import BaseModel

class AnomalyDetector(BaseModel):
    """
    时间序列异常检测模型
    """

    def __init__(self, config=None):
        """
        初始化异常检测模型

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.model_name = self.config.get('model_name', 'anomaly_detector')
        self.scaler = None
        self.look_back = self.config.get('look_back', 60)  # 过去60个时间步
        self.lstm_units = self.config.get('lstm_units', 50)
        self.dropout_rate = self.config.get('dropout_rate', 0.2)
        self.epochs = self.config.get('epochs', 100)
        self.batch_size = self.config.get('batch_size', 32)
        self.learning_rate = self.config.get('learning_rate', 0.001)
        self.threshold = self.config.get('threshold', 0.05)  # 异常检测阈值

    def build_model(self):
        """
        构建异常检测模型
        """
        model = Sequential([
            LSTM(self.lstm_units, return_sequences=True, input_shape=(self.look_back, 1)),
            Dropout(self.dropout_rate),
            LSTM(self.lstm_units),
            Dropout(self.dropout_rate),
            Dense(25),
            Dense(1)
        ])

        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

        model.compile(
            optimizer=optimizer,
            loss='mean_squared_error'
        )

        self.model = model
        return model

    def train(self, data):
        """
        训练模型

        Args:
            data: 时间序列数据

        Returns:
            训练结果
        """
        try:
            # 数据预处理
            data = np.array(data).reshape(-1, 1)

            # 数据归一化
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = self.scaler.fit_transform(data)

            # 创建训练数据
            X, y = self._create_dataset(scaled_data)

            # 重塑数据形状 (samples, time steps, features)
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))

            # 分割数据
            train_size = int(len(X) * 0.8)
            X_train, X_test = X[:train_size], X[train_size:]
            y_train, y_test = y[:train_size], y[train_size:]

            # 构建模型
            if self.model is None:
                self.build_model()

            # 训练模型
            history = self.model.fit(
                X_train, y_train,
                epochs=self.epochs,
                batch_size=self.batch_size,
                validation_data=(X_test, y_test),
                verbose=1
            )

            # 评估模型
            evaluation = self.evaluate(X_test, y_test)

            # 保存模型和缩放器
            self.save()

            return {
                'history': history.history,
                'evaluation': evaluation
            }

        except Exception as e:
            self.logger.error(f"Error training anomaly detector: {str(e)}")
            return None

    def predict(self, data):
        """
        检测异常

        Args:
            data: 时间序列数据

        Returns:
            异常检测结果
        """
        try:
            if self.model is None:
                self.load()
                if self.model is None:
                    self.build_model()

            if self.scaler is None:
                self.load_scaler()
                if self.scaler is None:
                    self.logger.error("Scaler not loaded")
                    return []

            # 数据预处理
            data = np.array(data).reshape(-1, 1)
            scaled_data = self.scaler.transform(data)

            # 创建预测数据
            X, y = self._create_dataset(scaled_data)

            # 重塑数据形状
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))

            # 预测
            predictions = self.model.predict(X)

            # 计算重建误差
            mse = np.mean(np.power(y - predictions.flatten(), 2), axis=1)

            # 检测异常
            anomalies = mse > self.threshold

            # 反归一化
            if self.scaler is not None:
                y = self.scaler.inverse_transform(y.reshape(-1, 1))
                predictions = self.scaler.inverse_transform(predictions)

            # 转换检测结果
            results = []
            for i, (actual, pred, error, is_anomaly) in enumerate(zip(y, predictions, mse, anomalies)):
                results.append({
                    'index': i,
                    'actual': float(actual[0]),
                    'predicted': float(pred[0]),
                    'error': float(error),
                    'is_anomaly': bool(is_anomaly),
                    'threshold': self.threshold
                })

            return results

        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {str(e)}")
            return []

    def evaluate(self, X, y):
        """
        评估模型

        Args:
            X: 特征数据
            y: 标签数据

        Returns:
            评估指标
        """
        try:
            if self.model is None:
                self.logger.error("Model not initialized")
                return None

            # 预测
            y_pred = self.model.predict(X)

            # 计算重建误差
            mse = np.mean(np.power(y - y_pred.flatten(), 2), axis=1)

            # 检测异常
            anomalies = mse > self.threshold

            # 假设正常数据占大多数，创建伪标签
            # 在实际应用中，应该使用真实的异常标签
            y_true = np.zeros_like(anomalies)

            # 计算评估指标
            precision, recall, f1, _ = precision_recall_fscore_support(y_true, anomalies, average='binary')

            return {
                'mse': float(np.mean(mse)),
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1)
            }

        except Exception as e:
            self.logger.error(f"Error evaluating model: {str(e)}")
            return None

    def _create_dataset(self, dataset):
        """
        创建数据集

        Args:
            dataset: 原始数据集

        Returns:
            X, y: 特征和标签
        """
        X, y = [], []
        for i in range(len(dataset) - self.look_back):
            a = dataset[i:(i + self.look_back), 0]
            X.append(a)
            y.append(dataset[i + self.look_back, 0])
        return np.array(X), np.array(y)

    def _save_model(self, path):
        """
        保存模型

        Args:
            path: 保存路径
        """
        try:
            # 保存模型
            model_path = os.path.join(path, 'model.h5')
            self.model.save(model_path)

            # 保存缩放器
            import joblib
            scaler_path = os.path.join(path, 'scaler.joblib')
            joblib.dump(self.scaler, scaler_path)

            # 保存配置
            config_path = os.path.join(path, 'config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'look_back': self.look_back,
                    'lstm_units': self.lstm_units,
                    'dropout_rate': self.dropout_rate,
                    'learning_rate': self.learning_rate,
                    'threshold': self.threshold
                }, f)

        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")

    def _load_model(self, path):
        """
        加载模型

        Args:
            path: 加载路径
        """
        try:
            # 加载模型
            model_path = os.path.join(path, 'model.h5')
            self.model = tf.keras.models.load_model(model_path)

            # 加载配置
            config_path = os.path.join(path, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.look_back = config.get('look_back', self.look_back)
                    self.lstm_units = config.get('lstm_units', self.lstm_units)
                    self.dropout_rate = config.get('dropout_rate', self.dropout_rate)
                    self.learning_rate = config.get('learning_rate', self.learning_rate)
                    self.threshold = config.get('threshold', self.threshold)

            # 加载缩放器
            self.load_scaler(path)

        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")

    def load_scaler(self, path=None):
        """
        加载缩放器

        Args:
            path: 加载路径
        """
        if path is None:
            path = os.path.join(self.model_path, self.model_name)

        try:
            import joblib
            scaler_path = os.path.join(path, 'scaler.joblib')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)

        except Exception as e:
            self.logger.error(f"Error loading scaler: {str(e)}")

    def preprocess(self, data):
        """
        预处理数据

        Args:
            data: 原始数据

        Returns:
            预处理后的数据
        """
        # 确保数据是一维数组
        if isinstance(data, list):
            data = np.array(data)

        # 确保数据形状正确
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)

        return data
