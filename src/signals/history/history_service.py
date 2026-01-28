# History Service

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

class HistoryService:
    """
    历史服务
    管理信号历史记录和准确率追踪
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化历史服务

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 历史记录存储
        self.signal_history = []
        self.accuracy_tracking = {}

        # 配置参数
        self.max_history_size = self.config.get('max_history_size', 10000)
        self.accuracy_calculation_days = self.config.get('accuracy_calculation_days', 30)

    def add_signal_to_history(self, signal: Dict[str, Any]) -> bool:
        """
        添加信号到历史记录

        Args:
            signal: 信号对象

        Returns:
            是否成功
        """
        try:
            # 验证信号
            if not self._validate_signal(signal):
                self.logger.error("Invalid signal for history")
                return False

            # 添加到历史记录
            signal_with_history = signal.copy()
            signal_with_history['history_id'] = f"hist_{len(self.signal_history)}_{signal['signal_id']}"
            signal_with_history['added_to_history_at'] = datetime.now().isoformat()
            signal_with_history['status'] = 'active'
            signal_with_history['outcome'] = None  # 初始结果为 None
            signal_with_history['accuracy'] = None  # 初始准确率为 None

            # 添加到历史记录
            self.signal_history.append(signal_with_history)

            # 限制历史记录大小
            if len(self.signal_history) > self.max_history_size:
                self.signal_history = self.signal_history[-self.max_history_size:]

            # 初始化准确率追踪
            self._init_accuracy_tracking(signal['signal_id'])

            self.logger.info(f"Added signal {signal['signal_id']} to history")
            return True

        except Exception as e:
            self.logger.error(f"Error adding signal to history: {str(e)}")
            return False

    def update_signal_outcome(self, signal_id: str, outcome: Dict[str, Any]) -> bool:
        """
        更新信号结果

        Args:
            signal_id: 信号 ID
            outcome: 结果信息

        Returns:
            是否成功
        """
        try:
            # 查找信号
            signal = self._find_signal_by_id(signal_id)
            if not signal:
                self.logger.error(f"Signal not found: {signal_id}")
                return False

            # 更新结果
            signal['outcome'] = outcome
            signal['outcome_updated_at'] = datetime.now().isoformat()
            signal['status'] = 'completed'

            # 计算准确率
            accuracy = self._calculate_signal_accuracy(signal, outcome)
            signal['accuracy'] = accuracy

            # 更新准确率追踪
            self._update_accuracy_tracking(signal_id, accuracy, outcome)

            self.logger.info(f"Updated outcome for signal {signal_id} with accuracy {accuracy}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating signal outcome: {str(e)}")
            return False

    def get_signal_history(self, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        获取信号历史

        Args:
            filters: 过滤条件
            limit: 限制数量

        Returns:
            信号历史列表
        """
        try:
            filtered_history = self.signal_history

            # 应用过滤条件
            if filters:
                for key, value in filters.items():
                    if key == 'asset':
                        filtered_history = [s for s in filtered_history if s.get('asset') == value]
                    elif key == 'type':
                        filtered_history = [s for s in filtered_history if s.get('type') == value]
                    elif key == 'status':
                        filtered_history = [s for s in filtered_history if s.get('status') == value]
                    elif key == 'level':
                        filtered_history = [s for s in filtered_history if s.get('level') == value]
                    elif key == 'time_range':
                        start_time, end_time = value
                        filtered_history = [
                            s for s in filtered_history
                            if start_time <= s.get('timestamp', '') <= end_time
                        ]

            # 按时间排序
            filtered_history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

            # 限制数量
            return filtered_history[:limit]

        except Exception as e:
            self.logger.error(f"Error getting signal history: {str(e)}")
            return []

    def get_signal_statistics(self, time_range: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        获取信号统计信息

        Args:
            time_range: 时间范围

        Returns:
            统计信息
        """
        try:
            # 过滤时间范围
            if time_range:
                start_time, end_time = time_range
                filtered_history = [
                    s for s in self.signal_history
                    if start_time <= s.get('timestamp', '') <= end_time
                ]
            else:
                filtered_history = self.signal_history

            # 基本统计
            total_signals = len(filtered_history)
            completed_signals = [s for s in filtered_history if s.get('status') == 'completed']
            active_signals = [s for s in filtered_history if s.get('status') == 'active']

            # 信号类型分布
            type_distribution = {}
            for signal in filtered_history:
                signal_type = signal.get('type', 'unknown')
                type_distribution[signal_type] = type_distribution.get(signal_type, 0) + 1

            # 资产分布
            asset_distribution = {}
            for signal in filtered_history:
                asset = signal.get('asset', 'unknown')
                asset_distribution[asset] = asset_distribution.get(asset, 0) + 1

            # 级别分布
            level_distribution = {}
            for signal in filtered_history:
                level = signal.get('level', 'unknown')
                level_distribution[level] = level_distribution.get(level, 0) + 1

            # 准确率统计
            accuracy_stats = self._calculate_accuracy_statistics(completed_signals)

            # 综合统计
            statistics = {
                'total_signals': total_signals,
                'completed_signals': len(completed_signals),
                'active_signals': len(active_signals),
                'type_distribution': type_distribution,
                'asset_distribution': asset_distribution,
                'level_distribution': level_distribution,
                'accuracy': accuracy_stats,
                'time_range': time_range,
                'calculated_at': datetime.now().isoformat()
            }

            return statistics

        except Exception as e:
            self.logger.error(f"Error getting signal statistics: {str(e)}")
            return {}

    def get_accuracy_tracking(self, asset: Optional[str] = None, signal_type: Optional[str] = None) -> Dict[str, Any]:
        """
        获取准确率追踪信息

        Args:
            asset: 资产
            signal_type: 信号类型

        Returns:
            准确率追踪信息
        """
        try:
            # 过滤准确率追踪
            filtered_tracking = {}
            for signal_id, tracking in self.accuracy_tracking.items():
                # 查找对应的信号
                signal = self._find_signal_by_id(signal_id)
                if not signal:
                    continue

                # 应用过滤条件
                if asset and signal.get('asset') != asset:
                    continue
                if signal_type and signal.get('type') != signal_type:
                    continue

                filtered_tracking[signal_id] = tracking

            # 计算总体准确率
            overall_accuracy = self._calculate_overall_accuracy(filtered_tracking)

            return {
                'signal_tracking': filtered_tracking,
                'overall_accuracy': overall_accuracy,
                'calculated_at': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting accuracy tracking: {str(e)}")
            return {}

    def _find_signal_by_id(self, signal_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 查找信号

        Args:
            signal_id: 信号 ID

        Returns:
            信号对象
        """
        for signal in self.signal_history:
            if signal.get('signal_id') == signal_id:
                return signal
        return None

    def _init_accuracy_tracking(self, signal_id: str):
        """
        初始化准确率追踪

        Args:
            signal_id: 信号 ID
        """
        if signal_id not in self.accuracy_tracking:
            self.accuracy_tracking[signal_id] = {
                'signal_id': signal_id,
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy': 0.0,
                'last_updated': datetime.now().isoformat(),
                'predictions': []
            }

    def _update_accuracy_tracking(self, signal_id: str, accuracy: float, outcome: Dict[str, Any]):
        """
        更新准确率追踪

        Args:
            signal_id: 信号 ID
            accuracy: 准确率
            outcome: 结果信息
        """
        if signal_id in self.accuracy_tracking:
            tracking = self.accuracy_tracking[signal_id]
            tracking['total_predictions'] += 1
            if accuracy >= 0.5:  # 假设准确率 >= 0.5 为正确预测
                tracking['correct_predictions'] += 1

            # 更新准确率
            if tracking['total_predictions'] > 0:
                tracking['accuracy'] = tracking['correct_predictions'] / tracking['total_predictions']

            tracking['last_updated'] = datetime.now().isoformat()
            tracking['predictions'].append({
                'accuracy': accuracy,
                'outcome': outcome,
                'timestamp': datetime.now().isoformat()
            })

    def _calculate_signal_accuracy(self, signal: Dict[str, Any], outcome: Dict[str, Any]) -> float:
        """
        计算信号准确率

        Args:
            signal: 信号对象
            outcome: 结果信息

        Returns:
            准确率 (0-1)
        """
        try:
            signal_type = signal['type']
            actual_outcome = outcome.get('actual_outcome', 'neutral')
            expected_direction = None

            # 确定预期方向
            if signal_type == 'buy':
                expected_direction = 'up'
            elif signal_type == 'sell':
                expected_direction = 'down'
            elif signal_type == 'hold':
                expected_direction = 'neutral'

            # 计算准确率
            if expected_direction == actual_outcome:
                return 1.0
            elif (expected_direction == 'up' and actual_outcome == 'down') or \
                 (expected_direction == 'down' and actual_outcome == 'up'):
                return 0.0
            else:
                return 0.5

        except Exception as e:
            self.logger.error(f"Error calculating signal accuracy: {str(e)}")
            return 0.0

    def _calculate_accuracy_statistics(self, completed_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算准确率统计

        Args:
            completed_signals: 已完成的信号列表

        Returns:
            准确率统计
        """
        if not completed_signals:
            return {
                'average_accuracy': 0.0,
                'total_completed': 0,
                'correct_predictions': 0,
                'accuracy_by_type': {},
                'accuracy_by_asset': {},
                'accuracy_by_level': {}
            }

        # 计算总体准确率
        accuracies = [s.get('accuracy', 0.0) for s in completed_signals]
        average_accuracy = sum(accuracies) / len(accuracies)
        correct_predictions = sum(1 for acc in accuracies if acc >= 0.5)

        # 按类型计算准确率
        accuracy_by_type = {}
        type_counts = {}
        for signal in completed_signals:
            signal_type = signal.get('type', 'unknown')
            accuracy = signal.get('accuracy', 0.0)

            if signal_type not in accuracy_by_type:
                accuracy_by_type[signal_type] = 0.0
                type_counts[signal_type] = 0

            accuracy_by_type[signal_type] += accuracy
            type_counts[signal_type] += 1

        for signal_type in accuracy_by_type:
            if type_counts[signal_type] > 0:
                accuracy_by_type[signal_type] /= type_counts[signal_type]

        # 按资产计算准确率
        accuracy_by_asset = {}
        asset_counts = {}
        for signal in completed_signals:
            asset = signal.get('asset', 'unknown')
            accuracy = signal.get('accuracy', 0.0)

            if asset not in accuracy_by_asset:
                accuracy_by_asset[asset] = 0.0
                asset_counts[asset] = 0

            accuracy_by_asset[asset] += accuracy
            asset_counts[asset] += 1

        for asset in accuracy_by_asset:
            if asset_counts[asset] > 0:
                accuracy_by_asset[asset] /= asset_counts[asset]

        # 按级别计算准确率
        accuracy_by_level = {}
        level_counts = {}
        for signal in completed_signals:
            level = signal.get('level', 'unknown')
            accuracy = signal.get('accuracy', 0.0)

            if level not in accuracy_by_level:
                accuracy_by_level[level] = 0.0
                level_counts[level] = 0

            accuracy_by_level[level] += accuracy
            level_counts[level] += 1

        for level in accuracy_by_level:
            if level_counts[level] > 0:
                accuracy_by_level[level] /= level_counts[level]

        return {
            'average_accuracy': average_accuracy,
            'total_completed': len(completed_signals),
            'correct_predictions': correct_predictions,
            'accuracy_by_type': accuracy_by_type,
            'accuracy_by_asset': accuracy_by_asset,
            'accuracy_by_level': accuracy_by_level
        }

    def _calculate_overall_accuracy(self, filtered_tracking: Dict[str, Any]) -> float:
        """
        计算总体准确率

        Args:
            filtered_tracking: 过滤后的准确率追踪

        Returns:
            总体准确率
        """
        if not filtered_tracking:
            return 0.0

        total_predictions = 0
        correct_predictions = 0

        for tracking in filtered_tracking.values():
            total_predictions += tracking.get('total_predictions', 0)
            correct_predictions += tracking.get('correct_predictions', 0)

        if total_predictions > 0:
            return correct_predictions / total_predictions
        else:
            return 0.0

    def _validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        验证信号

        Args:
            signal: 信号对象

        Returns:
            是否有效
        """
        try:
            required_fields = ['signal_id', 'asset', 'type', 'strength', 'confidence', 'timestamp']
            for field in required_fields:
                if field not in signal:
                    return False

            if not 1 <= signal['strength'] <= 10:
                return False

            if not 0 <= signal['confidence'] <= 1:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating signal: {str(e)}")
            return False

    def clear_history(self, older_than_days: Optional[int] = None) -> bool:
        """
        清除历史记录

        Args:
            older_than_days: 清除超过指定天数的记录

        Returns:
            是否成功
        """
        try:
            if older_than_days:
                # 计算时间阈值
                import datetime as dt
                threshold = (dt.datetime.now() - dt.timedelta(days=older_than_days)).isoformat()

                # 过滤历史记录
                self.signal_history = [
                    s for s in self.signal_history
                    if s.get('timestamp', '') >= threshold
                ]
            else:
                # 清空历史记录
                self.signal_history = []
                self.accuracy_tracking = {}

            self.logger.info("Cleared history")
            return True

        except Exception as e:
            self.logger.error(f"Error clearing history: {str(e)}")
            return False

    def export_history(self, format: str = 'json') -> Any:
        """
        导出历史记录

        Args:
            format: 导出格式

        Returns:
            导出数据
        """
        try:
            if format == 'json':
                import json
                return json.dumps(self.signal_history, indent=2)
            elif format == 'csv':
                import csv
                import io
                output = io.StringIO()
                if not self.signal_history:
                    return output.getvalue()

                # 提取字段名
                fieldnames = list(self.signal_history[0].keys())
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                for signal in self.signal_history:
                    writer.writerow(signal)
                return output.getvalue()
            else:
                self.logger.error(f"Unsupported export format: {format}")
                return None

        except Exception as e:
            self.logger.error(f"Error exporting history: {str(e)}")
            return None
