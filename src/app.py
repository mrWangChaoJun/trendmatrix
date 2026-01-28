# Main Application
# 主应用入口，初始化和启动所有服务

import logging
import sys
from api.main_api_service import MainAPIService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('trendmatrix.log')
    ]
)

class TrendMatrixApp:
    """
    TrendMatrix 主应用
    初始化和管理所有服务
    """

    def __init__(self):
        """
        初始化主应用
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing TrendMatrix application...")

        # 服务实例
        self.main_api_service = None

        # 初始化服务
        self._initialize_services()

    def _initialize_services(self):
        """
        初始化所有服务
        """
        try:
            # 延迟导入，避免启动时的依赖问题
            from signals.api.api_service import APIService as SignalsAPIService
            from solana.api.solana_api_service import SolanaAPIService
            from solana.core.analyzer.project_activity_analyzer import ProjectActivityAnalyzer
            from solana.activity.developer_activity_analyzer import DeveloperActivityAnalyzer
            from solana.nft.nft_market_analyzer import NFTMarketAnalyzer
            from solana.defi.defi_protocol_analyzer import DeFiProtocolAnalyzer
            from solana.visualization.solana_visualizer import SolanaVisualizer

            # 初始化Solana分析器
            self.logger.info("Initializing Solana analyzers...")
            project_analyzer = ProjectActivityAnalyzer()
            developer_analyzer = DeveloperActivityAnalyzer()
            nft_analyzer = NFTMarketAnalyzer()
            defi_analyzer = DeFiProtocolAnalyzer()
            visualizer = SolanaVisualizer()

            # 初始化Solana API服务
            self.logger.info("Initializing Solana API service...")
            solana_api_service = SolanaAPIService(
                project_analyzer=project_analyzer,
                developer_analyzer=developer_analyzer,
                nft_analyzer=nft_analyzer,
                defi_analyzer=defi_analyzer,
                visualizer=visualizer
            )

            # 初始化信号系统组件
            self.logger.info("Initializing Signals API service...")
            from signals.core.generator.signal_generator import SignalGenerator
            from signals.core.evaluator.signal_evaluator import SignalEvaluator
            from signals.core.classifier.signal_classifier import SignalClassifier
            from signals.notification.notification_service import NotificationService
            from signals.history.history_service import HistoryService

            # 初始化信号系统组件
            signal_generator = SignalGenerator()
            signal_evaluator = SignalEvaluator()
            signal_classifier = SignalClassifier()
            notification_service = NotificationService()
            history_service = HistoryService()

            # 初始化信号系统API服务
            signals_api_service = SignalsAPIService(
                signal_generator=signal_generator,
                signal_evaluator=signal_evaluator,
                signal_classifier=signal_classifier,
                notification_service=notification_service,
                history_service=history_service
            )

            # 初始化主API服务
            self.logger.info("Initializing Main API service...")
            self.main_api_service = MainAPIService(
                signals_api_service=signals_api_service,
                solana_api_service=solana_api_service
            )

            self.logger.info("All services initialized successfully")

        except ImportError as e:
            self.logger.error(f"Error importing dependencies: {str(e)}")
            self.logger.warning("Some services may not be available")
        except Exception as e:
            self.logger.error(f"Error initializing services: {str(e)}")

    def get_main_api_service(self):
        """
        获取主API服务实例

        Returns:
            主API服务实例
        """
        return self.main_api_service

    def run(self):
        """
        运行应用
        """
        try:
            self.logger.info("Starting TrendMatrix application...")

            # 打印服务信息
            if self.main_api_service:
                service_info = self.main_api_service.get_service_info()
                self.logger.info(f"Service info: {service_info}")
                print("\nTrendMatrix Application Started")
                print("================================")
                print(f"API Version: {service_info.get('data', {}).get('api_version', 'N/A')}")
                print("Available Services:")
                for service, available in service_info.get('data', {}).get('services', {}).items():
                    status = "✓" if available else "✗"
                    print(f"  {service}: {status}")
                print("\nAvailable Endpoints:")
                for endpoint in service_info.get('data', {}).get('endpoints', []):
                    print(f"  - {endpoint}")
                print("\nApplication ready for requests")
            else:
                self.logger.error("Main API service not initialized")
                print("Error: Main API service not initialized")

        except Exception as e:
            self.logger.error(f"Error running application: {str(e)}")
            print(f"Error running application: {str(e)}")

    def test_solana_integration(self):
        """
        测试Solana集成功能
        """
        try:
            self.logger.info("Testing Solana integration...")

            if not self.main_api_service:
                self.logger.error("Main API service not available")
                return False

            # 测试Solana项目分析
            test_project_data = {
                "project_id": "test-project-1",
                "name": "Test Project"
            }

            test_historical_data = {
                "transaction_count": 1000,
                "unique_addresses": 100,
                "volume": 1000000,
                "tvl": 5000000,
                "new_holders": 50,
                "code_commits": 20,
                "active_developers": 3,
                "pull_requests": 10,
                "issue_resolutions": 8,
                "community_interactions": 500,
                "social_media_mentions": 200,
                "sentiment_score": 0.2
            }

            # 测试分析功能
            analysis_result = self.main_api_service.analyze_solana_project({
                "project_data": test_project_data,
                "historical_data": test_historical_data
            })

            self.logger.info(f"Solana project analysis result: {analysis_result}")
            print("\nSolana Integration Test")
            print("======================")
            print(f"Analysis Success: {analysis_result.get('success')}")
            if analysis_result.get('success'):
                data = analysis_result.get('data', {})
                print(f"Project Name: {data.get('project_name')}")
                print(f"Total Score: {data.get('total_score')}")
                print(f"Confidence: {data.get('confidence')}%")
                print("Metrics:")
                for metric, value in data.get('metrics', {}).items():
                    print(f"  {metric}: {value}")

            # 测试集成分析功能
            integration_result = self.main_api_service.analyze_ecosystem_with_signals({
                "solana_data": test_project_data,
                "historical_data": test_historical_data
            })

            self.logger.info(f"Ecosystem analysis with signals result: {integration_result}")
            print("\nEcosystem Analysis with Signals Test")
            print("====================================")
            print(f"Integration Success: {integration_result.get('success')}")
            if integration_result.get('success'):
                data = integration_result.get('data', {})
                print(f"Signal Generated: {data.get('signal_status')}")
                if data.get('signal'):
                    print(f"Signal Asset: {data.get('signal', {}).get('asset')}")
                    print(f"Signal Strength: {data.get('signal', {}).get('strength')}")
                    print(f"Signal Confidence: {data.get('signal', {}).get('confidence')}%")

            return True

        except Exception as e:
            self.logger.error(f"Error testing Solana integration: {str(e)}")
            print(f"Error testing Solana integration: {str(e)}")
            return False

if __name__ == "__main__":
    # 运行主应用
    app = TrendMatrixApp()
    app.run()

    # 测试Solana集成
    app.test_solana_integration()
