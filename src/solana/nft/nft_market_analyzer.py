# NFT Market Analyzer

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class NFTMarketAnalyzer:
    """
    NFT 市场分析器
    分析 NFT 市场趋势和集合表现
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 NFT 市场分析器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 分析参数
        self.price_weight = self.config.get('price_weight', 0.3)
        self.volume_weight = self.config.get('volume_weight', 0.3)
        self.sales_weight = self.config.get('sales_weight', 0.2)
        self.ownership_weight = self.config.get('ownership_weight', 0.2)

        # 时间窗口配置
        self.time_windows = {
            '24h': timedelta(hours=24),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '90d': timedelta(days=90)
        }

    def analyze_nft_collection(self, collection_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析 NFT 集合

        Args:
            collection_data: 集合基本数据
            market_data: 市场数据

        Returns:
            集合分析结果
        """
        try:
            # 验证输入数据
            if not collection_data or not market_data:
                self.logger.error("Invalid input data for NFT collection analysis")
                return None

            # 分析结果
            analysis = {
                'collection_id': collection_data.get('collection_id'),
                'collection_name': collection_data.get('name'),
                'analysis_timestamp': datetime.now().isoformat(),
                'time_windows': {},
                'overall_market_score': 0.0,
                'market_trend': 'stable',
                'key_metrics': {},
                'price_analysis': {},
                'volume_analysis': {},
                'sales_analysis': {},
                'ownership_analysis': {},
                'comparative_analysis': {},
                'recommendations': []
            }

            # 分析不同时间窗口的市场表现
            for window_name, window_delta in self.time_windows.items():
                window_analysis = self._analyze_time_window(window_name, window_delta, collection_data, market_data)
                if window_analysis:
                    analysis['time_windows'][window_name] = window_analysis

            # 计算总体市场评分
            analysis['overall_market_score'] = self._calculate_overall_score(analysis['time_windows'])

            # 分析市场趋势
            analysis['market_trend'] = self._analyze_market_trend(analysis['time_windows'])

            # 提取关键指标
            analysis['key_metrics'] = self._extract_key_metrics(analysis['time_windows'])

            # 分析价格
            analysis['price_analysis'] = self._analyze_price(analysis['time_windows'])

            # 分析交易量
            analysis['volume_analysis'] = self._analyze_volume(analysis['time_windows'])

            # 分析销售量
            analysis['sales_analysis'] = self._analyze_sales(analysis['time_windows'])

            # 分析所有权
            analysis['ownership_analysis'] = self._analyze_ownership(analysis['time_windows'])

            # 生成建议
            analysis['recommendations'] = self._generate_recommendations(analysis)

            self.logger.info(f"Analyzed NFT collection: {collection_data.get('name')}")
            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing NFT collection: {str(e)}")
            return None

    def _analyze_time_window(self, window_name: str, window_delta: timedelta, collection_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析特定时间窗口的市场表现

        Args:
            window_name: 时间窗口名称
            window_delta: 时间窗口
            collection_data: 集合基本数据
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

            # 分析价格
            price_analysis = self._analyze_window_price(window_data)

            # 分析交易量
            volume_analysis = self._analyze_window_volume(window_data)

            # 分析销售量
            sales_analysis = self._analyze_window_sales(window_data)

            # 分析所有权
            ownership_analysis = self._analyze_window_ownership(window_data)

            # 计算时间窗口市场评分
            window_score = (
                price_analysis['score'] * self.price_weight +
                volume_analysis['score'] * self.volume_weight +
                sales_analysis['score'] * self.sales_weight +
                ownership_analysis['score'] * self.ownership_weight
            )

            # 确定市场表现等级
            market_level = self._get_market_level(window_score)

            return {
                'window_name': window_name,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'score': window_score,
                'market_level': market_level,
                'price': price_analysis,
                'volume': volume_analysis,
                'sales': sales_analysis,
                'ownership': ownership_analysis,
                'metrics': {
                    'floor_price': price_analysis['metrics'].get('floor_price', 0),
                    'average_price': price_analysis['metrics'].get('average_price', 0),
                    'price_change': price_analysis['metrics'].get('price_change', 0.0),
                    'volume': volume_analysis['metrics'].get('volume', 0),
                    'volume_change': volume_analysis['metrics'].get('volume_change', 0.0),
                    'sales_count': sales_analysis['metrics'].get('sales_count', 0),
                    'sales_change': sales_analysis['metrics'].get('sales_change', 0.0),
                    'owners_count': ownership_analysis['metrics'].get('owners_count', 0),
                    'unique_owners': ownership_analysis['metrics'].get('unique_owners', 0),
                    'ownership_concentration': ownership_analysis['metrics'].get('ownership_concentration', 0.0)
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing time window {window_name}: {str(e)}")
            return None

    def _analyze_window_price(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的价格

        Args:
            window_data: 时间窗口内的数据

        Returns:
            价格分析结果
        """
        try:
            # 提取价格指标
            floor_price = window_data.get('floor_price', 0)
            average_price = window_data.get('average_price', 0)
            price_change = window_data.get('price_change', 0.0)
            price_volatility = window_data.get('price_volatility', 0.0)

            # 计算价格评分
            # 这里使用相对评分，实际应用中可以根据市场基准进行调整
            floor_price_score = min(1.0, floor_price / 10000)  # 假设10000 SOL为满分
            average_price_score = min(1.0, average_price / 20000)  # 假设20000 SOL为满分
            price_change_score = min(1.0, max(0.0, (price_change + 1) / 2))  # 将价格变化从[-1,1]归一化到[0,1]
            volatility_score = min(1.0, 1 - price_volatility)  # 波动率越低评分越高

            # 计算综合价格评分
            overall_price_score = (
                floor_price_score * 0.3 +
                average_price_score * 0.3 +
                price_change_score * 0.3 +
                volatility_score * 0.1
            )

            return {
                'score': overall_price_score,
                'level': self._get_market_level(overall_price_score),
                'metrics': {
                    'floor_price': floor_price,
                    'average_price': average_price,
                    'price_change': price_change,
                    'price_volatility': price_volatility
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window price: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_window_volume(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的交易量

        Args:
            window_data: 时间窗口内的数据

        Returns:
            交易量分析结果
        """
        try:
            # 提取交易量指标
            volume = window_data.get('volume', 0)
            volume_change = window_data.get('volume_change', 0.0)
            average_daily_volume = window_data.get('average_daily_volume', 0)
            volume_volatility = window_data.get('volume_volatility', 0.0)

            # 计算交易量评分
            volume_score = min(1.0, volume / 100000)  # 假设100000 SOL为满分
            volume_change_score = min(1.0, max(0.0, (volume_change + 1) / 2))  # 将交易量变化从[-1,1]归一化到[0,1]
            consistency_score = min(1.0, 1 - volume_volatility)  # 交易量越稳定评分越高

            # 计算综合交易量评分
            overall_volume_score = (
                volume_score * 0.5 +
                volume_change_score * 0.3 +
                consistency_score * 0.2
            )

            return {
                'score': overall_volume_score,
                'level': self._get_market_level(overall_volume_score),
                'metrics': {
                    'volume': volume,
                    'volume_change': volume_change,
                    'average_daily_volume': average_daily_volume,
                    'volume_volatility': volume_volatility
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window volume: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_window_sales(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的销售量

        Args:
            window_data: 时间窗口内的数据

        Returns:
            销售量分析结果
        """
        try:
            # 提取销售量指标
            sales_count = window_data.get('sales_count', 0)
            sales_change = window_data.get('sales_change', 0.0)
            average_daily_sales = window_data.get('average_daily_sales', 0)
            sales_volatility = window_data.get('sales_volatility', 0.0)

            # 计算销售量评分
            sales_count_score = min(1.0, sales_count / 1000)  # 假设1000笔销售为满分
            sales_change_score = min(1.0, max(0.0, (sales_change + 1) / 2))  # 将销售量变化从[-1,1]归一化到[0,1]
            consistency_score = min(1.0, 1 - sales_volatility)  # 销售量越稳定评分越高

            # 计算综合销售量评分
            overall_sales_score = (
                sales_count_score * 0.5 +
                sales_change_score * 0.3 +
                consistency_score * 0.2
            )

            return {
                'score': overall_sales_score,
                'level': self._get_market_level(overall_sales_score),
                'metrics': {
                    'sales_count': sales_count,
                    'sales_change': sales_change,
                    'average_daily_sales': average_daily_sales,
                    'sales_volatility': sales_volatility
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window sales: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _analyze_window_ownership(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析时间窗口内的所有权

        Args:
            window_data: 时间窗口内的数据

        Returns:
            所有权分析结果
        """
        try:
            # 提取所有权指标
            owners_count = window_data.get('owners_count', 0)
            unique_owners = window_data.get('unique_owners', 0)
            ownership_concentration = window_data.get('ownership_concentration', 0.0)
            new_owners = window_data.get('new_owners', 0)

            # 计算所有权评分
            owners_count_score = min(1.0, owners_count / 1000)  # 假设1000个持有者为满分
            unique_owners_score = min(1.0, unique_owners / 1000)  # 假设1000个唯一持有者为满分
            concentration_score = min(1.0, 1 - ownership_concentration)  # 集中度越低评分越高
            new_owners_score = min(1.0, new_owners / 100)  # 假设100个新持有者为满分

            # 计算综合所有权评分
            overall_ownership_score = (
                owners_count_score * 0.3 +
                unique_owners_score * 0.3 +
                concentration_score * 0.2 +
                new_owners_score * 0.2
            )

            return {
                'score': overall_ownership_score,
                'level': self._get_market_level(overall_ownership_score),
                'metrics': {
                    'owners_count': owners_count,
                    'unique_owners': unique_owners,
                    'ownership_concentration': ownership_concentration,
                    'new_owners': new_owners
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing window ownership: {str(e)}")
            return {'score': 0.0, 'level': 'low', 'metrics': {}}

    def _calculate_overall_score(self, time_windows: Dict[str, Any]) -> float:
        """
        计算总体市场评分

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            总体市场评分
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

    def _analyze_market_trend(self, time_windows: Dict[str, Any]) -> str:
        """
        分析市场趋势

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            市场趋势
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
            self.logger.error(f"Error analyzing market trend: {str(e)}")
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
                'average_floor_price': 0,
                'average_average_price': 0,
                'average_volume': 0,
                'average_sales_count': 0,
                'average_owners_count': 0,
                'highest_performing_window': None,
                'lowest_performing_window': None,
                'most_volatile_metric': None,
                'most_stable_metric': None
            }

            if not time_windows:
                return key_metrics

            # 计算平均指标
            total_floor_price = 0
            total_average_price = 0
            total_volume = 0
            total_sales_count = 0
            total_owners_count = 0
            window_count = len(time_windows)

            for window_data in time_windows.values():
                metrics = window_data.get('metrics', {})
                total_floor_price += metrics.get('floor_price', 0)
                total_average_price += metrics.get('average_price', 0)
                total_volume += metrics.get('volume', 0)
                total_sales_count += metrics.get('sales_count', 0)
                total_owners_count += metrics.get('owners_count', 0)

            if window_count > 0:
                key_metrics['average_floor_price'] = total_floor_price / window_count
                key_metrics['average_average_price'] = total_average_price / window_count
                key_metrics['average_volume'] = total_volume / window_count
                key_metrics['average_sales_count'] = total_sales_count / window_count
                key_metrics['average_owners_count'] = total_owners_count / window_count

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

    def _analyze_price(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析价格

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            价格分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取价格数据
            price_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                price_data.append({
                    'window': window_name,
                    'floor_price': metrics.get('floor_price', 0),
                    'average_price': metrics.get('average_price', 0),
                    'price_change': metrics.get('price_change', 0.0)
                })

            # 分析价格趋势
            floor_prices = [d['floor_price'] for d in price_data]
            average_prices = [d['average_price'] for d in price_data]
            price_changes = [d['price_change'] for d in price_data]

            # 计算价格趋势
            floor_price_trend = 'stable'
            if len(floor_prices) >= 2:
                if floor_prices[-1] > floor_prices[0] * 1.1:
                    floor_price_trend = 'rising'
                elif floor_prices[-1] < floor_prices[0] * 0.9:
                    floor_price_trend = 'falling'

            average_price_trend = 'stable'
            if len(average_prices) >= 2:
                if average_prices[-1] > average_prices[0] * 1.1:
                    average_price_trend = 'rising'
                elif average_prices[-1] < average_prices[0] * 0.9:
                    average_price_trend = 'falling'

            # 计算价格波动性
            price_volatility = 0.0
            if len(price_changes) > 1:
                import statistics
                price_volatility = statistics.stdev(price_changes) if len(price_changes) > 1 else 0.0

            return {
                'price_data': price_data,
                'floor_price_trend': floor_price_trend,
                'average_price_trend': average_price_trend,
                'price_volatility': price_volatility,
                'price_correlation': 0.0  # 可以计算价格与其他指标的相关性
            }

        except Exception as e:
            self.logger.error(f"Error analyzing price: {str(e)}")
            return {}

    def _analyze_volume(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析交易量

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            交易量分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取交易量数据
            volume_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                volume_data.append({
                    'window': window_name,
                    'volume': metrics.get('volume', 0),
                    'volume_change': metrics.get('volume_change', 0.0)
                })

            # 分析交易量趋势
            volumes = [d['volume'] for d in volume_data]
            volume_changes = [d['volume_change'] for d in volume_data]

            # 计算交易量趋势
            volume_trend = 'stable'
            if len(volumes) >= 2:
                if volumes[-1] > volumes[0] * 1.1:
                    volume_trend = 'increasing'
                elif volumes[-1] < volumes[0] * 0.9:
                    volume_trend = 'decreasing'

            # 计算交易量波动性
            volume_volatility = 0.0
            if len(volume_changes) > 1:
                import statistics
                volume_volatility = statistics.stdev(volume_changes) if len(volume_changes) > 1 else 0.0

            return {
                'volume_data': volume_data,
                'volume_trend': volume_trend,
                'volume_volatility': volume_volatility
            }

        except Exception as e:
            self.logger.error(f"Error analyzing volume: {str(e)}")
            return {}

    def _analyze_sales(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析销售量

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            销售量分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取销售量数据
            sales_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                sales_data.append({
                    'window': window_name,
                    'sales_count': metrics.get('sales_count', 0),
                    'sales_change': metrics.get('sales_change', 0.0)
                })

            # 分析销售量趋势
            sales_counts = [d['sales_count'] for d in sales_data]
            sales_changes = [d['sales_change'] for d in sales_data]

            # 计算销售量趋势
            sales_trend = 'stable'
            if len(sales_counts) >= 2:
                if sales_counts[-1] > sales_counts[0] * 1.1:
                    sales_trend = 'increasing'
                elif sales_counts[-1] < sales_counts[0] * 0.9:
                    sales_trend = 'decreasing'

            # 计算销售量波动性
            sales_volatility = 0.0
            if len(sales_changes) > 1:
                import statistics
                sales_volatility = statistics.stdev(sales_changes) if len(sales_changes) > 1 else 0.0

            return {
                'sales_data': sales_data,
                'sales_trend': sales_trend,
                'sales_volatility': sales_volatility
            }

        except Exception as e:
            self.logger.error(f"Error analyzing sales: {str(e)}")
            return {}

    def _analyze_ownership(self, time_windows: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析所有权

        Args:
            time_windows: 不同时间窗口的分析结果

        Returns:
            所有权分析结果
        """
        try:
            if not time_windows:
                return {}

            # 提取所有权数据
            ownership_data = []
            for window_name, window_data in time_windows.items():
                metrics = window_data.get('metrics', {})
                ownership_data.append({
                    'window': window_name,
                    'owners_count': metrics.get('owners_count', 0),
                    'unique_owners': metrics.get('unique_owners', 0),
                    'ownership_concentration': metrics.get('ownership_concentration', 0.0)
                })

            # 分析所有权趋势
            owners_counts = [d['owners_count'] for d in ownership_data]
            unique_owners = [d['unique_owners'] for d in ownership_data]
            concentrations = [d['ownership_concentration'] for d in ownership_data]

            # 计算所有权趋势
            owners_trend = 'stable'
            if len(owners_counts) >= 2:
                if owners_counts[-1] > owners_counts[0] * 1.1:
                    owners_trend = 'increasing'
                elif owners_counts[-1] < owners_counts[0] * 0.9:
                    owners_trend = 'decreasing'

            # 计算集中度趋势
            concentration_trend = 'stable'
            if len(concentrations) >= 2:
                if concentrations[-1] > concentrations[0] * 1.1:
                    concentration_trend = 'increasing'
                elif concentrations[-1] < concentrations[0] * 0.9:
                    concentration_trend = 'decreasing'

            return {
                'ownership_data': ownership_data,
                'owners_trend': owners_trend,
                'concentration_trend': concentration_trend
            }

        except Exception as e:
            self.logger.error(f"Error analyzing ownership: {str(e)}")
            return {}

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        生成建议

        Args:
            analysis: NFT 集合分析结果

        Returns:
            建议列表
        """
        try:
            recommendations = []
            overall_score = analysis.get('overall_market_score', 0)
            market_trend = analysis.get('market_trend', 'stable')
            key_metrics = analysis.get('key_metrics', {})

            # 基于总体市场评分的建议
            if overall_score < 0.3:
                recommendations.append("集合市场表现较差，建议关注其基本面和社区活跃度")
                recommendations.append("建议监控价格走势和交易量变化，寻找潜在的反转信号")
            elif overall_score > 0.7:
                recommendations.append("集合市场表现较好，建议关注其可持续性和增长潜力")
                recommendations.append("建议分析其与同类集合的比较优势")

            # 基于市场趋势的建议
            if market_trend == 'rapidly_increasing':
                recommendations.append("集合市场表现快速增长，建议关注是否有重大事件或合作")
            elif market_trend == 'rapidly_decreasing':
                recommendations.append("集合市场表现快速下降，建议分析原因并评估投资风险")

            # 基于关键指标的建议
            if key_metrics.get('average_sales_count', 0) < 10:
                recommendations.append("销售量较低，建议关注其流动性和市场需求")

            if key_metrics.get('average_owners_count', 0) < 100:
                recommendations.append("持有者数量较少，建议关注其社区建设和用户获取策略")

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
                'floor_price': 100 + days_in_window * 10,
                'average_price': 200 + days_in_window * 20,
                'price_change': 0.01 * days_in_window,
                'price_volatility': 0.05 + days_in_window * 0.001,
                'volume': 10000 + days_in_window * 1000,
                'volume_change': 0.02 * days_in_window,
                'average_daily_volume': 1000 + days_in_window * 100,
                'volume_volatility': 0.1 + days_in_window * 0.005,
                'sales_count': 50 + days_in_window * 5,
                'sales_change': 0.015 * days_in_window,
                'average_daily_sales': 5 + days_in_window,
                'sales_volatility': 0.15 + days_in_window * 0.01,
                'owners_count': 200 + days_in_window * 10,
                'unique_owners': 150 + days_in_window * 8,
                'ownership_concentration': 0.3 - days_in_window * 0.005,
                'new_owners': 10 + days_in_window * 2
            }

        except Exception as e:
            self.logger.error(f"Error filtering data by time range: {str(e)}")
            return {}

    def _get_market_level(self, score: float) -> str:
        """
        根据评分确定市场表现等级

        Args:
            score: 市场评分

        Returns:
            市场表现等级
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

    def analyze_multiple_collections(self, collections_data: List[Dict[str, Any]], market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分析多个 NFT 集合

        Args:
            collections_data: 多个集合的基本数据
            market_data: 市场数据

        Returns:
            多个集合的分析结果
        """
        try:
            analyses = []
            for collection_data in collections_data:
                analysis = self.analyze_nft_collection(collection_data, market_data)
                if analysis:
                    analyses.append(analysis)

            # 对集合进行排序
            analyses.sort(key=lambda x: x.get('overall_market_score', 0), reverse=True)

            return analyses

        except Exception as e:
            self.logger.error(f"Error analyzing multiple collections: {str(e)}")
            return []
