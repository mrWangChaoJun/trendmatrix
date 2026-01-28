# Sentiment Analyzer Model

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from ...utils.base_model import BaseModel

class SentimentAnalyzer(BaseModel):
    """
    社交媒体情绪分析模型
    """

    def __init__(self, config=None):
        """
        初始化情绪分析模型

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.model_name = self.config.get('model_name', 'sentiment_analyzer')
        self.tokenizer = None
        self.max_sequence_length = self.config.get('max_sequence_length', 100)
        self.vocab_size = self.config.get('vocab_size', 10000)
        self.embedding_dim = self.config.get('embedding_dim', 128)
        self.lstm_units = self.config.get('lstm_units', 64)
        self.dropout_rate = self.config.get('dropout_rate', 0.2)
        self.epochs = self.config.get('epochs', 10)
        self.batch_size = self.config.get('batch_size', 32)

    def build_model(self):
        """
        构建情绪分析模型
        """
        model = Sequential([
            Embedding(self.vocab_size, self.embedding_dim, input_length=self.max_sequence_length),
            Dropout(self.dropout_rate),
            LSTM(self.lstm_units, return_sequences=True),
            Dropout(self.dropout_rate),
            LSTM(self.lstm_units),
            Dropout(self.dropout_rate),
            Dense(64, activation='relu'),
            Dense(3, activation='softmax')  # 3 classes: positive, neutral, negative
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        self.model = model
        return model

    def train(self, texts, labels):
        """
        训练模型

        Args:
            texts: 文本数据
            labels: 标签数据（0: negative, 1: neutral, 2: positive）

        Returns:
            训练结果
        """
        try:
            # 初始化分词器
            self.tokenizer = Tokenizer(num_words=self.vocab_size, oov_token='<OOV>')
            self.tokenizer.fit_on_texts(texts)

            # 文本向量化
            sequences = self.tokenizer.texts_to_sequences(texts)
            padded_sequences = pad_sequences(sequences, maxlen=self.max_sequence_length, padding='post', truncating='post')

            # 转换标签
            labels = np.array(labels)

            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

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

            # 保存模型和分词器
            self.save()

            return {
                'history': history.history,
                'evaluation': evaluation
            }

        except Exception as e:
            self.logger.error(f"Error training sentiment analyzer: {str(e)}")
            return None

    def predict(self, texts):
        """
        预测情绪

        Args:
            texts: 文本数据

        Returns:
            预测结果
        """
        try:
            if self.model is None:
                self.load()
                if self.model is None:
                    self.build_model()

            if self.tokenizer is None:
                self.load_tokenizer()
                if self.tokenizer is None:
                    self.logger.error("Tokenizer not loaded")
                    return []

            # 文本向量化
            sequences = self.tokenizer.texts_to_sequences(texts)
            padded_sequences = pad_sequences(sequences, maxlen=self.max_sequence_length, padding='post', truncating='post')

            # 预测
            predictions = self.model.predict(padded_sequences)

            # 转换预测结果
            predicted_classes = np.argmax(predictions, axis=1)
            sentiment_labels = ['negative', 'neutral', 'positive']
            results = []

            for text, pred_class, pred_prob in zip(texts, predicted_classes, predictions):
                results.append({
                    'text': text,
                    'sentiment': sentiment_labels[pred_class],
                    'confidence': float(np.max(pred_prob)),
                    'probabilities': {
                        'negative': float(pred_prob[0]),
                        'neutral': float(pred_prob[1]),
                        'positive': float(pred_prob[2])
                    }
                })

            return results

        except Exception as e:
            self.logger.error(f"Error predicting sentiment: {str(e)}")
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

            loss, accuracy = self.model.evaluate(X, y, verbose=0)

            # 生成分类报告
            y_pred = np.argmax(self.model.predict(X), axis=1)
            report = classification_report(y, y_pred, output_dict=True)

            return {
                'loss': float(loss),
                'accuracy': float(accuracy),
                'classification_report': report
            }

        except Exception as e:
            self.logger.error(f"Error evaluating model: {str(e)}")
            return None

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

            # 保存分词器
            tokenizer_path = os.path.join(path, 'tokenizer.json')
            with open(tokenizer_path, 'w', encoding='utf-8') as f:
                json.dump(self.tokenizer.to_json(), f, ensure_ascii=False)

            # 保存配置
            config_path = os.path.join(path, 'config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'max_sequence_length': self.max_sequence_length,
                    'vocab_size': self.vocab_size,
                    'embedding_dim': self.embedding_dim,
                    'lstm_units': self.lstm_units,
                    'dropout_rate': self.dropout_rate
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
                    self.max_sequence_length = config.get('max_sequence_length', self.max_sequence_length)
                    self.vocab_size = config.get('vocab_size', self.vocab_size)
                    self.embedding_dim = config.get('embedding_dim', self.embedding_dim)
                    self.lstm_units = config.get('lstm_units', self.lstm_units)
                    self.dropout_rate = config.get('dropout_rate', self.dropout_rate)

            # 加载分词器
            self.load_tokenizer(path)

        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")

    def load_tokenizer(self, path=None):
        """
        加载分词器

        Args:
            path: 加载路径
        """
        if path is None:
            path = os.path.join(self.model_path, self.model_name)

        try:
            tokenizer_path = os.path.join(path, 'tokenizer.json')
            if os.path.exists(tokenizer_path):
                with open(tokenizer_path, 'r', encoding='utf-8') as f:
                    self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(f.read())

        except Exception as e:
            self.logger.error(f"Error loading tokenizer: {str(e)}")

    def preprocess(self, text):
        """
        预处理文本

        Args:
            text: 原始文本

        Returns:
            预处理后的文本
        """
        # 简单的文本预处理
        text = text.lower()
        # 移除特殊字符
        import re
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # 移除多余的空格
        text = ' '.join(text.split())
        return text
