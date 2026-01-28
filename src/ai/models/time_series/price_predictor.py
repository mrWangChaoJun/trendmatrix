# Price Predictor Model

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Bidirectional
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ...utils.base_model import BaseModel

class PricePredictor(BaseModel):
    """
    价格预测模型
    """

    def __init__(self, config=None):
        """
        初始化价格预测模型

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.model_name = self.config.get('model_name', 'price_predictor')
        self.scaler = None
        self.look_back = self.config.get('look_back', 60)  # 过去60个时间步
        self.lstm_units = self.config.get('lstm_units', 50)
        self.dropout_rate = self.config.get('dropout_rate', 0.2)
        self.epochs = self.config.get('epochs', 100)
        self.batch_size = self.config.get('batch_size', 32)
        self.learning_rate = self.config.get('learning_rate', 0.001)

    def build_model(self):
        """
        构建价格预测模型
        """
        model = Sequential([
            Bidirectional(LSTM(self.lstm_units, return_sequences=True), input_shape=(self.look_back, 1)),
            Dropout(self.dropout_rate),
            Bidirectional(LSTM(self.lstm_units)),
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

    def train(self, prices):
        """
        训练模型

        Args:
            prices: 价格数据

        Returns:
            训练结果
        """
        try:
            # 数据预处理
            prices = np.array(prices).reshape(-1, 1)

            # 数据归一化
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_prices = self.scaler.fit_transform(prices)

            # 创建训练数据
            X, y = self._create_dataset(scaled_prices)

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
            self.logger.error(f"Error training price predictor: {str(e)}")
            return None

    def predict(self, prices, days=1):
        """
        预测价格

        Args:
            prices: 历史价格数据
            days: 预测天数

        Returns:
            预测结果
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
            prices = np.array(prices).reshape(-1, 1)
            scaled_prices = self.scaler.transform(prices)

            # 获取最近的 look_back 个数据点
            last_sequence = scaled_prices[-self.look_back:]
            last_sequence = np.reshape(last_sequence, (1, self.look_back, 1))

            # 预测
            predictions = []
            current_sequence = last_sequence

            for _ in range(days):
                # 预测下一个值
                next_value = self.model.predict(current_sequence, verbose=0)
                predictions.append(next_value[0][0])

                # 更新序列
                current_sequence = np.append(current_sequence[:, 1:, :], [[next_value]], axis=1)

            # 反归一化
            predictions = np.array(predictions).reshape(-1, 1)
            predictions = self.scaler.inverse_transform(predictions)

            # 转换预测结果
            results = []
            for i, pred in enumerate(predictions):
                results.append({
                    'day': i + 1,
                    'price': float(pred[0])
                })

            return results

        except Exception as e:
            self.logger.error(f"Error predicting price: {str(e)}")
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

            # 反归一化
            if self.scaler is not None:
                y = self.scaler.inverse_transform(y.reshape(-1, 1))
                y_pred = self.scaler.inverse_transform(y_pred)

            # 计算评估指标
            mse = mean_squared_error(y, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y, y_pred)
            r2 = r2_score(y, y_pred)

            return {
                'mse': float(mse),
                'rmse': float(rmse),
                'mae': float(mae),
                'r2': float(r2)
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
                    'learning_rate': self.learning_rate
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
