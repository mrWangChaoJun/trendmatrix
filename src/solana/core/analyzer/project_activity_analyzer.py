# Project Activity Analyzer

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class ProjectActivityAnalyzer:
    """
    项目活跃度分析器
    分析项目的链上活动、开发者活动和社区参与度
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化项目活跃度分析器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 分析参数
        self.activity_weight = self.config.get('activity_weight', 0.4)
        self.developer_weight = self.config.get('developer_weight', 0.3)
        self.community_weight = self.config.get('community_weight', 0.3)

        # 时间窗口配置
        self.time_windows = {
            '24h': timedelta(hours=24),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '90d': timedelta(days=90)
        }

    def analyze_project_activity(self, project_data: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析项目活跃度

        Args:
            project_data: 项目基本数据
            historical_data: 历史活动数据

        Returns:
            活跃度分析结果
        """
        try:
            # 验证输入数据
            if not project_data or not historical_data:
                self.logger.error("Invalid input data for project activity analysis")
                return None

            # 分析结果
            analysis = {
                'project_id': project_data.get('project_id'),
                'project_name': project_data.get('name'),
                'analysis_timestamp': datetime.now().isoformat(),
                'time_windows': {},
                'overall_activity_score': 0.0,
                'activity_trend': 'stable',
                'key_metrics': {},
                'recommendations': []
            }

            # 分析不同时间窗口的活跃度
            for window_name, window_delta in self.time_windows.items():
                window_analysis = self._analyze_time_window(window_name, window_delta, project_data, historical_data)
                if window_analysis:
                    analysis['time_windows'][window_name] = window_analysis

            # 计算总体活跃度评分
            analysis['overall_activity_score'] = self._calculate_overall_score(analysis['time_windows'])

            # 分析活跃度趋势
            analysis['activity_trend'] = self._analyze_activity_trend(analysis['time_windows'])

            # 提取关键指标
            analysis['key_metrics'] = self._extract_key_metrics(analysis['time_windows'])

            # 生成建议
            analysis['recommendations'] = self._generate_recommendations(analysis)

            self.logger.info(f"Analyzed project activity for {project_data.get('name')}")
            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing project activity: {str(e)}")
            return None

    def _analyze_time_window(self, window_name: str, window_delta: timedelta, project_data: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析特定时间窗口的活跃度

        Args:
            window_name: 时间窗口名称
            window_delta: 时间窗口
            project_data: 项目基本数据
            historical_data: 历史活动数据

        Returns:
            时间窗口分析结果
        """
        try:
            # 计算时间范围
            end_time = datetime.now()
            start_time = end_time - window_delta

            # 过滤时间范围内的数据
            window_data = self._filter_data_by_time_range(historical_data, start_time, end_time)

            # 分析链上活动
            on_chain_activity = self._analyze_on_chain_activity(window_data)

            # 分析开发者活动
            developer_activity = self._analyze_developer_activity(window_data)

            # 分析社区参与度
            community_engagement = self._analyze_community_engagement(window_data)

            # 计算时间窗口活跃度评分
            window_score = (
                on_chain_activity['score'] * self.activity_weight +
                developer_activity['score'] * self.developer_weight +
                community_engagement['score'] * self.community_weight
            )

            # 确定活跃度等级
            activity_level = self._get_activity_level(window_score)

            return {
                'window_name': window_name,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'score': window_score,
                'activity_level': activity_level,
                'on_chain_activity': on_chain_activity,
                'developer_activity': developer_activity,
                'community_engagement': community_engagement,
                'metrics': {
                    'transaction_count': on_chain_activity['metrics'].get('transaction_count', 0),
                    'unique_addresses': on_chain_activity['metrics'].get('unique_addresses', 0),
                    'volume': on_chain_activity['metrics'].get('volume', 0),
                    'tvl': on_chain_activity['metrics'].get('tvl', 0),
                    'new_holders': on_chain_activity['metrics'].get('new_holders', 0),
                    'code_commits': developer_activity['metrics'].get('code_commits', 0),
                    'active_developers': developer_activity['metrics'].get('active_developers', 0),
                    'pull_requests': developer_activity['metrics'].get('pull_requests', 0),
                    'issue_resolutions': developer_activity['metrics'].get('issue_resolutions', 0),
                    'community_interactions': community_engagement['metrics'].get('community_interactions', 0),
                    'social_media_mentions': community_engagement['metrics'].get('social_media_mentions', 0),
                    'sentiment_score': community_engagement['metrics'].get('sentiment_score', 0.0)
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing time window {window_name}: {str(e)}")
            return None

    def _analyze_on_chain_activity(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析链上活动

        Args:
            window_data: 时间窗口内的数据

        Returns:
            链上活动分析结果
        """
        try:
            # 提取链上活动指标
            transaction_count = window_data.get('transaction_count', 0)
            unique_addresses = window_data.get('unique_addresses', 0)
            volume = window_data.get('volume', 0)
            tvl = window_data.get('tvl', 0)
            new_holders = window_data.get('new_holders', 0)

            # 计算链上活动评分
            # 这里使用简单的评分算法，实际应用中可以根据项目类型和行业标准进行调整
            transaction_score = min(1.0, transaction_count / 10000)  # 假设10000笔交易为满分
            address_score = min(1.0, unique_addresses / 1000)  # 假设1000个唯一地址为满分
            volume_score = min(1.0, volume / 100000000)  # 假设1亿交易量为满分
            tvl_score = min(1.0, tvl / 500000000)  # 假设5亿TVL为满分
            holders_score = min(1.0, new_holders / 500)  # 假设500个新持有者为满分

            # 计算综合链上活动评分
            on_chain_score = (
                transaction_score * 0.3 +
                address_score * 0.25 +
                volume_score * 0.2 +
                tvl_score * 0.15 +
                holders_score * 0.1
            )

            return {
                'score': on_chain_score,
                'level': self._get_activity_level(on_chain_score),
                'metrics': {
                    'transaction_count': transaction_count,
                    'unique_addresses': unique_addresses,
                    'volume': volume,
                    'tvl': tvl,
                    'new_holders': new_holders
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing on-chain activity: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_developer_activity(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析开发者活动

        Args:
            window_data: 时间窗口内的数据

        Returns:
            开发者活动分析结果
        """
        try:
            # 提取开发者活动指标
            code_commits = window_data.get('code_commits', 0)
            active_developers = window_data.get('active_developers', 0)
            pull_requests = window_data.get('pull_requests', 0)
            issue_resolutions = window_data.get('issue_resolutions', 0)

            # 计算开发者活动评分
            commit_score = min(1.0, code_commits / 100)  # 假设100次提交为满分
            developer_score = min(1.0, active_developers / 10)  # 假设10个活跃开发者为满分
            pr_score = min(1.0, pull_requests / 50)  # 假设50个PR为满分
            issue_score = min(1.0, issue_resolutions / 50)  # 假设50个问题解决为满分

            # 计算综合开发者活动评分
            developer_score = (
                commit_score * 0.4 +
                developer_score * 0.3 +
                pr_score * 0.15 +
                issue_score * 0.15
            )

            return {
                'score': developer_score,
                'level': self._get_activity_level(developer_score),
                'metrics': {
                    'code_commits': code_commits,
                    'active_developers': active_developers,
                    'pull_requests': pull_requests,
                    'issue_resolutions': issue_resolutions
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing developer activity: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_community_engagement(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析社区参与度

        Args:
            window_data: 时间窗口内的数据

        Returns:
            社区参与度分析结果
        """
        try:
            # 提取社区参与度指标
            community_interactions = window_data.get('community_interactions', 0)
            social_media_mentions = window_data.get('social_media_mentions', 0)
            sentiment_score = window_data.get('sentiment_score', 0.0)

            # 计算社区参与度评分
            interaction_score = min(1.0, community_interactions / 1000)  # 假设1000次互动为满分
            mention_score = min(1.0, social_media_mentions / 500)  # 假设500次提及为满分
            sentiment_normalized = (sentiment_score + 1) / 2  # 将情感分数从[-1,1]归一化到[0,1]

            # 计算综合社区参与度评分
            community_score = (
                interaction_score * 0.4 +
                mention_score * 0.3 +
                sentiment_normalized * 0.3
            )

            return {
                'score': community_score,
                'level': self._get_activity_level(community_score),
                'metrics': {
                    'community_interactions': community_interactions,
                    'social_media_mentions': social_media_mentions,
                    'sentiment_score': sentiment_score
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing community engagement: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _calculate_overall_score(self, time_windows: Dict[str, Any]) -> float:
        """
        计算总体活跃度评分

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            总体活跃度评分
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

    def _analyze_activity_trend(self, time_windows: Dict[str, Any]) -> str:
        """
        分析活跃度趋势

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            活跃度趋势
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
                trend = 'rapidly_increasing'
            elif score_change > 0.05:
                trend = 'increasing'
            elif score_change < -0.2:
                trend = 'rapidly_decreasing'
            elif score_change < -0.05:
                trend = 'decreasing'

            return trend

        except Exception as e:
            self.logger.error(f"Error analyzing activity trend: {str(e)}")
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
                'highest_activity_window': None,
                'lowest_activity_window': None,
                'most_active_metric': None,
                'least_active_metric': None,
                'average_transaction_count': 0,
                'average_unique_addresses': 0,
                'average_volume': 0,
                'average_tvl': 0,
                'average_code_commits': 0
            }

            if not time_windows:
                return key_metrics

            # 找出活跃度最高和最低的时间窗口
            window_scores = [(name, data['score']) for name, data in time_windows.items()]
            if window_scores:
                window_scores.sort(key=lambda x: x[1], reverse=True)
                key_metrics['highest_activity_window'] = window_scores[0][0]
                key_metrics['lowest_activity_window'] = window_scores[-1][0]

            # 计算平均指标
            total_transactions = 0
            total_addresses = 0
            total_volume = 0
            total_tvl = 0
            total_commits = 0
            window_count = len(time_windows)

            for window_data in time_windows.values():
                metrics = window_data.get('metrics', {})
                total_transactions += metrics.get('transaction_count', 0)
                total_addresses += metrics.get('unique_addresses', 0)
                total_volume += metrics.get('volume', 0)
                total_tvl += metrics.get('tvl', 0)
                total_commits += metrics.get('code_commits', 0)

            if window_count > 0:
                key_metrics['average_transaction_count'] = total_transactions / window_count
                key_metrics['average_unique_addresses'] = total_addresses / window_count
                key_metrics['average_volume'] = total_volume / window_count
                key_metrics['average_tvl'] = total_tvl / window_count
                key_metrics['average_code_commits'] = total_commits / window_count

            return key_metrics

        except Exception as e:
            self.logger.error(f"Error extracting key metrics: {str(e)}")
            return {}

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        生成建议

        Args:
            analysis: 活跃度分析结果

        Returns:
            建议列表
        """
        try:
            recommendations = []
            overall_score = analysis.get('overall_activity_score', 0)
            trend = analysis.get('activity_trend', 'stable')
            key_metrics = analysis.get('key_metrics', {})

            # 基于总体活跃度评分的建议
            if overall_score < 0.3:
                recommendations.append("项目活跃度较低，建议关注项目团队的开发进度和社区运营策略")
                recommendations.append("建议监控项目的代码提交频率和社区互动情况")
            elif overall_score > 0.7:
                recommendations.append("项目活跃度较高，建议关注项目的可持续性和发展方向")
                recommendations.append("建议分析项目的用户增长趋势和TVL变化")

            # 基于活跃度趋势的建议
            if trend == 'rapidly_increasing':
                recommendations.append("项目活跃度快速增长，建议关注是否有重大事件或更新")
            elif trend == 'rapidly_decreasing':
                recommendations.append("项目活跃度快速下降，建议分析原因并评估项目健康状况")

            # 基于关键指标的建议
            if key_metrics.get('average_code_commits', 0) < 5:
                recommendations.append("开发者活动较少，建议关注项目的开发团队稳定性")

            if key_metrics.get('average_unique_addresses', 0) < 100:
                recommendations.append("用户数量较少，建议关注项目的用户获取策略")

            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def _filter_data_by_time_range(self, historical_data: Dict[str, Any], start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """
        过滤时间范围内的数据

        Args:
            historical_data: 历史数据
            start_time: 开始时间
            end_time: 结束时间

        Returns:
            过滤后的数据
        """
        try:
            # 这里应该根据实际数据结构进行过滤
            # 现在返回模拟数据
            return {
                'transaction_count': 1000 + int((end_time - start_time).days * 10),
                'unique_addresses': 100 + int((end_time - start_time).days),
                'volume': 1000000 + int((end_time - start_time).days * 10000),
                'tvl': 5000000 + int((end_time - start_time).days * 50000),
                'new_holders': 50 + int((end_time - start_time).days),
                'code_commits': 20 + int((end_time - start_time).days // 7),
                'active_developers': 3 + int((end_time - start_time).days // 30),
                'pull_requests': 10 + int((end_time - start_time).days // 7),
                'issue_resolutions': 8 + int((end_time - start_time).days // 7),
                'community_interactions': 500 + int((end_time - start_time).days * 5),
                'social_media_mentions': 200 + int((end_time - start_time).days * 2),
                'sentiment_score': 0.2 + ((end_time - start_time).days / 90) * 0.3
            }

        except Exception as e:
            self.logger.error(f"Error filtering data by time range: {str(e)}")
            return {}

    def _get_activity_level(self, score: float) -> str:
        """
        根据评分确定活跃度等级

        Args:
            score: 活跃度评分

        Returns:
            活跃度等级
        """
        if score >= 0.8:
            return 'very_high'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        elif score >= 0.2:
            return 'low'
        else:
            return 'very_low'

    def analyze_multiple_projects(self, projects_data: List[Dict[str, Any]], historical_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分析多个项目的活跃度

        Args:
            projects_data: 多个项目的基本数据
            historical_data: 历史活动数据

        Returns:
            多个项目的活跃度分析结果
        """
        try:
            analyses = []
            for project_data in projects_data:
                analysis = self.analyze_project_activity(project_data, historical_data)
                if analysis:
                    analyses.append(analysis)

            # 对项目进行排序
            analyses.sort(key=lambda x: x.get('overall_activity_score', 0), reverse=True)

            return analyses

        except Exception as e:
            self.logger.error(f"Error analyzing multiple projects: {str(e)}")
            return []
