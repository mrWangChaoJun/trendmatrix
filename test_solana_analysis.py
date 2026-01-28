#!/usr/bin/env python3

"""
Solana生态分析功能测试脚本
测试项目活跃度分析、开发者活动分析、NFT市场分析和DeFi协议分析功能
"""

import logging
import sys
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.insert(0, '/Users/mike/Desktop/wcjproject/Mantle/VibeCoding/TrendMatrix')

# 导入测试模块
try:
    from src.solana.core.analyzer.project_activity_analyzer import ProjectActivityAnalyzer
    from src.solana.activity.developer_activity_analyzer import DeveloperActivityAnalyzer
    from src.solana.nft.nft_market_analyzer import NFTMarketAnalyzer
    from src.solana.defi.defi_protocol_analyzer import DeFiProtocolAnalyzer
    logger.info("成功导入所有分析模块")
except ImportError as e:
    logger.error(f"导入模块失败: {e}")
    sys.exit(1)

class SolanaAnalysisTester:
    """
    Solana生态分析功能测试类
    """

    def __init__(self):
        """
        初始化测试类
        """
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0

    def run_all_tests(self):
        """
        运行所有测试
        """
        logger.info("开始测试Solana生态分析功能")
        logger.info(f"测试开始时间: {datetime.now().isoformat()}")

        # 运行各个模块的测试
        self.test_project_activity_analyzer()
        self.test_developer_activity_analyzer()
        self.test_nft_market_analyzer()
        self.test_defi_protocol_analyzer()

        # 输出测试结果
        self.print_test_summary()

    def test_project_activity_analyzer(self):
        """
        测试项目活跃度分析器
        """
        logger.info("\n=== 测试项目活跃度分析器 ===")

        try:
            # 初始化分析器
            analyzer = ProjectActivityAnalyzer()
            self.total_tests += 1
            self.passed_tests += 1
            logger.info("✓ 项目活跃度分析器初始化成功")

            # 准备测试数据
            project_data = {
                'project_id': 'project_1',
                'name': 'Test Project',
                'type': 'DeFi'
            }

            historical_data = {
                'transactions': [],
                'developers': [],
                'community': []
            }

            # 测试分析功能
            result = analyzer.analyze_project_activity(project_data, historical_data)
            self.total_tests += 1

            if result:
                logger.info(f"✓ 项目活跃度分析成功: {result['project_name']}")
                logger.info(f"  总体活跃度评分: {result['overall_activity_score']:.2f}")
                logger.info(f"  活跃度趋势: {result['activity_trend']}")
                logger.info(f"  分析时间窗口数: {len(result['time_windows'])}")
                self.passed_tests += 1
            else:
                logger.error("✗ 项目活跃度分析失败")

            # 测试批量分析功能
            projects_data = [
                project_data,
                {
                    'project_id': 'project_2',
                    'name': 'Another Project',
                    'type': 'NFT'
                }
            ]

            batch_result = analyzer.analyze_multiple_projects(projects_data, historical_data)
            self.total_tests += 1

            if batch_result and len(batch_result) == 2:
                logger.info("✓ 批量项目活跃度分析成功")
                logger.info(f"  分析项目数: {len(batch_result)}")
                logger.info(f"  排名第一的项目: {batch_result[0]['project_name']}")
                self.passed_tests += 1
            else:
                logger.error("✗ 批量项目活跃度分析失败")

        except Exception as e:
            logger.error(f"✗ 测试项目活跃度分析器时出错: {e}")

    def test_developer_activity_analyzer(self):
        """
        测试开发者活动分析器
        """
        logger.info("\n=== 测试开发者活动分析器 ===")

        try:
            # 初始化分析器
            analyzer = DeveloperActivityAnalyzer()
            self.total_tests += 1
            self.passed_tests += 1
            logger.info("✓ 开发者活动分析器初始化成功")

            # 准备测试数据
            developer_data = {
                'developer_id': 'dev_1',
                'name': 'Test Developer',
                'username': 'test_dev',
                'skills': ['Rust', 'TypeScript', 'Solidity']
            }

            repository_data = {
                'repositories': [
                    {
                        'name': 'solana-project',
                        'contribution_percentage': 60,
                        'stars': 1000,
                        'forks': 200,
                        'language': 'Rust',
                        'description': 'A Solana project'
                    },
                    {
                        'name': 'frontend-app',
                        'contribution_percentage': 40,
                        'stars': 500,
                        'forks': 100,
                        'language': 'TypeScript',
                        'description': 'Frontend application'
                    }
                ]
            }

            # 测试分析功能
            result = analyzer.analyze_developer_activity(developer_data, repository_data)
            self.total_tests += 1

            if result:
                logger.info(f"✓ 开发者活动分析成功: {result['developer_name']}")
                logger.info(f"  总体活跃度评分: {result['overall_activity_score']:.2f}")
                logger.info(f"  活跃度趋势: {result['activity_trend']}")
                logger.info(f"  分析时间窗口数: {len(result['time_windows'])}")
                logger.info(f"  顶级技能: {result['skills_analysis']['primary_skills']}")
                self.passed_tests += 1
            else:
                logger.error("✗ 开发者活动分析失败")

            # 测试批量分析功能
            developers_data = [
                developer_data,
                {
                    'developer_id': 'dev_2',
                    'name': 'Another Developer',
                    'username': 'another_dev',
                    'skills': ['Python', 'JavaScript']
                }
            ]

            batch_result = analyzer.analyze_multiple_developers(developers_data, repository_data)
            self.total_tests += 1

            if batch_result and len(batch_result) == 2:
                logger.info("✓ 批量开发者活动分析成功")
                logger.info(f"  分析开发者数: {len(batch_result)}")
                logger.info(f"  排名第一的开发者: {batch_result[0]['developer_name']}")
                self.passed_tests += 1
            else:
                logger.error("✗ 批量开发者活动分析失败")

        except Exception as e:
            logger.error(f"✗ 测试开发者活动分析器时出错: {e}")

    def test_nft_market_analyzer(self):
        """
        测试NFT市场分析器
        """
        logger.info("\n=== 测试NFT市场分析器 ===")

        try:
            # 初始化分析器
            analyzer = NFTMarketAnalyzer()
            self.total_tests += 1
            self.passed_tests += 1
            logger.info("✓ NFT市场分析器初始化成功")

            # 准备测试数据
            collection_data = {
                'collection_id': 'nft_1',
                'name': 'Test Collection',
                'total_supply': 1000
            }

            market_data = {
                'sales': [],
                'prices': [],
                'owners': []
            }

            # 测试分析功能
            result = analyzer.analyze_nft_collection(collection_data, market_data)
            self.total_tests += 1

            if result:
                logger.info(f"✓ NFT集合分析成功: {result['collection_name']}")
                logger.info(f"  总体市场评分: {result['overall_market_score']:.2f}")
                logger.info(f"  市场趋势: {result['market_trend']}")
                logger.info(f"  分析时间窗口数: {len(result['time_windows'])}")
                self.passed_tests += 1
            else:
                logger.error("✗ NFT集合分析失败")

            # 测试批量分析功能
            collections_data = [
                collection_data,
                {
                    'collection_id': 'nft_2',
                    'name': 'Another Collection',
                    'total_supply': 500
                }
            ]

            batch_result = analyzer.analyze_multiple_collections(collections_data, market_data)
            self.total_tests += 1

            if batch_result and len(batch_result) == 2:
                logger.info("✓ 批量NFT集合分析成功")
                logger.info(f"  分析集合数: {len(batch_result)}")
                logger.info(f"  排名第一的集合: {batch_result[0]['collection_name']}")
                self.passed_tests += 1
            else:
                logger.error("✗ 批量NFT集合分析失败")

        except Exception as e:
            logger.error(f"✗ 测试NFT市场分析器时出错: {e}")

    def test_defi_protocol_analyzer(self):
        """
        测试DeFi协议分析器
        """
        logger.info("\n=== 测试DeFi协议分析器 ===")

        try:
            # 初始化分析器
            analyzer = DeFiProtocolAnalyzer()
            self.total_tests += 1
            self.passed_tests += 1
            logger.info("✓ DeFi协议分析器初始化成功")

            # 准备测试数据
            protocol_data = {
                'protocol_id': 'defi_1',
                'name': 'Test Protocol',
                'type': 'AMM'
            }

            market_data = {
                'liquidity': [],
                'yields': [],
                'risks': []
            }

            # 测试分析功能
            result = analyzer.analyze_defi_protocol(protocol_data, market_data)
            self.total_tests += 1

            if result:
                logger.info(f"✓ DeFi协议分析成功: {result['protocol_name']}")
                logger.info(f"  总体评分: {result['overall_score']:.2f}")
                logger.info(f"  趋势: {result['trend']}")
                logger.info(f"  分析时间窗口数: {len(result['time_windows'])}")
                self.passed_tests += 1
            else:
                logger.error("✗ DeFi协议分析失败")

            # 测试批量分析功能
            protocols_data = [
                protocol_data,
                {
                    'protocol_id': 'defi_2',
                    'name': 'Another Protocol',
                    'type': 'Lending'
                }
            ]

            batch_result = analyzer.analyze_multiple_protocols(protocols_data, market_data)
            self.total_tests += 1

            if batch_result and len(batch_result) == 2:
                logger.info("✓ 批量DeFi协议分析成功")
                logger.info(f"  分析协议数: {len(batch_result)}")
                logger.info(f"  排名第一的协议: {batch_result[0]['protocol_name']}")
                self.passed_tests += 1
            else:
                logger.error("✗ 批量DeFi协议分析失败")

        except Exception as e:
            logger.error(f"✗ 测试DeFi协议分析器时出错: {e}")

    def print_test_summary(self):
        """
        打印测试结果摘要
        """
        logger.info("\n=== 测试结果摘要 ===")
        logger.info(f"总测试数: {self.total_tests}")
        logger.info(f"通过测试数: {self.passed_tests}")
        logger.info(f"失败测试数: {self.total_tests - self.passed_tests}")

        if self.total_tests > 0:
            pass_rate = (self.passed_tests / self.total_tests) * 100
            logger.info(f"通过率: {pass_rate:.2f}%")

        if self.passed_tests == self.total_tests:
            logger.info("🎉 所有测试通过！Solana生态分析功能工作正常")
        else:
            logger.warning("⚠️  部分测试失败，需要检查和修复")

        logger.info(f"测试结束时间: {datetime.now().isoformat()}")

if __name__ == "__main__":
    """
    运行测试
    """
    tester = SolanaAnalysisTester()
    tester.run_all_tests()
