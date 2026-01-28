#!/usr/bin/env python3

"""
Solana生态数据可视化功能测试脚本
测试项目活跃度、开发者活动、NFT市场和DeFi协议的可视化功能
"""

import logging
import sys
import os
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.insert(0, '/Users/mike/Desktop/wcjproject/Mantle/VibeCoding/TrendMatrix')

# 创建输出目录
output_dir = 'visualization_output'
os.makedirs(output_dir, exist_ok=True)

# 导入测试模块
try:
    from src.solana.core.analyzer.project_activity_analyzer import ProjectActivityAnalyzer
    from src.solana.activity.developer_activity_analyzer import DeveloperActivityAnalyzer
    from src.solana.nft.nft_market_analyzer import NFTMarketAnalyzer
    from src.solana.defi.defi_protocol_analyzer import DeFiProtocolAnalyzer
    from src.solana.visualization.solana_visualizer import SolanaVisualizer
    logger.info("成功导入所有模块")
except ImportError as e:
    logger.error(f"导入模块失败: {e}")
    sys.exit(1)

class SolanaVisualizationTester:
    """
    Solana生态数据可视化功能测试类
    """

    def __init__(self):
        """
        初始化测试类
        """
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.visualizer = SolanaVisualizer()

    def run_all_tests(self):
        """
        运行所有测试
        """
        logger.info("开始测试Solana生态数据可视化功能")
        logger.info(f"测试开始时间: {datetime.now().isoformat()}")
        logger.info(f"输出目录: {output_dir}")

        # 运行各个模块的测试
        self.test_project_activity_visualization()
        self.test_developer_activity_visualization()
        self.test_nft_market_visualization()
        self.test_defi_protocol_visualization()
        self.test_multiple_projects_visualization()
        self.test_ecosystem_overview_visualization()

        # 输出测试结果
        self.print_test_summary()

    def test_project_activity_visualization(self):
        """
        测试项目活跃度可视化
        """
        logger.info("\n=== 测试项目活跃度可视化 ===")

        try:
            # 初始化分析器
            analyzer = ProjectActivityAnalyzer()
            self.total_tests += 1

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

            # 生成分析结果
            analysis_result = analyzer.analyze_project_activity(project_data, historical_data)
            self.total_tests += 1

            if analysis_result:
                # 测试可视化功能
                generated_files = self.visualizer.visualize_project_activity(analysis_result, output_dir)
                self.total_tests += 1

                if generated_files:
                    logger.info(f"✓ 项目活跃度可视化成功")
                    logger.info(f"  生成的图表文件数: {len(generated_files)}")
                    for file in generated_files:
                        logger.info(f"  - {os.path.basename(file)}")
                    self.passed_tests += 3  # 初始化、分析、可视化都通过
                else:
                    logger.error("✗ 项目活跃度可视化失败")
                    self.passed_tests += 2  # 初始化和分析通过，可视化失败
            else:
                logger.error("✗ 项目活跃度分析失败")
                self.passed_tests += 1  # 初始化通过，分析失败

        except Exception as e:
            logger.error(f"✗ 测试项目活跃度可视化时出错: {e}")

    def test_developer_activity_visualization(self):
        """
        测试开发者活动可视化
        """
        logger.info("\n=== 测试开发者活动可视化 ===")

        try:
            # 初始化分析器
            analyzer = DeveloperActivityAnalyzer()
            self.total_tests += 1

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

            # 生成分析结果
            analysis_result = analyzer.analyze_developer_activity(developer_data, repository_data)
            self.total_tests += 1

            if analysis_result:
                # 测试可视化功能
                generated_files = self.visualizer.visualize_developer_activity(analysis_result, output_dir)
                self.total_tests += 1

                if generated_files:
                    logger.info(f"✓ 开发者活动可视化成功")
                    logger.info(f"  生成的图表文件数: {len(generated_files)}")
                    for file in generated_files:
                        logger.info(f"  - {os.path.basename(file)}")
                    self.passed_tests += 3  # 初始化、分析、可视化都通过
                else:
                    logger.error("✗ 开发者活动可视化失败")
                    self.passed_tests += 2  # 初始化和分析通过，可视化失败
            else:
                logger.error("✗ 开发者活动分析失败")
                self.passed_tests += 1  # 初始化通过，分析失败

        except Exception as e:
            logger.error(f"✗ 测试开发者活动可视化时出错: {e}")

    def test_nft_market_visualization(self):
        """
        测试NFT市场可视化
        """
        logger.info("\n=== 测试NFT市场可视化 ===")

        try:
            # 初始化分析器
            analyzer = NFTMarketAnalyzer()
            self.total_tests += 1

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

            # 生成分析结果
            analysis_result = analyzer.analyze_nft_collection(collection_data, market_data)
            self.total_tests += 1

            if analysis_result:
                # 测试可视化功能
                generated_files = self.visualizer.visualize_nft_market(analysis_result, output_dir)
                self.total_tests += 1

                if generated_files:
                    logger.info(f"✓ NFT市场可视化成功")
                    logger.info(f"  生成的图表文件数: {len(generated_files)}")
                    for file in generated_files:
                        logger.info(f"  - {os.path.basename(file)}")
                    self.passed_tests += 3  # 初始化、分析、可视化都通过
                else:
                    logger.error("✗ NFT市场可视化失败")
                    self.passed_tests += 2  # 初始化和分析通过，可视化失败
            else:
                logger.error("✗ NFT市场分析失败")
                self.passed_tests += 1  # 初始化通过，分析失败

        except Exception as e:
            logger.error(f"✗ 测试NFT市场可视化时出错: {e}")

    def test_defi_protocol_visualization(self):
        """
        测试DeFi协议可视化
        """
        logger.info("\n=== 测试DeFi协议可视化 ===")

        try:
            # 初始化分析器
            analyzer = DeFiProtocolAnalyzer()
            self.total_tests += 1

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

            # 生成分析结果
            analysis_result = analyzer.analyze_defi_protocol(protocol_data, market_data)
            self.total_tests += 1

            if analysis_result:
                # 测试可视化功能
                generated_files = self.visualizer.visualize_defi_protocol(analysis_result, output_dir)
                self.total_tests += 1

                if generated_files:
                    logger.info(f"✓ DeFi协议可视化成功")
                    logger.info(f"  生成的图表文件数: {len(generated_files)}")
                    for file in generated_files:
                        logger.info(f"  - {os.path.basename(file)}")
                    self.passed_tests += 3  # 初始化、分析、可视化都通过
                else:
                    logger.error("✗ DeFi协议可视化失败")
                    self.passed_tests += 2  # 初始化和分析通过，可视化失败
            else:
                logger.error("✗ DeFi协议分析失败")
                self.passed_tests += 1  # 初始化通过，分析失败

        except Exception as e:
            logger.error(f"✗ 测试DeFi协议可视化时出错: {e}")

    def test_multiple_projects_visualization(self):
        """
        测试多个项目可视化
        """
        logger.info("\n=== 测试多个项目可视化 ===")

        try:
            # 初始化分析器
            analyzer = ProjectActivityAnalyzer()
            self.total_tests += 1

            # 准备测试数据
            projects_data = [
                {
                    'project_id': 'project_1',
                    'name': 'Test Project 1',
                    'type': 'DeFi'
                },
                {
                    'project_id': 'project_2',
                    'name': 'Test Project 2',
                    'type': 'NFT'
                },
                {
                    'project_id': 'project_3',
                    'name': 'Test Project 3',
                    'type': 'Social'
                }
            ]

            historical_data = {
                'transactions': [],
                'developers': [],
                'community': []
            }

            # 生成多个项目的分析结果
            analyses = []
            for project_data in projects_data:
                analysis = analyzer.analyze_project_activity(project_data, historical_data)
                if analysis:
                    analyses.append(analysis)
            self.total_tests += 1

            if len(analyses) > 1:
                # 测试可视化功能
                generated_files = self.visualizer.visualize_multiple_projects(analyses, output_dir)
                self.total_tests += 1

                if generated_files:
                    logger.info(f"✓ 多个项目可视化成功")
                    logger.info(f"  生成的图表文件数: {len(generated_files)}")
                    for file in generated_files:
                        logger.info(f"  - {os.path.basename(file)}")
                    self.passed_tests += 3  # 初始化、分析、可视化都通过
                else:
                    logger.error("✗ 多个项目可视化失败")
                    self.passed_tests += 2  # 初始化和分析通过，可视化失败
            else:
                logger.error("✗ 多个项目分析失败")
                self.passed_tests += 1  # 初始化通过，分析失败

        except Exception as e:
            logger.error(f"✗ 测试多个项目可视化时出错: {e}")

    def test_ecosystem_overview_visualization(self):
        """
        测试生态系统概览可视化
        """
        logger.info("\n=== 测试生态系统概览可视化 ===")

        try:
            # 初始化分析器
            project_analyzer = ProjectActivityAnalyzer()
            developer_analyzer = DeveloperActivityAnalyzer()
            nft_analyzer = NFTMarketAnalyzer()
            defi_analyzer = DeFiProtocolAnalyzer()
            self.total_tests += 1

            # 准备测试数据
            project_data = {
                'project_id': 'project_1',
                'name': 'Test Project',
                'type': 'DeFi'
            }

            developer_data = {
                'developer_id': 'dev_1',
                'name': 'Test Developer',
                'username': 'test_dev',
                'skills': ['Rust', 'TypeScript', 'Solidity']
            }

            collection_data = {
                'collection_id': 'nft_1',
                'name': 'Test Collection',
                'total_supply': 1000
            }

            protocol_data = {
                'protocol_id': 'defi_1',
                'name': 'Test Protocol',
                'type': 'AMM'
            }

            historical_data = {
                'transactions': [],
                'developers': [],
                'community': []
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
                    }
                ]
            }

            market_data = {
                'sales': [],
                'prices': [],
                'owners': []
            }

            # 生成分析结果
            project_analyses = [project_analyzer.analyze_project_activity(project_data, historical_data)]
            developer_analyses = [developer_analyzer.analyze_developer_activity(developer_data, repository_data)]
            nft_analyses = [nft_analyzer.analyze_nft_collection(collection_data, market_data)]
            defi_analyses = [defi_analyzer.analyze_defi_protocol(protocol_data, market_data)]
            self.total_tests += 1

            # 过滤None结果
            project_analyses = [a for a in project_analyses if a]
            developer_analyses = [a for a in developer_analyses if a]
            nft_analyses = [a for a in nft_analyses if a]
            defi_analyses = [a for a in defi_analyses if a]

            if project_analyses and developer_analyses and nft_analyses and defi_analyses:
                # 测试可视化功能
                generated_files = self.visualizer.visualize_ecosystem_overview(
                    project_analyses, developer_analyses, nft_analyses, defi_analyses, output_dir
                )
                self.total_tests += 1

                if generated_files:
                    logger.info(f"✓ 生态系统概览可视化成功")
                    logger.info(f"  生成的图表文件数: {len(generated_files)}")
                    for file in generated_files:
                        logger.info(f"  - {os.path.basename(file)}")
                    self.passed_tests += 3  # 初始化、分析、可视化都通过
                else:
                    logger.error("✗ 生态系统概览可视化失败")
                    self.passed_tests += 2  # 初始化和分析通过，可视化失败
            else:
                logger.error("✗ 生态系统概览分析失败")
                self.passed_tests += 1  # 初始化通过，分析失败

        except Exception as e:
            logger.error(f"✗ 测试生态系统概览可视化时出错: {e}")

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
            logger.info("🎉 所有测试通过！Solana生态数据可视化功能工作正常")
        else:
            logger.warning("⚠️  部分测试失败，需要检查和修复")

        logger.info(f"测试结束时间: {datetime.now().isoformat()}")
        logger.info(f"生成的图表文件保存在: {output_dir}")

if __name__ == "__main__":
    """
    运行测试
    """
    tester = SolanaVisualizationTester()
    tester.run_all_tests()
