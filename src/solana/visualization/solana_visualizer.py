# Solana生态数据可视化工具类
# 专门用于处理Solana生态分析结果的可视化

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from .base_visualizer import BaseVisualizer

class SolanaVisualizer(BaseVisualizer):
    """
    Solana生态数据可视化工具类
    专门用于处理Solana生态分析结果的可视化
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化Solana可视化工具

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.logger = logging.getLogger(__name__)

    def visualize_project_activity(self, analysis_result: Dict[str, Any], 
                                  output_dir: Optional[str] = None) -> List[str]:
        """
        可视化项目活跃度分析结果

        Args:
            analysis_result: 项目活跃度分析结果
            output_dir: 输出目录

        Returns:
            生成的图表文件列表
        """
        try:
            generated_files = []
            project_name = analysis_result.get('project_name', 'Unknown Project')

            # 1. 时间窗口活跃度趋势图
            time_windows = analysis_result.get('time_windows', {})
            if time_windows:
                window_names = list(time_windows.keys())
                window_scores = [window['score'] for window in time_windows.values()]
                on_chain_activity = [window['on_chain_activity']['score'] for window in time_windows.values()]
                developer_activity = [window['developer_activity']['score'] for window in time_windows.values()]
                community_engagement = [window['community_engagement']['score'] for window in time_windows.values()]

                data = {
                    'Overall Score': window_scores,
                    'On-Chain Activity': on_chain_activity,
                    'Developer Activity': developer_activity,
                    'Community Engagement': community_engagement
                }

                output_path = f"{output_dir}/project_activity_{project_name}_trend.png" if output_dir else None
                fig = self.create_time_series_chart(data, window_names, 
                                                  f"{project_name} Activity Trends", 
                                                  "Score", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 2. 关键指标柱状图
            key_metrics = analysis_result.get('key_metrics', {})
            if key_metrics:
                metrics_data = {
                    'Avg Transactions': key_metrics.get('average_transaction_count', 0),
                    'Avg Unique Addresses': key_metrics.get('average_unique_addresses', 0),
                    'Avg Volume': key_metrics.get('average_volume', 0),
                    'Avg TVL': key_metrics.get('average_tvl', 0),
                    'Avg Code Commits': key_metrics.get('average_code_commits', 0)
                }

                output_path = f"{output_dir}/project_activity_{project_name}_metrics.png" if output_dir else None
                fig = self.create_bar_chart(metrics_data, 
                                          f"{project_name} Key Metrics", 
                                          "Metric", "Value", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 3. 活跃度等级饼图
            if time_windows:
                activity_levels = {}
                for window in time_windows.values():
                    level = window['activity_level']
                    activity_levels[level] = activity_levels.get(level, 0) + 1

                output_path = f"{output_dir}/project_activity_{project_name}_levels.png" if output_dir else None
                fig = self.create_pie_chart(activity_levels, 
                                          f"{project_name} Activity Levels Distribution", 
                                          output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            return generated_files

        except Exception as e:
            self.logger.error(f"可视化项目活跃度失败: {str(e)}")
            return []

    def visualize_developer_activity(self, analysis_result: Dict[str, Any], 
                                    output_dir: Optional[str] = None) -> List[str]:
        """
        可视化开发者活动分析结果

        Args:
            analysis_result: 开发者活动分析结果
            output_dir: 输出目录

        Returns:
            生成的图表文件列表
        """
        try:
            generated_files = []
            developer_name = analysis_result.get('developer_name', 'Unknown Developer')

            # 1. 时间窗口活跃度趋势图
            time_windows = analysis_result.get('time_windows', {})
            if time_windows:
                window_names = list(time_windows.keys())
                window_scores = [window['score'] for window in time_windows.values()]
                code_commits = [window['code_commits']['score'] for window in time_windows.values()]
                repository_activity = [window['repository_activity']['score'] for window in time_windows.values()]
                contributions = [window['contributions']['score'] for window in time_windows.values()]
                activity_patterns = [window['activity_patterns']['score'] for window in time_windows.values()]

                data = {
                    'Overall Score': window_scores,
                    'Code Commits': code_commits,
                    'Repository Activity': repository_activity,
                    'Contributions': contributions,
                    'Activity Patterns': activity_patterns
                }

                output_path = f"{output_dir}/developer_activity_{developer_name}_trend.png" if output_dir else None
                fig = self.create_time_series_chart(data, window_names, 
                                                  f"{developer_name} Activity Trends", 
                                                  "Score", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 2. 技能分析饼图
            skills_analysis = analysis_result.get('skills_analysis', {})
            if skills_analysis:
                top_skills = skills_analysis.get('top_skills', [])
                if top_skills:
                    skills_data = {skill: 1 for skill in top_skills[:8]}  # 只取前8个技能
                    output_path = f"{output_dir}/developer_activity_{developer_name}_skills.png" if output_dir else None
                    fig = self.create_pie_chart(skills_data, 
                                              f"{developer_name} Top Skills", 
                                              output_path)
                    if output_path and fig:
                        generated_files.append(output_path)

            # 3. 关键指标柱状图
            key_metrics = analysis_result.get('key_metrics', {})
            if key_metrics:
                metrics_data = {
                    'Avg Commits/Week': key_metrics.get('average_commits_per_week', 0),
                    'Avg Active Repos': key_metrics.get('average_active_repositories', 0),
                    'Avg Pull Requests': key_metrics.get('average_pull_requests', 0),
                    'Avg Issue Resolutions': key_metrics.get('average_issue_resolutions', 0)
                }

                output_path = f"{output_dir}/developer_activity_{developer_name}_metrics.png" if output_dir else None
                fig = self.create_bar_chart(metrics_data, 
                                          f"{developer_name} Key Metrics", 
                                          "Metric", "Value", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            return generated_files

        except Exception as e:
            self.logger.error(f"可视化开发者活动失败: {str(e)}")
            return []

    def visualize_nft_market(self, analysis_result: Dict[str, Any], 
                            output_dir: Optional[str] = None) -> List[str]:
        """
        可视化NFT市场分析结果

        Args:
            analysis_result: NFT市场分析结果
            output_dir: 输出目录

        Returns:
            生成的图表文件列表
        """
        try:
            generated_files = []
            collection_name = analysis_result.get('collection_name', 'Unknown Collection')

            # 1. 时间窗口市场表现趋势图
            time_windows = analysis_result.get('time_windows', {})
            if time_windows:
                window_names = list(time_windows.keys())
                window_scores = [window['score'] for window in time_windows.values()]
                floor_prices = [window['metrics'].get('floor_price', 0) for window in time_windows.values()]
                volumes = [window['metrics'].get('volume', 0) for window in time_windows.values()]
                sales_counts = [window['metrics'].get('sales_count', 0) for window in time_windows.values()]

                data = {
                    'Market Score': window_scores,
                    'Floor Price': floor_prices,
                    'Volume': volumes,
                    'Sales Count': sales_counts
                }

                output_path = f"{output_dir}/nft_market_{collection_name}_trend.png" if output_dir else None
                fig = self.create_time_series_chart(data, window_names, 
                                                  f"{collection_name} Market Trends", 
                                                  "Value", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 2. 关键指标柱状图
            key_metrics = analysis_result.get('key_metrics', {})
            if key_metrics:
                metrics_data = {
                    'Avg Floor Price': key_metrics.get('average_floor_price', 0),
                    'Avg Average Price': key_metrics.get('average_average_price', 0),
                    'Avg Volume': key_metrics.get('average_volume', 0),
                    'Avg Sales Count': key_metrics.get('average_sales_count', 0),
                    'Avg Owners Count': key_metrics.get('average_owners_count', 0)
                }

                output_path = f"{output_dir}/nft_market_{collection_name}_metrics.png" if output_dir else None
                fig = self.create_bar_chart(metrics_data, 
                                          f"{collection_name} Key Metrics", 
                                          "Metric", "Value", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 3. 市场分析子图
            if time_windows:
                price_data = analysis_result.get('price_analysis', {})
                volume_data = analysis_result.get('volume_analysis', {})
                sales_data = analysis_result.get('sales_analysis', {})
                ownership_data = analysis_result.get('ownership_analysis', {})

                plots_data = []

                # 价格分析
                if price_data.get('price_data'):
                    price_values = [d['floor_price'] for d in price_data['price_data']]
                    plots_data.append({
                        'type': 'line',
                        'data': {'Floor Price': price_values},
                        'title': 'Price Trend',
                        'x_label': 'Time Window',
                        'y_label': 'Floor Price'
                    })

                # 交易量分析
                if volume_data.get('volume_data'):
                    volume_values = [d['volume'] for d in volume_data['volume_data']]
                    plots_data.append({
                        'type': 'line',
                        'data': {'Volume': volume_values},
                        'title': 'Volume Trend',
                        'x_label': 'Time Window',
                        'y_label': 'Volume'
                    })

                # 销售量分析
                if sales_data.get('sales_data'):
                    sales_values = [d['sales_count'] for d in sales_data['sales_data']]
                    plots_data.append({
                        'type': 'line',
                        'data': {'Sales Count': sales_values},
                        'title': 'Sales Trend',
                        'x_label': 'Time Window',
                        'y_label': 'Sales Count'
                    })

                # 所有权分析
                if ownership_data.get('ownership_data'):
                    owners_values = [d['owners_count'] for d in ownership_data['ownership_data']]
                    plots_data.append({
                        'type': 'line',
                        'data': {'Owners Count': owners_values},
                        'title': 'Ownership Trend',
                        'x_label': 'Time Window',
                        'y_label': 'Owners Count'
                    })

                if plots_data:
                    rows = (len(plots_data) + 1) // 2
                    cols = min(2, len(plots_data))
                    output_path = f"{output_dir}/nft_market_{collection_name}_analysis.png" if output_dir else None
                    fig = self.create_subplots(plots_data, rows, cols, 
                                              f"{collection_name} Market Analysis", output_path)
                    if output_path and fig:
                        generated_files.append(output_path)

            return generated_files

        except Exception as e:
            self.logger.error(f"可视化NFT市场分析失败: {str(e)}")
            return []

    def visualize_defi_protocol(self, analysis_result: Dict[str, Any], 
                               output_dir: Optional[str] = None) -> List[str]:
        """
        可视化DeFi协议分析结果

        Args:
            analysis_result: DeFi协议分析结果
            output_dir: 输出目录

        Returns:
            生成的图表文件列表
        """
        try:
            generated_files = []
            protocol_name = analysis_result.get('protocol_name', 'Unknown Protocol')

            # 1. 时间窗口协议表现趋势图
            time_windows = analysis_result.get('time_windows', {})
            if time_windows:
                window_names = list(time_windows.keys())
                window_scores = [window['score'] for window in time_windows.values()]
                liquidities = [window['liquidity']['score'] for window in time_windows.values()]
                yields = [window['yield']['score'] for window in time_windows.values()]
                risks = [window['risk']['score'] for window in time_windows.values()]
                growths = [window['growth']['score'] for window in time_windows.values()]

                data = {
                    'Protocol Score': window_scores,
                    'Liquidity Score': liquidities,
                    'Yield Score': yields,
                    'Risk Score': risks,
                    'Growth Score': growths
                }

                output_path = f"{output_dir}/defi_protocol_{protocol_name}_trend.png" if output_dir else None
                fig = self.create_time_series_chart(data, window_names, 
                                                  f"{protocol_name} Performance Trends", 
                                                  "Score", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 2. 关键指标柱状图
            key_metrics = analysis_result.get('key_metrics', {})
            if key_metrics:
                metrics_data = {
                    'Total Liquidity': key_metrics.get('average_total_liquidity', 0),
                    'Average APY': key_metrics.get('average_apy', 0) * 100,  # 转换为百分比
                    'Risk Score': key_metrics.get('average_risk_score', 0),
                    'Growth Rate': key_metrics.get('average_growth_rate', 0) * 100,  # 转换为百分比
                    'Avg Transactions': key_metrics.get('average_transaction_count', 0),
                    'Avg Volume': key_metrics.get('average_volume', 0)
                }

                output_path = f"{output_dir}/defi_protocol_{protocol_name}_metrics.png" if output_dir else None
                fig = self.create_bar_chart(metrics_data, 
                                          f"{protocol_name} Key Metrics", 
                                          "Metric", "Value", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            # 3. 风险分析饼图
            risk_analysis = analysis_result.get('risk_analysis', {})
            if risk_analysis:
                risk_data = {
                    'Risk Score': risk_analysis.get('average_risk_score', 0),
                    'Liquidity Risk': risk_analysis.get('average_liquidity_risk', 0),
                    'Smart Contract Risk': risk_analysis.get('average_smart_contract_risk', 0)
                }

                output_path = f"{output_dir}/defi_protocol_{protocol_name}_risk.png" if output_dir else None
                fig = self.create_pie_chart(risk_data, 
                                          f"{protocol_name} Risk Analysis", 
                                          output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            return generated_files

        except Exception as e:
            self.logger.error(f"可视化DeFi协议分析失败: {str(e)}")
            return []

    def visualize_multiple_projects(self, analyses: List[Dict[str, Any]], 
                                   output_dir: Optional[str] = None) -> List[str]:
        """
        可视化多个项目的分析结果

        Args:
            analyses: 多个项目的分析结果
            output_dir: 输出目录

        Returns:
            生成的图表文件列表
        """
        try:
            generated_files = []

            if len(analyses) > 1:
                # 项目活跃度评分对比
                project_scores = {}
                for analysis in analyses:
                    project_name = analysis.get('project_name', 'Unknown')
                    score = analysis.get('overall_activity_score', 0)
                    project_scores[project_name] = score

                output_path = f"{output_dir}/multiple_projects_scores.png" if output_dir else None
                fig = self.create_bar_chart(project_scores, 
                                          "Project Activity Scores Comparison", 
                                          "Project", "Activity Score", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

                # 项目活跃度趋势对比
                if analyses[0].get('time_windows'):
                    window_names = list(analyses[0]['time_windows'].keys())
                    trend_data = {}

                    for analysis in analyses:
                        project_name = analysis.get('project_name', 'Unknown')
                        if analysis.get('time_windows'):
                            scores = [window['score'] for window in analysis['time_windows'].values()]
                            trend_data[project_name] = scores

                    output_path = f"{output_dir}/multiple_projects_trends.png" if output_dir else None
                    fig = self.create_time_series_chart(trend_data, window_names, 
                                                      "Project Activity Trends Comparison", 
                                                      "Activity Score", output_path)
                    if output_path and fig:
                        generated_files.append(output_path)

            return generated_files

        except Exception as e:
            self.logger.error(f"可视化多个项目失败: {str(e)}")
            return []

    def visualize_ecosystem_overview(self, project_analyses: List[Dict[str, Any]], 
                                    developer_analyses: List[Dict[str, Any]], 
                                    nft_analyses: List[Dict[str, Any]], 
                                    defi_analyses: List[Dict[str, Any]], 
                                    output_dir: Optional[str] = None) -> List[str]:
        """
        可视化Solana生态系统概览

        Args:
            project_analyses: 项目活跃度分析结果
            developer_analyses: 开发者活动分析结果
            nft_analyses: NFT市场分析结果
            defi_analyses: DeFi协议分析结果
            output_dir: 输出目录

        Returns:
            生成的图表文件列表
        """
        try:
            generated_files = []

            # 1. 生态系统各部分评分对比
            ecosystem_scores = {}

            if project_analyses:
                avg_project_score = sum(a.get('overall_activity_score', 0) for a in project_analyses) / len(project_analyses)
                ecosystem_scores['Projects'] = avg_project_score

            if developer_analyses:
                avg_dev_score = sum(a.get('overall_activity_score', 0) for a in developer_analyses) / len(developer_analyses)
                ecosystem_scores['Developers'] = avg_dev_score

            if nft_analyses:
                avg_nft_score = sum(a.get('overall_market_score', 0) for a in nft_analyses) / len(nft_analyses)
                ecosystem_scores['NFT Market'] = avg_nft_score

            if defi_analyses:
                avg_defi_score = sum(a.get('overall_score', 0) for a in defi_analyses) / len(defi_analyses)
                ecosystem_scores['DeFi Protocols'] = avg_defi_score

            output_path = f"{output_dir}/ecosystem_overview_scores.png" if output_dir else None
            fig = self.create_bar_chart(ecosystem_scores, 
                                      "Solana Ecosystem Overview", 
                                      "Category", "Average Score", output_path)
            if output_path and fig:
                generated_files.append(output_path)

            # 2. 生态系统概览子图
            plots_data = []

            # 项目活跃度分布
            if project_analyses:
                project_scores = [a.get('overall_activity_score', 0) for a in project_analyses]
                plots_data.append({
                    'type': 'bar',
                    'data': {f'Project {i+1}': score for i, score in enumerate(project_scores[:5])},  # 只取前5个
                    'title': 'Top Project Activity Scores',
                    'x_label': 'Project',
                    'y_label': 'Activity Score'
                })

            # 开发者活跃度分布
            if developer_analyses:
                dev_scores = [a.get('overall_activity_score', 0) for a in developer_analyses]
                plots_data.append({
                    'type': 'bar',
                    'data': {f'Dev {i+1}': score for i, score in enumerate(dev_scores[:5])},  # 只取前5个
                    'title': 'Top Developer Activity Scores',
                    'x_label': 'Developer',
                    'y_label': 'Activity Score'
                })

            # NFT市场表现分布
            if nft_analyses:
                nft_scores = [a.get('overall_market_score', 0) for a in nft_analyses]
                plots_data.append({
                    'type': 'bar',
                    'data': {f'Collection {i+1}': score for i, score in enumerate(nft_scores[:5])},  # 只取前5个
                    'title': 'Top NFT Collection Market Scores',
                    'x_label': 'Collection',
                    'y_label': 'Market Score'
                })

            # DeFi协议表现分布
            if defi_analyses:
                defi_scores = [a.get('overall_score', 0) for a in defi_analyses]
                plots_data.append({
                    'type': 'bar',
                    'data': {f'Protocol {i+1}': score for i, score in enumerate(defi_scores[:5])},  # 只取前5个
                    'title': 'Top DeFi Protocol Scores',
                    'x_label': 'Protocol',
                    'y_label': 'Protocol Score'
                })

            if plots_data:
                rows = (len(plots_data) + 1) // 2
                cols = min(2, len(plots_data))
                output_path = f"{output_dir}/ecosystem_overview_detailed.png" if output_dir else None
                fig = self.create_subplots(plots_data, rows, cols, 
                                          "Solana Ecosystem Detailed Overview", output_path)
                if output_path and fig:
                    generated_files.append(output_path)

            return generated_files

        except Exception as e:
            self.logger.error(f"可视化生态系统概览失败: {str(e)}")
            return []

    def export_analysis_to_csv(self, analysis_result: Dict[str, Any], file_path: str) -> bool:
        """
        导出分析结果到CSV文件

        Args:
            analysis_result: 分析结果
            file_path: 文件路径

        Returns:
            是否导出成功
        """
        try:
            # 准备导出数据
            export_data = {
                'analysis_timestamp': analysis_result.get('analysis_timestamp', datetime.now().isoformat()),
                'name': analysis_result.get('project_name') or analysis_result.get('developer_name') or 
                        analysis_result.get('collection_name') or analysis_result.get('protocol_name') or 'Unknown',
                'overall_score': analysis_result.get('overall_activity_score') or 
                                analysis_result.get('overall_market_score') or 
                                analysis_result.get('overall_score') or 0,
                'trend': analysis_result.get('activity_trend') or analysis_result.get('market_trend') or 
                         analysis_result.get('trend') or 'stable'
            }

            # 添加时间窗口数据
            time_windows = analysis_result.get('time_windows', {})
            for window_name, window_data in time_windows.items():
                export_data[f'{window_name}_score'] = window_data.get('score', 0)
                if 'metrics' in window_data:
                    for metric_name, metric_value in window_data['metrics'].items():
                        export_data[f'{window_name}_{metric_name}'] = metric_value

            # 添加关键指标
            key_metrics = analysis_result.get('key_metrics', {})
            for metric_name, metric_value in key_metrics.items():
                export_data[f'key_{metric_name}'] = metric_value

            return self.export_to_csv(export_data, file_path)

        except Exception as e:
            self.logger.error(f"导出分析结果到CSV失败: {str(e)}")
            return False

    def export_analysis_to_json(self, analysis_result: Dict[str, Any], file_path: str) -> bool:
        """
        导出分析结果到JSON文件

        Args:
            analysis_result: 分析结果
            file_path: 文件路径

        Returns:
            是否导出成功
        """
        try:
            return self.export_to_json(analysis_result, file_path)
        except Exception as e:
            self.logger.error(f"导出分析结果到JSON失败: {str(e)}")
            return False
