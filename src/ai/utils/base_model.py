# Base Model Class

import os
import json
import logging
from datetime import datetime

class BaseModel:
    """
    基础模型类
    """

    def __init__(self, config=None):
        """
        初始化模型

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.model_path = self.config.get('model_path', './models')
        self.model_name = self.config.get('model_name', 'base_model')

    def train(self, X, y=None):
        """
        训练模型

        Args:
            X: 特征数据
            y: 标签数据

        Returns:
            训练结果
        """
        raise NotImplementedError("Subclass must implement train method")

    def predict(self, X):
        """
        预测

        Args:
            X: 特征数据

        Returns:
            预测结果
        """
        raise NotImplementedError("Subclass must implement predict method")

    def evaluate(self, X, y):
        """
        评估模型

        Args:
            X: 特征数据
            y: 标签数据

        Returns:
            评估指标
        """
        raise NotImplementedError("Subclass must implement evaluate method")

    def save(self, path=None):
        """
        保存模型

        Args:
            path: 保存路径
        """
        if path is None:
            path = os.path.join(self.model_path, self.model_name)

        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self._save_model(path)
            self.logger.info(f"Model saved to {path}")
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")

    def load(self, path=None):
        """
        加载模型

        Args:
            path: 加载路径
        """
        if path is None:
            path = os.path.join(self.model_path, self.model_name)

        try:
            if os.path.exists(path):
                self._load_model(path)
                self.logger.info(f"Model loaded from {path}")
            else:
                self.logger.warning(f"Model path does not exist: {path}")
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")

    def _save_model(self, path):
        """
        保存模型的具体实现

        Args:
            path: 保存路径
        """
        raise NotImplementedError("Subclass must implement _save_model method")

    def _load_model(self, path):
        """
        加载模型的具体实现

        Args:
            path: 加载路径
        """
        raise NotImplementedError("Subclass must implement _load_model method")

    def preprocess(self, data):
        """
        预处理数据

        Args:
            data: 原始数据

        Returns:
            预处理后的数据
        """
        return data

    def postprocess(self, predictions):
        """
        后处理预测结果

        Args:
            predictions: 原始预测结果

        Returns:
            后处理后的结果
        """
        return predictions
