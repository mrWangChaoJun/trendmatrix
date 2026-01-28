# 基础可视化工具类
# 提供通用的图表生成功能

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# 尝试导入可视化库
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    VISUALIZATION_AVAILABLE = True

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
except ImportError:
    VISUALIZATION_AVAILABLE = False
    plt = None
    sns = None
    pd = None
    np = None
    logging.warning("可视化库未安装，部分功能可能不可用")

class BaseVisualizer:
    """
    基础可视化工具类
    提供通用的图表生成功能
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化可视化工具

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 默认配置
        self.default_style = self.config.get('style', 'seaborn-v0_8')
        self.default_dpi = self.config.get('dpi', 100)
        self.default_figsize = self.config.get('figsize', (12, 6))
        self.default_color_palette = self.config.get('color_palette', 'viridis')

        # 设置默认样式
        if VISUALIZATION_AVAILABLE:
            plt.style.use(self.default_style)
            sns.set_palette(self.default_color_palette)

    def create_line_chart(self, data: Dict[str, Any], title: str, x_label: str, y_label: str,
                         output_path: Optional[str] = None) -> Optional[Any]:
        """
        创建折线图

        Args:
            data: 图表数据
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            output_path: 输出路径

        Returns:
            图表对象
        """
        if not VISUALIZATION_AVAILABLE:
            self.logger.warning("可视化库未安装，无法创建折线图")
            return None

        try:
            fig, ax = plt.subplots(figsize=self.default_figsize, dpi=self.default_dpi)

            # 绘制折线图
            for series_name, series_data in data.items():
                if isinstance(series_data, list) and len(series_data) > 0:
                    x_values = list(range(len(series_data)))
                    ax.plot(x_values, series_data, marker='o', label=series_name)

            # 设置图表属性
            ax.set_title(title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # 调整布局
            plt.tight_layout()

            # 保存图表
            if output_path:
                plt.savefig(output_path)
                self.logger.info(f"折线图已保存到: {output_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建折线图失败: {str(e)}")
            return None

    def create_bar_chart(self, data: Dict[str, Any], title: str, x_label: str, y_label: str,
                        output_path: Optional[str] = None) -> Optional[Any]:
        """
        创建柱状图

        Args:
            data: 图表数据
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            output_path: 输出路径

        Returns:
            图表对象
        """
        if not VISUALIZATION_AVAILABLE:
            self.logger.warning("可视化库未安装，无法创建柱状图")
            return None

        try:
            fig, ax = plt.subplots(figsize=self.default_figsize, dpi=self.default_dpi)

            # 绘制柱状图
            x_pos = np.arange(len(data))
            values = list(data.values())
            labels = list(data.keys())

            bars = ax.bar(x_pos, values, color=sns.color_palette(self.default_color_palette, len(data)))

            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{height:.2f}',
                        ha='center', va='bottom')

            # 设置图表属性
            ax.set_title(title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')

            # 调整布局
            plt.tight_layout()

            # 保存图表
            if output_path:
                plt.savefig(output_path)
                self.logger.info(f"柱状图已保存到: {output_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建柱状图失败: {str(e)}")
            return None

    def create_heatmap(self, data: Dict[str, Any], title: str, x_label: str, y_label: str,
                      output_path: Optional[str] = None) -> Optional[Any]:
        """
        创建热力图

        Args:
            data: 热力图数据
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            output_path: 输出路径

        Returns:
            图表对象
        """
        if not VISUALIZATION_AVAILABLE:
            self.logger.warning("可视化库未安装，无法创建热力图")
            return None

        try:
            fig, ax = plt.subplots(figsize=self.default_figsize, dpi=self.default_dpi)

            # 确保数据是DataFrame格式
            if pd and not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)

            # 绘制热力图
            sns.heatmap(data, annot=True, fmt='.2f', cmap=self.default_color_palette,
                       ax=ax, cbar_kws={'label': 'Value'})

            # 设置图表属性
            ax.set_title(title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)

            # 调整布局
            plt.tight_layout()

            # 保存图表
            if output_path:
                plt.savefig(output_path)
                self.logger.info(f"热力图已保存到: {output_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建热力图失败: {str(e)}")
            return None

    def create_pie_chart(self, data: Dict[str, float], title: str,
                        output_path: Optional[str] = None) -> Optional[Any]:
        """
        创建饼图

        Args:
            data: 饼图数据
            title: 图表标题
            output_path: 输出路径

        Returns:
            图表对象
        """
        if not VISUALIZATION_AVAILABLE:
            self.logger.warning("可视化库未安装，无法创建饼图")
            return None

        try:
            fig, ax = plt.subplots(figsize=(10, 8), dpi=self.default_dpi)

            # 绘制饼图
            labels = list(data.keys())
            values = list(data.values())

            wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                           startangle=90, colors=sns.color_palette(self.default_color_palette, len(data)))

            # 设置饼图属性
            ax.set_title(title)
            ax.axis('equal')  # 确保饼图是圆形

            # 调整图例
            plt.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            # 调整布局
            plt.tight_layout()

            # 保存图表
            if output_path:
                plt.savefig(output_path)
                self.logger.info(f"饼图已保存到: {output_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建饼图失败: {str(e)}")
            return None

    def create_subplots(self, plots_data: List[Dict[str, Any]], rows: int, cols: int,
                       title: str, output_path: Optional[str] = None) -> Optional[Any]:
        """
        创建子图

        Args:
            plots_data: 子图数据
            rows: 行数
            cols: 列数
            title: 图表标题
            output_path: 输出路径

        Returns:
            图表对象
        """
        if not VISUALIZATION_AVAILABLE:
            self.logger.warning("可视化库未安装，无法创建子图")
            return None

        try:
            fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4), dpi=self.default_dpi)
            fig.suptitle(title, fontsize=16)

            # 绘制子图
            for i, plot_data in enumerate(plots_data):
                if i >= rows * cols:
                    break

                row = i // cols
                col = i % cols
                ax = axes[row, col] if rows > 1 and cols > 1 else axes[i]

                plot_type = plot_data.get('type', 'line')
                data = plot_data.get('data', {})
                plot_title = plot_data.get('title', f'Plot {i+1}')
                x_label = plot_data.get('x_label', 'X')
                y_label = plot_data.get('y_label', 'Y')

                if plot_type == 'line':
                    for series_name, series_data in data.items():
                        if isinstance(series_data, list) and len(series_data) > 0:
                            x_values = list(range(len(series_data)))
                            ax.plot(x_values, series_data, marker='o', label=series_name)
                    ax.legend()
                elif plot_type == 'bar':
                    x_pos = np.arange(len(data))
                    values = list(data.values())
                    labels = list(data.keys())
                    ax.bar(x_pos, values, color=sns.color_palette(self.default_color_palette, len(data)))
                    ax.set_xticks(x_pos)
                    ax.set_xticklabels(labels, rotation=45, ha='right')

                ax.set_title(plot_title)
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.grid(True, alpha=0.3)

            # 调整布局
            plt.tight_layout(rect=[0, 0, 1, 0.95])

            # 保存图表
            if output_path:
                plt.savefig(output_path)
                self.logger.info(f"子图已保存到: {output_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建子图失败: {str(e)}")
            return None

    def create_time_series_chart(self, data: Dict[str, List[float]], times: List[str],
                                title: str, y_label: str, output_path: Optional[str] = None) -> Optional[Any]:
        """
        创建时间序列图表

        Args:
            data: 时间序列数据
            times: 时间标签
            title: 图表标题
            y_label: Y轴标签
            output_path: 输出路径

        Returns:
            图表对象
        """
        if not VISUALIZATION_AVAILABLE:
            self.logger.warning("可视化库未安装，无法创建时间序列图表")
            return None

        try:
            fig, ax = plt.subplots(figsize=self.default_figsize, dpi=self.default_dpi)

            # 绘制时间序列
            for series_name, series_data in data.items():
                if isinstance(series_data, list) and len(series_data) == len(times):
                    ax.plot(times, series_data, marker='o', label=series_name)

            # 设置图表属性
            ax.set_title(title)
            ax.set_xlabel('Time')
            ax.set_ylabel(y_label)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # 旋转X轴标签
            plt.xticks(rotation=45, ha='right')

            # 调整布局
            plt.tight_layout()

            # 保存图表
            if output_path:
                plt.savefig(output_path)
                self.logger.info(f"时间序列图表已保存到: {output_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建时间序列图表失败: {str(e)}")
            return None

    def export_to_csv(self, data: Dict[str, Any], file_path: str) -> bool:
        """
        导出数据到CSV文件

        Args:
            data: 要导出的数据
            file_path: 文件路径

        Returns:
            是否导出成功
        """
        if not pd:
            self.logger.warning("pandas未安装，无法导出CSV文件")
            return False

        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            self.logger.info(f"数据已导出到CSV: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"导出CSV失败: {str(e)}")
            return False

    def export_to_json(self, data: Dict[str, Any], file_path: str) -> bool:
        """
        导出数据到JSON文件

        Args:
            data: 要导出的数据
            file_path: 文件路径

        Returns:
            是否导出成功
        """
        try:
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"数据已导出到JSON: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"导出JSON失败: {str(e)}")
            return False

    def close_all(self):
        """
        关闭所有图表
        """
        if plt:
            plt.close('all')
