# Rule Engine

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable

class RuleEngine:
    """
    规则引擎
    管理和执行信号生成规则
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化规则引擎

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 规则存储
        self.rules = {}

        # 规则类型处理器
        self.rule_handlers = {
            'threshold': self._handle_threshold_rule,
            'trend': self._handle_trend_rule,
            'composite': self._handle_composite_rule,
            'anomaly': self._handle_anomaly_rule,
            'pattern': self._handle_pattern_rule
        }

    def add_rule(self, rule: Dict[str, Any]) -> str:
        """
        添加规则

        Args:
            rule: 规则对象

        Returns:
            规则 ID
        """
        try:
            # 验证规则
            if not self._validate_rule(rule):
                raise ValueError("Invalid rule")

            # 生成规则 ID
            rule_id = rule.get('rule_id', f"rule_{uuid.uuid4().hex[:8]}")
            rule['rule_id'] = rule_id

            # 设置规则元数据
            rule['created_at'] = datetime.now().isoformat()
            rule['updated_at'] = datetime.now().isoformat()
            rule['status'] = rule.get('status', 'enabled')

            # 添加规则
            self.rules[rule_id] = rule
            self.logger.info(f"Added rule: {rule_id} - {rule.get('name')}")

            return rule_id

        except Exception as e:
            self.logger.error(f"Error adding rule: {str(e)}")
            return None

    def remove_rule(self, rule_id: str) -> bool:
        """
        移除规则

        Args:
            rule_id: 规则 ID

        Returns:
            是否成功
        """
        try:
            if rule_id in self.rules:
                del self.rules[rule_id]
                self.logger.info(f"Removed rule: {rule_id}")
                return True
            else:
                self.logger.warning(f"Rule not found: {rule_id}")
                return False

        except Exception as e:
            self.logger.error(f"Error removing rule: {str(e)}")
            return False

    def update_rule(self, rule_id: str, updates: Dict[str, Any]) -> bool:
        """
        更新规则

        Args:
            rule_id: 规则 ID
            updates: 更新内容

        Returns:
            是否成功
        """
        try:
            if rule_id not in self.rules:
                self.logger.warning(f"Rule not found: {rule_id}")
                return False

            # 获取原始规则
            rule = self.rules[rule_id].copy()

            # 应用更新
            for key, value in updates.items():
                rule[key] = value

            # 验证更新后的规则
            if not self._validate_rule(rule):
                raise ValueError("Invalid rule after updates")

            # 更新规则
            rule['updated_at'] = datetime.now().isoformat()
            self.rules[rule_id] = rule
            self.logger.info(f"Updated rule: {rule_id}")

            return True

        except Exception as e:
            self.logger.error(f"Error updating rule: {str(e)}")
            return False

    def get_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """
        获取规则

        Args:
            rule_id: 规则 ID

        Returns:
            规则对象
        """
        return self.rules.get(rule_id)

    def get_all_rules(self) -> List[Dict[str, Any]]:
        """
        获取所有规则

        Returns:
            规则列表
        """
        return list(self.rules.values())

    def get_rules_by_type(self, rule_type: str) -> List[Dict[str, Any]]:
        """
        按类型获取规则

        Args:
            rule_type: 规则类型

        Returns:
            规则列表
        """
        return [rule for rule in self.rules.values() if rule.get('type') == rule_type]

    def evaluate_rules(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        评估规则

        Args:
            data: 评估数据

        Returns:
            匹配的规则列表
        """
        try:
            matched_rules = []

            # 按优先级排序规则
            sorted_rules = sorted(
                self.rules.values(),
                key=lambda r: r.get('priority', 5),
                reverse=True
            )

            # 评估每个规则
            for rule in sorted_rules:
                # 跳过禁用的规则
                if rule.get('status') != 'enabled':
                    continue

                # 评估规则
                if self._evaluate_rule(rule, data):
                    matched_rules.append(rule)
                    self.logger.info(f"Rule matched: {rule['rule_id']} - {rule['name']}")

            return matched_rules

        except Exception as e:
            self.logger.error(f"Error evaluating rules: {str(e)}")
            return []

    def _validate_rule(self, rule: Dict[str, Any]) -> bool:
        """
        验证规则

        Args:
            rule: 规则对象

        Returns:
            是否有效
        """
        try:
            # 检查必要字段
            required_fields = ['name', 'description', 'type', 'conditions', 'actions']
            for field in required_fields:
                if field not in rule:
                    self.logger.error(f"Missing required field {field} in rule")
                    return False

            # 检查规则类型
            rule_type = rule['type']
            if rule_type not in self.rule_handlers:
                self.logger.error(f"Invalid rule type: {rule_type}")
                return False

            # 检查条件
            conditions = rule['conditions']
            if not isinstance(conditions, list) or not conditions:
                self.logger.error("Invalid rule conditions")
                return False

            # 检查动作
            actions = rule['actions']
            if not isinstance(actions, list) or not actions:
                self.logger.error("Invalid rule actions")
                return False

            # 检查优先级
            if 'priority' in rule and not (1 <= rule['priority'] <= 10):
                self.logger.error("Invalid rule priority")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating rule: {str(e)}")
            return False

    def _evaluate_rule(self, rule: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """
        评估单个规则

        Args:
            rule: 规则对象
            data: 评估数据

        Returns:
            是否匹配
        """
        try:
            rule_type = rule['type']
            conditions = rule['conditions']

            # 使用对应的处理器评估规则
            if rule_type in self.rule_handlers:
                return self.rule_handlers[rule_type](conditions, data)
            else:
                self.logger.error(f"No handler for rule type: {rule_type}")
                return False

        except Exception as e:
            self.logger.error(f"Error evaluating rule: {str(e)}")
            return False

    def _handle_threshold_rule(self, conditions: List[Dict[str, Any]], data: Dict[str, Any]) -> bool:
        """
        处理阈值规则

        Args:
            conditions: 规则条件
            data: 评估数据

        Returns:
            是否匹配
        """
        try:
            for condition in conditions:
                parameter = condition['parameter']
                operator = condition['operator']
                value = condition['value']

                # 获取数据中的参数值
                param_value = self._get_parameter_value(parameter, data)
                if param_value is None:
                    return False

                # 评估条件
                if not self._evaluate_condition(param_value, operator, value):
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error handling threshold rule: {str(e)}")
            return False

    def _handle_trend_rule(self, conditions: List[Dict[str, Any]], data: Dict[str, Any]) -> bool:
        """
        处理趋势规则

        Args:
            conditions: 规则条件
            data: 评估数据

        Returns:
            是否匹配
        """
        try:
            for condition in conditions:
                parameter = condition['parameter']
                operator = condition['operator']
                value = condition['value']

                # 获取数据中的参数值
                param_value = self._get_parameter_value(parameter, data)
                if param_value is None:
                    return False

                # 评估条件
                if not self._evaluate_condition(param_value, operator, value):
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error handling trend rule: {str(e)}")
            return False

    def _handle_composite_rule(self, conditions: List[Dict[str, Any]], data: Dict[str, Any]) -> bool:
        """
        处理组合规则

        Args:
            conditions: 规则条件
            data: 评估数据

        Returns:
            是否匹配
        """
        try:
            # 组合规则需要所有条件都满足
            for condition in conditions:
                # 递归评估子条件
                if isinstance(condition, dict) and 'conditions' in condition:
                    if not self._evaluate_rule(condition, data):
                        return False
                else:
                    parameter = condition['parameter']
                    operator = condition['operator']
                    value = condition['value']

                    # 获取数据中的参数值
                    param_value = self._get_parameter_value(parameter, data)
                    if param_value is None:
                        return False

                    # 评估条件
                    if not self._evaluate_condition(param_value, operator, value):
                        return False

            return True

        except Exception as e:
            self.logger.error(f"Error handling composite rule: {str(e)}")
            return False

    def _handle_anomaly_rule(self, conditions: List[Dict[str, Any]], data: Dict[str, Any]) -> bool:
        """
        处理异常规则

        Args:
            conditions: 规则条件
            data: 评估数据

        Returns:
            是否匹配
        """
        try:
            for condition in conditions:
                parameter = condition['parameter']
                operator = condition['operator']
                value = condition['value']

                # 获取数据中的参数值
                param_value = self._get_parameter_value(parameter, data)
                if param_value is None:
                    return False

                # 评估条件
                if not self._evaluate_condition(param_value, operator, value):
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error handling anomaly rule: {str(e)}")
            return False

    def _handle_pattern_rule(self, conditions: List[Dict[str, Any]], data: Dict[str, Any]) -> bool:
        """
        处理模式规则

        Args:
            conditions: 规则条件
            data: 评估数据

        Returns:
            是否匹配
        """
        try:
            for condition in conditions:
                parameter = condition['parameter']
                operator = condition['operator']
                value = condition['value']

                # 获取数据中的参数值
                param_value = self._get_parameter_value(parameter, data)
                if param_value is None:
                    return False

                # 评估条件
                if not self._evaluate_condition(param_value, operator, value):
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error handling pattern rule: {str(e)}")
            return False

    def _get_parameter_value(self, parameter: str, data: Dict[str, Any]) -> Any:
        """
        获取参数值

        Args:
            parameter: 参数路径
            data: 数据

        Returns:
            参数值
        """
        try:
            # 支持嵌套参数路径
            if '.' in parameter:
                parts = parameter.split('.')
                value = data
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        return None
                return value
            else:
                return data.get(parameter)

        except Exception as e:
            self.logger.error(f"Error getting parameter value: {str(e)}")
            return None

    def _evaluate_condition(self, param_value: Any, operator: str, value: Any) -> bool:
        """
        评估条件

        Args:
            param_value: 参数值
            operator: 操作符
            value: 比较值

        Returns:
            是否满足条件
        """
        try:
            if operator == 'equals':
                return param_value == value
            elif operator == 'not_equals':
                return param_value != value
            elif operator == 'greater_than':
                return param_value > value
            elif operator == 'less_than':
                return param_value < value
            elif operator == 'greater_than_or_equal':
                return param_value >= value
            elif operator == 'less_than_or_equal':
                return param_value <= value
            elif operator == 'contains':
                return value in param_value
            elif operator == 'not_contains':
                return value not in param_value
            elif operator == 'cross_above':
                # 用于趋势交叉
                if isinstance(param_value, list) and len(param_value) >= 2:
                    return param_value[-1] > value and param_value[-2] <= value
                return False
            elif operator == 'cross_below':
                # 用于趋势交叉
                if isinstance(param_value, list) and len(param_value) >= 2:
                    return param_value[-1] < value and param_value[-2] >= value
                return False
            else:
                self.logger.error(f"Invalid operator: {operator}")
                return False

        except Exception as e:
            self.logger.error(f"Error evaluating condition: {str(e)}")
            return False

    def load_rules(self, rules: List[Dict[str, Any]]) -> int:
        """
        加载规则

        Args:
            rules: 规则列表

        Returns:
            成功加载的规则数量
        """
        count = 0
        for rule in rules:
            if self.add_rule(rule):
                count += 1
        return count

    def save_rules(self) -> List[Dict[str, Any]]:
        """
        保存规则

        Returns:
            规则列表
        """
        return list(self.rules.values())

    def get_default_rules(self) -> List[Dict[str, Any]]:
        """
        获取默认规则

        Returns:
            默认规则列表
        """
        return [
            {
                'name': '比特币价格突破规则',
                'description': '当比特币价格突破 20 日均线且成交量增加 50% 时生成买入信号',
                'type': 'trend',
                'conditions': [
                    {
                        'parameter': 'price.ma_20',
                        'operator': 'cross_above',
                        'value': 'price.current'
                    },
                    {
                        'parameter': 'volume.change',
                        'operator': 'greater_than',
                        'value': 0.5
                    }
                ],
                'actions': [
                    {
                        'type': 'generate_signal',
                        'signal_type': 'buy',
                        'asset': 'BTC',
                        'strength': 8,
                        'confidence': 0.7
                    }
                ],
                'priority': 5
            },
            {
                'name': '以太坊价格下跌规则',
                'description': '当以太坊价格跌破 50 日均线且市场情绪消极时生成卖出信号',
                'type': 'trend',
                'conditions': [
                    {
                        'parameter': 'price.ma_50',
                        'operator': 'cross_below',
                        'value': 'price.current'
                    },
                    {
                        'parameter': 'sentiment.average',
                        'operator': 'less_than',
                        'value': -0.3
                    }
                ],
                'actions': [
                    {
                        'type': 'generate_signal',
                        'signal_type': 'sell',
                        'asset': 'ETH',
                        'strength': 7,
                        'confidence': 0.6
                    }
                ],
                'priority': 5
            },
            {
                'name': '市场异常波动规则',
                'description': '当价格波动超过历史 95% 范围时生成预警信号',
                'type': 'anomaly',
                'conditions': [
                    {
                        'parameter': 'price.volatility',
                        'operator': 'greater_than',
                        'value': 0.05
                    },
                    {
                        'parameter': 'anomaly.risk',
                        'operator': 'equals',
                        'value': 'high'
                    }
                ],
                'actions': [
                    {
                        'type': 'generate_signal',
                        'signal_type': 'alert',
                        'asset': 'ALL',
                        'strength': 9,
                        'confidence': 0.8
                    }
                ],
                'priority': 8
            }
        ]
