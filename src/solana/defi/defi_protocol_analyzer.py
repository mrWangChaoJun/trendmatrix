# DeFi Protocol Analyzer

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class DeFiProtocolAnalyzer:
    """
    DeFi协议分析器
    分析DeFi协议的流动性、收益率和风险指标
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化DeFi协议分析器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 分析参数
        self.liquidity_weight = self.config.get('liquidity_weight', 0.4)
        self.yield_weight = self.config.get('yield_weight', 0.3)
        self.risk_weight = self.config.get('risk_weight', 0.2)
        self.growth_weight = self.config.get('growth_weight', 0.1)

        # 时间窗口配置
        self.time_windows = {
            '24h': timedelta(hours=24),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '90d': timedelta(days=90)
        }

    def analyze_defi_protocol(self, protocol_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析DeFi协议

        Args:
            protocol_data: 协议基本数据
            market_data: 市场数据

        Returns:
            协议分析结果
        """
        try:
            # 验证输入数据
            if not protocol_data or not market_data:
                self.logger.error("Invalid input data for DeFi protocol analysis")
                return None

            # 分析结果
            analysis = {
                'protocol_id': protocol_data.get('protocol_id'),
                'protocol_name': protocol_data.get('name'),
                'protocol_type': protocol_data.get('type'),
                'analysis_timestamp': datetime.now().isoformat(),
                'time_windows': {},
                'overall_score': 0.0,
                'trend': 'stable',
                'key_metrics': {},
                'liquidity_analysis': {},
                'yield_analysis': {},
                'risk_analysis': {},
                'growth_analysis': {},
                'comparative_analysis': {},
                'recommendations': []
            }

            # 分析不同时间窗口的数据
            for window_name, window_delta in self.time_windows.items():
                window_analysis = self._analyze_time_window(window_name, window_delta, protocol_data, market_data)
                if window_analysis:
                    analysis['time_windows'][window_name] = window_analysis

            # 计算总体评分
            analysis['overall_score'] = self._calculate_overall_score(analysis['time_windows'])

            # 分析趋势
            analysis['trend'] = self._analyze_trend(analysis['time_windows'])

            # 提取关键指标
            analysis['key_metrics'] = self._extract_key_metrics(analysis['time_windows'])

            # 分析流动性
            analysis['liquidity_analysis'] = self._analyze_liquidity(analysis['time_windows'])

            # 分析收益率
            analysis['yield_analysis'] = self._analyze_yield(analysis['time_windows'])

            # 分析风险
            analysis['risk_analysis'] = self._analyze_risk(analysis['time_windows'])

            # 分析增长
            analysis['growth_analysis'] = self._analyze_growth(analysis['time_windows'])

            # 生成建议
            analysis['recommendations'] = self._generate_recommendations(analysis)

            self.logger.info(f"Analyzed DeFi protocol: {protocol_data.get('name')}")
            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing DeFi protocol: {str(e)}")
            return None

    def _analyze_time_window(self, window_name: str, window_delta: timedelta, protocol_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析特定时间窗口的数据

        Args:
            window_name: 时间窗口名称
            window_delta: 时间窗口
            protocol_data: 协议基本数据
            market_data: 市场数据

        Returns:
            时间窗口分析结果
        """
        try:
            # 计算时间范围
            end_time = datetime.now()
            start_time = end_time - window_delta

            # 过滤时间范围内的数据
            window_data = self._filter_data_by_time_range(market_data, start_time, end_time)

            # 分析流动性
            liquidity_analysis = self._analyze_window_liquidity(window_data)

            # 分析收益率
            yield_analysis = self._analyze_window_yield(window_data)

            # 分析风险
            risk_analysis = self._analyze_window_risk(window_data)

            # 分析增长
            growth_analysis = self._analyze_window_growth(window_data)

            # 计算时间窗口评分
            window_score = (
                liquidity_analysis['score'] * self.liquidity_weight +
                yield_analysis['score'] * self.yield_weight +
                risk_analysis['score'] * self.risk_weight +
                growth_analysis['score'] * self.growth_weight
            )

            # 确定等级
            level = self._get_level(window_score)

            return {
                'window_name': window_name,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'score': window_score,
                'level': level,
                'liquidity': liquidity_analysis,
                'yield': yield_analysis,
                'risk': risk_analysis,
                'growth': growth_analysis,
                'metrics': {
                    'total_liquidity': liquidity_analysis['metrics'].get('total_liquidity', 0),
                    'liquidity_change': liquidity_analysis['metrics'].get('liquidity_change', 0.0),
                    'average_apy': yield_analysis['metrics'].get('average_apy', 0.0),
                    'apy_volatility': yield_analysis['metrics'].get('apy_volatility', 0.0),
                    'risk_score': risk_analysis['metrics'].get('risk_score', 0.0),
                    'liquidity_risk': risk_analysis['metrics'].get('liquidity_risk', 0.0),
                    'smart_contract_risk': risk_analysis['metrics'].get('smart_contract_risk', 0.0),
                    'growth_rate': growth_analysis['metrics'].get('growth_rate', 0.0),
                    'user_growth': growth_analysis['metrics'].get('user_growth', 0.0),
                    'transaction_count': window_data.get('transaction_count', 0),
                    'volume': window_data.get('volume', 0)
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing time window {window_name}: {str(e)}")
            return None

    def _analyze_window_liquidity(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的流动性

        Args:
            window_data: 时间窗口内的数据

        Returns:
            流动性分析结果
        """
        try:
            # 提取流动性指标
            total_liquidity = window_data.get('total_liquidity', 0)
            liquidity_change = window_data.get('liquidity_change', 0.0)
            liquidity_depth = window_data.get('liquidity_depth', 0)
            liquidity_concentration = window_data.get('liquidity_concentration', 0.0)

            # 计算流动性评分
            liquidity_score = min(1.0, total_liquidity / 100000000)  # 假设1亿为满分
            change_score = min(1.0, max(0.0, (liquidity_change + 1) / 2))  # 将变化率从[-1,1]归一化到[0,1]
            depth_score = min(1.0, liquidity_depth / 10000000)  # 假设1000万为满分
            concentration_score = min(1.0, 1 - liquidity_concentration)  # 集中度越低评分越高

            # 计算综合流动性评分
            overall_liquidity_score = (
                liquidity_score * 0.4 +
                change_score * 0.3 +
                depth_score * 0.2 +
                concentration_score * 0.1
            )

            return {
                'score': overall_liquidity_score,
                'level': self._get_level(overall_liquidity_score),
                'metrics': {
                    'total_liquidity': total_liquidity,
                    'liquidity_change': liquidity_change,
                    'liquidity_depth': liquidity_depth,
                    'liquidity_concentration': liquidity_concentration
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window liquidity: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_window_yield(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的收益率

        Args:
            window_data: 时间窗口内的数据

        Returns:
            收益率分析结果
        """
        try:
            # 提取收益率指标
            average_apy = window_data.get('average_apy', 0.0)
            apy_volatility = window_data.get('apy_volatility', 0.0)
            yield_consistency = window_data.get('yield_consistency', 0.0)
            yield_comparison = window_data.get('yield_comparison', 0.0)  # 与同类协议的比较

            # 计算收益率评分
            apy_score = min(1.0, average_apy / 0.5)  # 假设50% APY为满分
            consistency_score = yield_consistency  # 一致性直接作为分数
            comparison_score = yield_comparison  # 比较分数直接作为分数
            stability_score = min(1.0, 1 - apy_volatility)  # 波动性越低评分越高

            # 计算综合收益率评分
            overall_yield_score = (
                apy_score * 0.4 +
                consistency_score * 0.3 +
                comparison_score * 0.2 +
                stability_score * 0.1
            )

            return {
                'score': overall_yield_score,
                'level': self._get_level(overall_yield_score),
                'metrics': {
                    'average_apy': average_apy,
                    'apy_volatility': apy_volatility,
                    'yield_consistency': yield_consistency,
                    'yield_comparison': yield_comparison
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window yield: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_window_risk(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的风险

        Args:
            window_data: 时间窗口内的数据

        Returns:
            风险分析结果
        """
        try:
            # 提取风险指标
            risk_score = window_data.get('risk_score', 0.0)
            liquidity_risk = window_data.get('liquidity_risk', 0.0)
            smart_contract_risk = window_data.get('smart_contract_risk', 0.0)
            market_risk = window_data.get('market_risk', 0.0)

            # 计算风险评分（风险越低评分越高）
            risk_score_normalized = 1 - min(1.0, risk_score)
            liquidity_risk_normalized = 1 - min(1.0, liquidity_risk)
            smart_contract_risk_normalized = 1 - min(1.0, smart_contract_risk)
            market_risk_normalized = 1 - min(1.0, market_risk)

            # 计算综合风险评分
            overall_risk_score = (
                risk_score_normalized * 0.4 +
                liquidity_risk_normalized * 0.3 +
                smart_contract_risk_normalized * 0.2 +
                market_risk_normalized * 0.1
            )

            return {
                'score': overall_risk_score,
                'level': self._get_level(overall_risk_score),
                'metrics': {
                    'risk_score': risk_score,
                    'liquidity_risk': liquidity_risk,
                    'smart_contract_risk': smart_contract_risk,
                    'market_risk': market_risk
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window risk: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_window_growth(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的增长

        Args:
            window_data: 时间窗口内的数据

        Returns:
            增长分析结果
        """
        try:
            # 提取增长指标
            growth_rate = window_data.get('growth_rate', 0.0)
            user_growth = window_data.get('user_growth', 0.0)
            transaction_growth = window_data.get('transaction_growth', 0.0)
            volume_growth = window_data.get('volume_growth', 0.0)

            # 计算增长评分
            growth_score = min(1.0, growth_rate)
            user_score = min(1.0, user_growth)
            transaction_score = min(1.0, transaction_growth)
            volume_score = min(1.0, volume_growth)

            # 计算综合增长评分
            overall_growth_score = (
                growth_score * 0.4 +
                user_score * 0.3 +
                transaction_score * 0.15 +
                volume_score * 0.15
            )

            return {
                'score': overall_growth_score,
                'level': self._get_level(overall_growth_score),
                'metrics': {
                    'growth_rate': growth_rate,
                    'user_growth': user_growth,
                    'transaction_growth': transaction_growth,
                    'volume_growth': volume_growth
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window growth: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _calculate_overall_score(self, time_windows: Dict[str, Any]) -> float:
        """
        计算总体评分

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            总体评分
        """
        try:
            if not time_windows:
                return 0.0

            # 计算不同时间窗口的加权平均
            weights = {
                '24h': 0.1,
                '7d': 0.2,
                '30d': 0.4,
                '90d': 0.3
            }

            weighted_sum = 0.0
            total_weight = 0.0

            for window_name, window_analysis in time_windows.items():
                if window_name in weights:
                    weighted_sum += window_analysis['score'] * weights[window_name]
                    total_weight += weights[window_name]

            if total_weight > 0:
                return weighted_sum / total_weight
            else:
                return 0.0

        except Exception as e:
            self.logger.error(f"Error calculating overall score: {str(e)}")
            return 0.0

    def _analyze_trend(self, time_windows: Dict[str, Any]) -> str:
        """
        分析趋势

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            趋势
        """
        try:
            if not time_windows:
                return 'stable'

            # 提取最近两个时间窗口的评分
            recent_windows = ['24h', '7d', '30d']
            scores = []

            for window_name in recent_windows:
                if window_name in time_windows:
                    scores.append(time_windows[window_name]['score'])

            if len(scores) < 2:
                return 'stable'

            # 计算趋势
            trend = 'stable'
            recent_score = scores[0]
            previous_score = scores[-1]

            score_change = (recent_score - previous_score) / previous_score if previous_score > 0 else 0

            if score_change > 0.2:
                trend = 'rapidly_improving'
            elif score_change > 0.05:
                trend = 'improving'
            elif score_change < -0.2:
                trend = 'rapidly_declining'
            elif score_change < -0.05:
                trend = 'declining'

            return trend

        except Exception as e:
            self.logger.error(f"Error analyzing trend: {str(e)}")
            return 'stable'

    def _extract_key_metrics(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取关键指标

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            关键指标
        """
        try:
            key_metrics = {
                'average_total_liquidity': 0,
                'average_apy': 0,
                'average_risk_score': 0,
                'average_growth_rate': 0,
                'highest_performing_window': None,
                'lowest_performing_window': None,
                'best_metric': None,
                'worst_metric': None,
                'average_transaction_count': 0,
                'average_volume': 0
            }

            if not time_windows:
                return key_metrics

            # 计算平均指标
            total_liquidity = 0
            total_apy = 0
            total_risk = 0
            total_growth = 0
            total_transactions = 0
            total_volume = 0
            window_count = len(time_windows)

            for window_data in time_windows.values():
                metrics = window_data.get('metrics', {})
                total_liquidity += metrics.get('total_liquidity', 0)
                total_apy += metrics.get('average_apy', 0)
                total_risk += metrics.get('risk_score', 0)
                total_growth += metrics.get('growth_rate', 0)
                total_transactions += metrics.get('transaction_count', 0)
                total_volume += metrics.get('volume', 0)

            if window_count > 0:
                key_metrics['average_total_liquidity'] = total_liquidity / window_count
                key_metrics['average_apy'] = total_apy / window_count
                key_metrics['average_risk_score'] = total_risk / window_count
                key_metrics['average_growth_rate'] = total_growth / window_count
                key_metrics['average_transaction_count'] = total_transactions / window_count
                key_metrics['average_volume'] = total_volume / window_count

            # 找出表现最好和最差的时间窗口
            window_scores = [(name, data['score']) for name, data in time_windows.items()]
            if window_scores:
                window_scores.sort(key=lambda x: x[1], reverse=True)
                key_metrics['highest_performing_window'] = window_scores[0][0]
                key_metrics['lowest_performing_window'] = window_scores[-1][0]

            return key_metrics

        except Exception as e:
            self.logger.error(f"Error extracting key metrics: {str(e)}")
            return {}

    def _analyze_liquidity(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析流动性

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            流动性分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取流动性数据
            liquidity_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                liquidity_data.append({
                    'window': window_name,
                    'total_liquidity': metrics.get('total_liquidity', 0),
                    'liquidity_change': metrics.get('liquidity_change', 0.0)
                })

            # 分析流动性趋势
            liquidities = [d['total_liquidity'] for d in liquidity_data]
            changes = [d['liquidity_change'] for d in liquidity_data]

            # 计算流动性趋势
            liquidity_trend = 'stable'
            if len(liquidities) >= 2:
                if liquidities[-1] > liquidities[0] * 1.1:
                    liquidity_trend = 'increasing'
                elif liquidities[-1] < liquidities[0] * 0.9:
                    liquidity_trend = 'decreasing'

            return {
                'liquidity_data': liquidity_data,
                'liquidity_trend': liquidity_trend,
                'average_liquidity_change': sum(changes) / len(changes) if changes else 0
            }

        except Exception as e:
            self.logger.error(f"Error analyzing liquidity: {str(e)}")
            return {}

    def _analyze_yield(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析收益率

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            收益率分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取收益率数据
            yield_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                yield_data.append({
                    'window': window_name,
                    'average_apy': metrics.get('average_apy', 0.0),
                    'apy_volatility': metrics.get('apy_volatility', 0.0)
                })

            # 分析收益率趋势
            apys = [d['average_apy'] for d in yield_data]
            volatilities = [d['apy_volatility'] for d in yield_data]

            # 计算收益率趋势
            yield_trend = 'stable'
            if len(apys) >= 2:
                if apys[-1] > apys[0] * 1.1:
                    yield_trend = 'increasing'
                elif apys[-1] < apys[0] * 0.9:
                    yield_trend = 'decreasing'

            return {
                'yield_data': yield_data,
                'yield_trend': yield_trend,
                'average_apy': sum(apys) / len(apys) if apys else 0,
                'average_volatility': sum(volatilities) / len(volatilities) if volatilities else 0
            }

        except Exception as e:
            self.logger.error(f"Error analyzing yield: {str(e)}")
            return {}

    def _analyze_risk(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析风险

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            风险分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取风险数据
            risk_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                risk_data.append({
                    'window': window_name,
                    'risk_score': metrics.get('risk_score', 0.0),
                    'liquidity_risk': metrics.get('liquidity_risk', 0.0),
                    'smart_contract_risk': metrics.get('smart_contract_risk', 0.0)
                })

            # 分析风险趋势
            risk_scores = [d['risk_score'] for d in risk_data]
            liquidity_risks = [d['liquidity_risk'] for d in risk_data]
            sc_risks = [d['smart_contract_risk'] for d in risk_data]

            # 计算风险趋势
            risk_trend = 'stable'
            if len(risk_scores) >= 2:
                if risk_scores[-1] > risk_scores[0] * 1.1:
                    risk_trend = 'increasing'
                elif risk_scores[-1] < risk_scores[0] * 0.9:
                    risk_trend = 'decreasing'

            return {
                'risk_data': risk_data,
                'risk_trend': risk_trend,
                'average_risk_score': sum(risk_scores) / len(risk_scores) if risk_scores else 0,
                'average_liquidity_risk': sum(liquidity_risks) / len(liquidity_risks) if liquidity_risks else 0,
                'average_smart_contract_risk': sum(sc_risks) / len(sc_risks) if sc_risks else 0
            }

        except Exception as e:
            self.logger.error(f"Error analyzing risk: {str(e)}")
            return {}

    def _analyze_growth(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析增长

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            增长分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取增长数据
            growth_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                growth_data.append({
                    'window': window_name,
                    'growth_rate': metrics.get('growth_rate', 0.0),
                    'user_growth': metrics.get('user_growth', 0.0)
                })

            # 分析增长趋势
            growth_rates = [d['growth_rate'] for d in growth_data]
            user_growths = [d['user_growth'] for d in growth_data]

            # 计算增长趋势
            growth_trend = 'stable'
            if len(growth_rates) >= 2:
                if growth_rates[-1] > growth_rates[0] * 1.1:
                    growth_trend = 'accelerating'
                elif growth_rates[-1] < growth_rates[0] * 0.9:
                    growth_trend = 'decelerating'

            return {
                'growth_data': growth_data,
                'growth_trend': growth_trend,
                'average_growth_rate': sum(growth_rates) / len(growth_rates) if growth_rates else 0,
                'average_user_growth': sum(user_growths) / len(user_growths) if user_growths else 0
            }

        except Exception as e:
            self.logger.error(f"Error analyzing growth: {str(e)}")
            return {}

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        生成建议

        Args:
            analysis: DeFi协议分析结果

        Returns:
            建议列表
        """
        try:
            recommendations = []
            overall_score = analysis.get('overall_score', 0)
            trend = analysis.get('trend', 'stable')
            key_metrics = analysis.get('key_metrics', {})
            liquidity_analysis = analysis.get('liquidity_analysis', {})
            yield_analysis = analysis.get('yield_analysis', {})
            risk_analysis = analysis.get('risk_analysis', {})

            # 基于总体评分的建议
            if overall_score < 0.3:
                recommendations.append("协议整体表现较差，建议关注其流动性和风险管理策略")
                recommendations.append("建议监控协议的用户增长和交易活跃度")
            elif overall_score > 0.7:
                recommendations.append("协议整体表现较好，建议关注其可持续性和进一步增长潜力")
                recommendations.append("建议分析其与同类协议的比较优势")

            # 基于趋势的建议
            if trend == 'rapidly_improving':
                recommendations.append("协议表现快速改善，建议关注其近期的产品更新和市场策略")
            elif trend == 'rapidly_declining':
                recommendations.append("协议表现快速下降，建议分析原因并评估投资风险")

            # 基于关键指标的建议
            if key_metrics.get('average_apy', 0) > 0.5:
                recommendations.append("收益率较高，建议关注其可持续性和风险水平")
            elif key_metrics.get('average_apy', 0) < 0.05:
                recommendations.append("收益率较低，建议关注其竞争力和改进空间")

            if key_metrics.get('average_risk_score', 0) > 0.7:
                recommendations.append("风险水平较高，建议关注其安全措施和审计情况")

            if key_metrics.get('average_total_liquidity', 0) < 1000000:
                recommendations.append("流动性较低，建议关注其流动性风险和深度")

            # 基于流动性分析的建议
            if liquidity_analysis.get('liquidity_trend') == 'decreasing':
                recommendations.append("流动性呈下降趋势，建议关注其资金流出原因")

            # 基于收益率分析的建议
            if yield_analysis.get('yield_trend') == 'decreasing':
                recommendations.append("收益率呈下降趋势，建议关注其收益模型的可持续性")

            # 基于风险分析的建议
            if risk_analysis.get('risk_trend') == 'increasing':
                recommendations.append("风险呈上升趋势，建议关注其风险管理措施")

            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def _filter_data_by_time_range(self, market_data: Dict[str, Any], start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """
        过滤时间范围内的数据

        Args:
            market_data: 市场数据
            start_time: 开始时间
            end_time: 结束时间

        Returns:
            过滤后的数据
        """
        try:
            # 这里应该根据实际数据结构进行过滤
            # 现在返回模拟数据
            days_in_window = (end_time - start_time).days
            return {
                'total_liquidity': 10000000 + days_in_window * 1000000,
                'liquidity_change': 0.02 * days_in_window,
                'liquidity_depth': 1000000 + days_in_window * 100000,
                'liquidity_concentration': 0.4 - days_in_window * 0.005,
                'average_apy': 0.1 + days_in_window * 0.001,
                'apy_volatility': 0.2 - days_in_window * 0.001,
                'yield_consistency': 0.7 + days_in_window * 0.005,
                'yield_comparison': 0.6 + days_in_window * 0.003,
                'risk_score': 0.3 - days_in_window * 0.001,
                'liquidity_risk': 0.25 - days_in_window * 0.001,
                'smart_contract_risk': 0.2 - days_in_window * 0.0005,
                'market_risk': 0.35 - days_in_window * 0.001,
                'growth_rate': 0.1 + days_in_window * 0.002,
                'user_growth': 0.15 + days_in_window * 0.003,
                'transaction_growth': 0.12 + days_in_window * 0.002,
                'volume_growth': 0.18 + days_in_window * 0.002,
                'transaction_count': 10000 + days_in_window * 1000,
                'volume': 5000000 + days_in_window * 500000
            }

        except Exception as e:
            self.logger.error(f"Error filtering data by time range: {str(e)}")
            return {}

    def _get_level(self, score: float) -> str:
        """
        根据评分确定等级

        Args:
            score: 评分

        Returns:
            等级
        """
        if score >= 0.8:
            return 'excellent'
        elif score >= 0.6:
            return 'good'
        elif score >= 0.4:
            return 'fair'
        elif score >= 0.2:
            return 'poor'
        else:
            return 'very_poor'

    def analyze_multiple_protocols(self, protocols_data: List[Dict[str, Any]], market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分析多个DeFi协议

        Args:
            protocols_data: 多个协议的基本数据
            market_data: 市场数据

        Returns:
            多个协议的分析结果
        """
        try:
            analyses = []
            for protocol_data in protocols_data:
                analysis = self.analyze_defi_protocol(protocol_data, market_data)
                if analysis:
                    analyses.append(analysis)

            # 对协议进行排序
            analyses.sort(key=lambda x: x.get('overall_score', 0), reverse=True)

            return analyses

        except Exception as e:
            self.logger.error(f"Error analyzing multiple protocols: {str(e)}")
            return []
