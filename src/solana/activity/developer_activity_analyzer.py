# Developer Activity Analyzer

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class DeveloperActivityAnalyzer:
    """
    开发者活动分析器
    分析开发者的代码提交、贡献和活跃度
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化开发者活动分析器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 分析参数
        self.commit_weight = self.config.get('commit_weight', 0.4)
        self.repository_weight = self.config.get('repository_weight', 0.2)
        self.contribution_weight = self.config.get('contribution_weight', 0.2)
        self.activity_weight = self.config.get('activity_weight', 0.2)

        # 时间窗口配置
        self.time_windows = {
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '90d': timedelta(days=90),
            '180d': timedelta(days=180)
        }

    def analyze_developer_activity(self, developer_data: Dict[str, Any], repository_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析开发者活动

        Args:
            developer_data: 开发者基本数据
            repository_data: 仓库数据

        Returns:
            开发者活动分析结果
        """
        try:
            # 验证输入数据
            if not developer_data or not repository_data:
                self.logger.error("Invalid input data for developer activity analysis")
                return None

            # 分析结果
            analysis = {
                'developer_id': developer_data.get('developer_id'),
                'developer_name': developer_data.get('name'),
                'username': developer_data.get('username'),
                'analysis_timestamp': datetime.now().isoformat(),
                'time_windows': {},
                'overall_activity_score': 0.0,
                'activity_trend': 'stable',
                'key_metrics': {},
                'top_repositories': [],
                'skills_analysis': {},
                'recommendations': []
            }

            # 分析不同时间窗口的活跃度
            for window_name, window_delta in self.time_windows.items():
                window_analysis = self._analyze_time_window(window_name, window_delta, developer_data, repository_data)
                if window_analysis:
                    analysis['time_windows'][window_name] = window_analysis

            # 计算总体活跃度评分
            analysis['overall_activity_score'] = self._calculate_overall_score(analysis['time_windows'])

            # 分析活跃度趋势
            analysis['activity_trend'] = self._analyze_activity_trend(analysis['time_windows'])

            # 提取关键指标
            analysis['key_metrics'] = self._extract_key_metrics(analysis['time_windows'])

            # 分析顶级仓库
            analysis['top_repositories'] = self._analyze_top_repositories(repository_data)

            # 分析技能
            analysis['skills_analysis'] = self._analyze_skills(developer_data, repository_data)

            # 生成建议
            analysis['recommendations'] = self._generate_recommendations(analysis)

            self.logger.info(f"Analyzed developer activity for {developer_data.get('name')}")
            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing developer activity: {str(e)}")
            return None

    def _analyze_time_window(self, window_name: str, window_delta: timedelta, developer_data: Dict[str, Any], repository_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析特定时间窗口的开发者活动

        Args:
            window_name: 时间窗口名称
            window_delta: 时间窗口
            developer_data: 开发者基本数据
            repository_data: 仓库数据

        Returns:
            时间窗口分析结果
        """
        try:
            # 计算时间范围
            end_time = datetime.now()
            start_time = end_time - window_delta

            # 过滤时间范围内的数据
            window_data = self._filter_data_by_time_range(repository_data, start_time, end_time)

            # 分析代码提交
            commit_analysis = self._analyze_code_commits(window_data)

            # 分析仓库活动
            repository_analysis = self._analyze_repository_activity(window_data)

            # 分析贡献
            contribution_analysis = self._analyze_contributions(window_data)

            # 分析活跃度
            activity_analysis = self._analyze_activity_patterns(window_data)

            # 计算时间窗口活跃度评分
            window_score = (
                commit_analysis['score'] * self.commit_weight +
                repository_analysis['score'] * self.repository_weight +
                contribution_analysis['score'] * self.contribution_weight +
                activity_analysis['score'] * self.activity_weight
            )

            # 确定活跃度等级
            activity_level = self._get_activity_level(window_score)

            return {
                'window_name': window_name,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'score': window_score,
                'activity_level': activity_level,
                'code_commits': commit_analysis,
                'repository_activity': repository_analysis,
                'contributions': contribution_analysis,
                'activity_patterns': activity_analysis,
                'metrics': {
                    'total_commits': commit_analysis['metrics'].get('total_commits', 0),
                    'commit_frequency': commit_analysis['metrics'].get('commit_frequency', 0.0),
                    'active_repositories': repository_analysis['metrics'].get('active_repositories', 0),
                    'repository_contribution_ratio': repository_analysis['metrics'].get('repository_contribution_ratio', 0.0),
                    'pull_requests': contribution_analysis['metrics'].get('pull_requests', 0),
                    'issue_resolutions': contribution_analysis['metrics'].get('issue_resolutions', 0),
                    'code_reviews': contribution_analysis['metrics'].get('code_reviews', 0),
                    'active_days': activity_analysis['metrics'].get('active_days', 0),
                    'activity_consistency': activity_analysis['metrics'].get('activity_consistency', 0.0)
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing time window {window_name}: {str(e)}")
            return None

    def _analyze_code_commits(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析代码提交

        Args:
            window_data: 时间窗口内的数据

        Returns:
            代码提交分析结果
        """
        try:
            # 提取代码提交指标
            total_commits = window_data.get('total_commits', 0)
            commit_frequency = window_data.get('commit_frequency', 0.0)
            commit_days = window_data.get('commit_days', 0)
            average_commit_size = window_data.get('average_commit_size', 0)

            # 计算代码提交评分
            commit_score = min(1.0, total_commits / 100)  # 假设100次提交为满分
            frequency_score = min(1.0, commit_frequency * 7)  # 假设每天1次提交为满分
            consistency_score = min(1.0, commit_days / 30)  # 假设30天中有20天活跃为满分

            # 计算综合代码提交评分
            overall_commit_score = (
                commit_score * 0.5 +
                frequency_score * 0.3 +
                consistency_score * 0.2
            )

            return {
                'score': overall_commit_score,
                'level': self._get_activity_level(overall_commit_score),
                'metrics': {
                    'total_commits': total_commits,
                    'commit_frequency': commit_frequency,
                    'commit_days': commit_days,
                    'average_commit_size': average_commit_size
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing code commits: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_repository_activity(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析仓库活动

        Args:
            window_data: 时间窗口内的数据

        Returns:
            仓库活动分析结果
        """
        try:
            # 提取仓库活动指标
            active_repositories = window_data.get('active_repositories', 0)
            total_repositories = window_data.get('total_repositories', 1)
            repository_contribution_ratio = window_data.get('repository_contribution_ratio', 0.0)
            top_repository_commits = window_data.get('top_repository_commits', 0)

            # 计算仓库活动评分
            repository_score = min(1.0, active_repositories / 10)  # 假设10个活跃仓库为满分
            contribution_ratio_score = repository_contribution_ratio  # 贡献比例直接作为分数
            diversity_score = min(1.0, active_repositories / total_repositories)  # 仓库多样性评分

            # 计算综合仓库活动评分
            overall_repository_score = (
                repository_score * 0.4 +
                contribution_ratio_score * 0.4 +
                diversity_score * 0.2
            )

            return {
                'score': overall_repository_score,
                'level': self._get_activity_level(overall_repository_score),
                'metrics': {
                    'active_repositories': active_repositories,
                    'total_repositories': total_repositories,
                    'repository_contribution_ratio': repository_contribution_ratio,
                    'top_repository_commits': top_repository_commits
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing repository activity: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_contributions(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析贡献

        Args:
            window_data: 时间窗口内的数据

        Returns:
            贡献分析结果
        """
        try:
            # 提取贡献指标
            pull_requests = window_data.get('pull_requests', 0)
            issue_resolutions = window_data.get('issue_resolutions', 0)
            code_reviews = window_data.get('code_reviews', 0)
            merged_pull_requests = window_data.get('merged_pull_requests', 0)

            # 计算贡献评分
            pr_score = min(1.0, pull_requests / 50)  # 假设50个PR为满分
            issue_score = min(1.0, issue_resolutions / 50)  # 假设50个问题解决为满分
            review_score = min(1.0, code_reviews / 30)  # 假设30个代码审查为满分
            merge_score = min(1.0, merged_pull_requests / max(1, pull_requests))  # PR合并率

            # 计算综合贡献评分
            overall_contribution_score = (
                pr_score * 0.4 +
                issue_score * 0.3 +
                review_score * 0.2 +
                merge_score * 0.1
            )

            return {
                'score': overall_contribution_score,
                'level': self._get_activity_level(overall_contribution_score),
                'metrics': {
                    'pull_requests': pull_requests,
                    'issue_resolutions': issue_resolutions,
                    'code_reviews': code_reviews,
                    'merged_pull_requests': merged_pull_requests,
                    'merge_ratio': merged_pull_requests / max(1, pull_requests)
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing contributions: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_activity_patterns(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析活动模式

        Args:
            window_data: 时间窗口内的数据

        Returns:
            活动模式分析结果
        """
        try:
            # 提取活动模式指标
            active_days = window_data.get('active_days', 0)
            activity_consistency = window_data.get('activity_consistency', 0.0)
            peak_activity_time = window_data.get('peak_activity_time', 'unknown')
            activity_streak = window_data.get('activity_streak', 0)

            # 计算活动模式评分
            consistency_score = activity_consistency  # 一致性直接作为分数
            streak_score = min(1.0, activity_streak / 30)  # 假设30天连续活跃为满分
            active_days_score = min(1.0, active_days / 30)  # 假设30天中有20天活跃为满分

            # 计算综合活动模式评分
            overall_activity_score = (
                consistency_score * 0.5 +
                streak_score * 0.3 +
                active_days_score * 0.2
            )

            return {
                'score': overall_activity_score,
                'level': self._get_activity_level(overall_activity_score),
                'metrics': {
                    'active_days': active_days,
                    'activity_consistency': activity_consistency,
                    'peak_activity_time': peak_activity_time,
                    'activity_streak': activity_streak
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing activity patterns: {str(e)}")
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
                '7d': 0.1,
                '30d': 0.4,
                '90d': 0.3,
                '180d': 0.2
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
            recent_windows = ['7d', '30d', '90d']
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
                'average_commits_per_week': 0,
                'average_active_repositories': 0,
                'average_pull_requests': 0,
                'average_issue_resolutions': 0,
                'most_active_period': None,
                'least_active_period': None
            }

            if not time_windows:
                return key_metrics

            # 计算平均指标
            total_commits = 0
            total_repositories = 0
            total_prs = 0
            total_issues = 0
            window_count = len(time_windows)

            for window_data in time_windows.values():
                metrics = window_data.get('metrics', {})
                total_commits += metrics.get('total_commits', 0)
                total_repositories += metrics.get('active_repositories', 0)
                total_prs += metrics.get('pull_requests', 0)
                total_issues += metrics.get('issue_resolutions', 0)

            if window_count > 0:
                key_metrics['average_commits_per_week'] = total_commits / window_count * 7 / 30  # 转换为每周平均
                key_metrics['average_active_repositories'] = total_repositories / window_count
                key_metrics['average_pull_requests'] = total_prs / window_count
                key_metrics['average_issue_resolutions'] = total_issues / window_count

            # 找出最活跃和最不活跃的时期
            window_scores = [(name, data['score']) for name, data in time_windows.items()]
            if window_scores:
                window_scores.sort(key=lambda x: x[1], reverse=True)
                key_metrics['most_active_period'] = window_scores[0][0]
                key_metrics['least_active_period'] = window_scores[-1][0]

            return key_metrics

        except Exception as e:
            self.logger.error(f"Error extracting key metrics: {str(e)}")
            return {}

    def _analyze_top_repositories(self, repository_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分析顶级仓库

        Args:
            repository_data: 仓库数据

        Returns:
            顶级仓库列表
        """
        try:
            repositories = repository_data.get('repositories', [])
            if not repositories:
                return []

            # 按贡献度排序仓库
            sorted_repositories = sorted(
                repositories,
                key=lambda x: x.get('contribution_percentage', 0),
                reverse=True
            )

            # 提取前5个仓库
            top_repos = []
            for repo in sorted_repositories[:5]:
                top_repos.append({
                    'name': repo.get('name'),
                    'contribution_percentage': repo.get('contribution_percentage', 0),
                    'stars': repo.get('stars', 0),
                    'forks': repo.get('forks', 0),
                    'language': repo.get('language', 'Unknown'),
                    'description': repo.get('description', '')
                })

            return top_repos

        except Exception as e:
            self.logger.error(f"Error analyzing top repositories: {str(e)}")
            return []

    def _analyze_skills(self, developer_data: Dict[str, Any], repository_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析技能

        Args:
            developer_data: 开发者基本数据
            repository_data: 仓库数据

        Returns:
            技能分析结果
        """
        try:
            skills = developer_data.get('skills', [])
            repositories = repository_data.get('repositories', [])

            # 从仓库中提取技能
            repo_skills = []
            for repo in repositories:
                language = repo.get('language')
                if language:
                    repo_skills.append(language)

            # 合并技能
            all_skills = skills + repo_skills
            skill_counts = {}
            for skill in all_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1

            # 按频率排序技能
            sorted_skills = sorted(
                skill_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # 提取前10个技能
            top_skills = [skill[0] for skill in sorted_skills[:10]]

            # 分析技能多样性
            skill_diversity = min(1.0, len(top_skills) / 10)

            return {
                'top_skills': top_skills,
                'skill_diversity': skill_diversity,
                'skill_count': len(top_skills),
                'primary_skills': top_skills[:3],
                'secondary_skills': top_skills[3:7],
                'emerging_skills': top_skills[7:]
            }

        except Exception as e:
            self.logger.error(f"Error analyzing skills: {str(e)}")
            return {}

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        生成建议

        Args:
            analysis: 开发者活动分析结果

        Returns:
            建议列表
        """
        try:
            recommendations = []
            overall_score = analysis.get('overall_activity_score', 0)
            trend = analysis.get('activity_trend', 'stable')
            key_metrics = analysis.get('key_metrics', {})
            skills_analysis = analysis.get('skills_analysis', {})

            # 基于总体活跃度评分的建议
            if overall_score < 0.3:
                recommendations.append("开发者活跃度较低，建议关注其最近的工作状态和项目参与情况")
                recommendations.append("建议监控其未来的代码提交和仓库活动")
            elif overall_score > 0.7:
                recommendations.append("开发者活跃度较高，建议关注其专业领域和技术贡献")
                recommendations.append("建议分析其在顶级项目中的角色和影响力")

            # 基于活跃度趋势的建议
            if trend == 'rapidly_increasing':
                recommendations.append("开发者活跃度快速增长，建议关注其新参与的项目和技术方向")
            elif trend == 'rapidly_decreasing':
                recommendations.append("开发者活跃度快速下降，建议分析原因并评估其对项目的影响")

            # 基于关键指标的建议
            if key_metrics.get('average_commits_per_week', 0) < 5:
                recommendations.append("代码提交频率较低，建议关注其工作重点和时间分配")

            if key_metrics.get('average_pull_requests', 0) < 2:
                recommendations.append("PR数量较少，建议关注其代码贡献方式和合作模式")

            # 基于技能分析的建议
            if skills_analysis.get('skill_diversity', 0) < 0.5:
                recommendations.append("技能多样性较低，建议关注其专业深度和技术专注度")

            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def _filter_data_by_time_range(self, repository_data: Dict[str, Any], start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """
        过滤时间范围内的数据

        Args:
            repository_data: 仓库数据
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
                'total_commits': 10 + days_in_window * 2,
                'commit_frequency': min(1.0, (10 + days_in_window * 2) / days_in_window),
                'commit_days': min(days_in_window, 20),
                'average_commit_size': 50 + days_in_window,
                'active_repositories': 2 + days_in_window // 30,
                'total_repositories': 5 + days_in_window // 60,
                'repository_contribution_ratio': 0.3 + (days_in_window / 180) * 0.5,
                'top_repository_commits': 5 + days_in_window,
                'pull_requests': 5 + days_in_window // 7,
                'issue_resolutions': 3 + days_in_window // 10,
                'code_reviews': 2 + days_in_window // 14,
                'merged_pull_requests': 4 + days_in_window // 8,
                'active_days': min(days_in_window, 25),
                'activity_consistency': 0.5 + (days_in_window / 180) * 0.3,
                'peak_activity_time': 'morning',
                'activity_streak': min(days_in_window, 15)
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

    def analyze_multiple_developers(self, developers_data: List[Dict[str, Any]], repository_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分析多个开发者的活动

        Args:
            developers_data: 多个开发者的基本数据
            repository_data: 仓库数据

        Returns:
            多个开发者的活动分析结果
        """
        try:
            analyses = []
            for developer_data in developers_data:
                analysis = self.analyze_developer_activity(developer_data, repository_data)
                if analysis:
                    analyses.append(analysis)

            # 对开发者进行排序
            analyses.sort(key=lambda x: x.get('overall_activity_score', 0), reverse=True)

            return analyses

        except Exception as e:
            self.logger.error(f"Error analyzing multiple developers: {str(e)}")
            return []
