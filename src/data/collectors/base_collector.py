# Base Collector Class

class BaseCollector:
    """
    基础数据采集器类，定义通用接口和方法
    """

    def __init__(self, config=None):
        """
        初始化采集器

        Args:
            config: 采集器配置参数
        """
        self.config = config or {}
        self.data_source = ""
        self.last_collected = None

    def collect(self, **kwargs):
        """
        采集数据的核心方法，子类必须实现

        Returns:
            采集的数据
        """
        raise NotImplementedError("Subclass must implement collect method")

    def validate(self, data):
        """
        验证采集的数据

        Args:
            data: 采集的数据

        Returns:
            bool: 数据是否有效
        """
        if data is None:
            return False
        return True

    def transform(self, data):
        """
        转换数据格式

        Args:
            data: 原始数据

        Returns:
            转换后的数据
        """
        return data

    def save(self, data):
        """
        保存采集的数据

        Args:
            data: 采集的数据
        """
        pass

    def get_last_collected(self):
        """
        获取上次采集时间

        Returns:
            上次采集时间
        """
        return self.last_collected

    def set_last_collected(self, timestamp):
        """
        设置上次采集时间

        Args:
            timestamp: 时间戳
        """
        self.last_collected = timestamp
