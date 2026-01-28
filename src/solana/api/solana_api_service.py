# Solana API Service
# 提供Solana生态分析的外部访问接口

import logging
from typing import Dict, List, Optional, Any

class SolanaAPIService:
    """
    Solana API服务
    提供Solana生态分析的外部访问接口
    """

    def __init__(self, project_analyzer=None, developer_analyzer=None, nft_analyzer=None, defi_analyzer=None, visualizer=None):
        """
        初始化Solana API服务

        Args:
            project_analyzer: 项目活跃度分析器
            developer_analyzer: 开发者活动分析器
            nft_analyzer: NFT市场分析器
            defi_analyzer: DeFi协议分析器
            visualizer: 可视化工具
        """
        self.logger = logging.getLogger(__name__)

        # 依赖服务
        self.project_analyzer = project_analyzer
        self.developer_analyzer = developer_analyzer
        self.nft_analyzer = nft_analyzer
        self.defi_analyzer = defi_analyzer
        self.visualizer = visualizer

        # API版本
        self.api_version = "1.0"

    def analyze_project_activity(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析项目活跃度

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.project_analyzer:
                return self._error_response("Project analyzer not available")

            # 验证请求参数
            if 'project_data' not in request:
                return self._error_response("Missing required parameter: project_data")

            # 分析项目活跃度
            analysis = self.project_analyzer.analyze_project_activity(
                project_data=request['project_data'],
                historical_data=request.get('historical_data', {})
            )

            if not analysis:
                return self._error_response("Failed to analyze project activity")

            return self._success_response(analysis)

        except Exception as e:
            self.logger.error(f"Error analyzing project activity: {str(e)}")
            return self._error_response(str(e))

    def analyze_developer_activity(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析开发者活动

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.developer_analyzer:
                return self._error_response("Developer analyzer not available")

            # 验证请求参数
            if 'developer_data' not in request or 'repository_data' not in request:
                return self._error_response("Missing required parameters: developer_data and repository_data")

            # 分析开发者活动
            analysis = self.developer_analyzer.analyze_developer_activity(
                developer_data=request['developer_data'],
                repository_data=request['repository_data']
            )

            if not analysis:
                return self._error_response("Failed to analyze developer activity")

            return self._success_response(analysis)

        except Exception as e:
            self.logger.error(f"Error analyzing developer activity: {str(e)}")
            return self._error_response(str(e))

    def analyze_nft_collection(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析NFT集合

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.nft_analyzer:
                return self._error_response("NFT analyzer not available")

            # 验证请求参数
            if 'collection_data' not in request:
                return self._error_response("Missing required parameter: collection_data")

            # 分析NFT集合
            analysis = self.nft_analyzer.analyze_nft_collection(
                collection_data=request['collection_data'],
                market_data=request.get('market_data', {})
            )

            if not analysis:
                return self._error_response("Failed to analyze NFT collection")

            return self._success_response(analysis)

        except Exception as e:
            self.logger.error(f"Error analyzing NFT collection: {str(e)}")
            return self._error_response(str(e))

    def analyze_defi_protocol(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析DeFi协议

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.defi_analyzer:
                return self._error_response("DeFi analyzer not available")

            # 验证请求参数
            if 'protocol_data' not in request:
                return self._error_response("Missing required parameter: protocol_data")

            # 分析DeFi协议
            analysis = self.defi_analyzer.analyze_defi_protocol(
                protocol_data=request['protocol_data'],
                market_data=request.get('market_data', {})
            )

            if not analysis:
                return self._error_response("Failed to analyze DeFi protocol")

            return self._success_response(analysis)

        except Exception as e:
            self.logger.error(f"Error analyzing DeFi protocol: {str(e)}")
            return self._error_response(str(e))

    def analyze_multiple_projects(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析多个项目

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.project_analyzer:
                return self._error_response("Project analyzer not available")

            # 验证请求参数
            if 'projects_data' not in request:
                return self._error_response("Missing required parameter: projects_data")

            # 分析多个项目
            analyses = []
            for project_data in request['projects_data']:
                analysis = self.project_analyzer.analyze_project_activity(
                    project_data=project_data,
                    historical_data=request.get('historical_data', {})
                )
                if analysis:
                    analyses.append(analysis)

            if not analyses:
                return self._error_response("Failed to analyze projects")

            return self._success_response(analyses)

        except Exception as e:
            self.logger.error(f"Error analyzing multiple projects: {str(e)}")
            return self._error_response(str(e))

    def visualize_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        可视化分析结果

        Args:
            request: 请求参数

        Returns:
            响应结果
        """
        try:
            if not self.visualizer:
                return self._error_response("Visualizer not available")

            # 验证请求参数
            if 'analysis_result' not in request:
                return self._error_response("Missing required parameter: analysis_result")

            # 确定分析类型并调用相应的可视化方法
            analysis_result = request['analysis_result']
            output_dir = request.get('output_dir')
            generated_files = []

            if 'project_name' in analysis_result:
                # 项目活跃度分析
                generated_files = self.visualizer.visualize_project_activity(analysis_result, output_dir)
            elif 'developer_name' in analysis_result:
                # 开发者活动分析
                generated_files = self.visualizer.visualize_developer_activity(analysis_result, output_dir)
            elif 'collection_name' in analysis_result:
                # NFT市场分析
                generated_files = self.visualizer.visualize_nft_market(analysis_result, output_dir)
            elif 'protocol_name' in analysis_result:
                # DeFi协议分析
                generated_files = self.visualizer.visualize_defi_protocol(analysis_result, output_dir)
            else:
                return self._error_response("Unknown analysis type")

            return self._success_response({"generated_files": generated_files})

        except Exception as e:
            self.logger.error(f"Error visualizing analysis: {str(e)}")
            return self._error_response(str(e))

    def get_service_info(self) -> Dict[str, Any]:
        """
        获取服务信息

        Returns:
            服务信息
        """
        try:
            info = {
                "api_version": self.api_version,
                "services": {
                    "project_analyzer": self.project_analyzer is not None,
                    "developer_analyzer": self.developer_analyzer is not None,
                    "nft_analyzer": self.nft_analyzer is not None,
                    "defi_analyzer": self.defi_analyzer is not None,
                    "visualizer": self.visualizer is not None
                },
                "endpoints": [
                    "/api/solana/analyze-project",
                    "/api/solana/analyze-developer",
                    "/api/solana/analyze-nft",
                    "/api/solana/analyze-defi",
                    "/api/solana/analyze-multiple-projects",
                    "/api/solana/visualize",
                    "/api/solana/service-info"
                ]
            }

            return self._success_response(info)

        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return self._error_response(str(e))

    def _success_response(self, data: Any) -> Dict[str, Any]:
        """
        成功响应

        Args:
            data: 响应数据

        Returns:
            响应对象
        """
        return {
            "success": True,
            "data": data,
            "message": "Operation completed successfully"
        }

    def _error_response(self, message: str) -> Dict[str, Any]:
        """
        错误响应

        Args:
            message: 错误消息

        Returns:
            响应对象
        """
        return {
            "success": False,
            "data": None,
            "message": message
        }
