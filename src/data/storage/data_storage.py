# Data Storage Module

import pymongo
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
import json
import logging

class DataStorage:
    """
    数据存储基类
    """

    def __init__(self, config=None):
        """
        初始化数据存储

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """
        连接到存储系统
        """
        raise NotImplementedError("Subclass must implement connect method")

    def disconnect(self):
        """
        断开连接
        """
        raise NotImplementedError("Subclass must implement disconnect method")

    def store(self, data, collection=None):
        """
        存储数据

        Args:
            data: 要存储的数据
            collection: 集合或表名
        """
        raise NotImplementedError("Subclass must implement store method")

    def validate(self, data):
        """
        验证数据

        Args:
            data: 数据

        Returns:
            bool: 数据是否有效
        """
        if data is None or len(data) == 0:
            return False
        return True

class MongoDBStorage(DataStorage):
    """
    MongoDB 数据存储
    """

    def __init__(self, config=None):
        """
        初始化 MongoDB 存储

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """
        连接到 MongoDB
        """
        try:
            mongo_config = self.config.get('mongodb', {
                'host': 'localhost',
                'port': 27017,
                'database': 'trendmatrix'
            })

            host = mongo_config.get('host')
            port = mongo_config.get('port')
            database = mongo_config.get('database')

            self.client = pymongo.MongoClient(host, port)
            self.db = self.client[database]
            self.logger.info(f"Connected to MongoDB at {host}:{port}")

        except Exception as e:
            self.logger.error(f"Error connecting to MongoDB: {str(e)}")
            self.client = None
            self.db = None

    def disconnect(self):
        """
        断开 MongoDB 连接
        """
        if self.client:
            try:
                self.client.close()
                self.logger.info("Disconnected from MongoDB")
            except Exception as e:
                self.logger.error(f"Error disconnecting from MongoDB: {str(e)}")
            finally:
                self.client = None
                self.db = None

    def store(self, data, collection=None):
        """
        存储数据到 MongoDB

        Args:
            data: 要存储的数据
            collection: 集合名

        Returns:
            存储结果
        """
        if not self.validate(data):
            self.logger.warning("No data to store")
            return 0

        if not self.db:
            self.logger.error("MongoDB connection not established")
            return 0

        if not collection:
            self.logger.error("Collection name not provided")
            return 0

        try:
            collection_obj = self.db[collection]

            # 处理单条数据
            if isinstance(data, dict):
                result = collection_obj.insert_one(data)
                return 1
            # 处理多条数据
            elif isinstance(data, list):
                if len(data) > 0:
                    result = collection_obj.insert_many(data)
                    return len(result.inserted_ids)
                else:
                    return 0
            else:
                self.logger.error("Data format not supported")
                return 0

        except Exception as e:
            self.logger.error(f"Error storing data to MongoDB: {str(e)}")
            return 0

    def find(self, collection, query=None, projection=None, limit=100):
        """
        从 MongoDB 查询数据

        Args:
            collection: 集合名
            query: 查询条件
            projection: 投影
            limit: 限制返回数量

        Returns:
            查询结果
        """
        if not self.db:
            self.logger.error("MongoDB connection not established")
            return []

        try:
            collection_obj = self.db[collection]
            query = query or {}
            projection = projection or {}

            cursor = collection_obj.find(query, projection).limit(limit)
            return list(cursor)

        except Exception as e:
            self.logger.error(f"Error querying MongoDB: {str(e)}")
            return []

class TimescaleDBStorage(DataStorage):
    """
    TimescaleDB 数据存储
    """

    def __init__(self, config=None):
        """
        初始化 TimescaleDB 存储

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """
        连接到 TimescaleDB
        """
        try:
            timescale_config = self.config.get('timescale', {
                'host': 'localhost',
                'port': 5432,
                'database': 'trendmatrix',
                'user': 'postgres',
                'password': 'postgres'
            })

            host = timescale_config.get('host')
            port = timescale_config.get('port')
            database = timescale_config.get('database')
            user = timescale_config.get('user')
            password = timescale_config.get('password')

            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to TimescaleDB at {host}:{port}")

        except Exception as e:
            self.logger.error(f"Error connecting to TimescaleDB: {str(e)}")
            self.connection = None
            self.cursor = None

    def disconnect(self):
        """
        断开 TimescaleDB 连接
        """
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as e:
                self.logger.error(f"Error closing cursor: {str(e)}")
            finally:
                self.cursor = None

        if self.connection:
            try:
                self.connection.close()
                self.logger.info("Disconnected from TimescaleDB")
            except Exception as e:
                self.logger.error(f"Error disconnecting from TimescaleDB: {str(e)}")
            finally:
                self.connection = None

    def store(self, data, table=None):
        """
        存储数据到 TimescaleDB

        Args:
            data: 要存储的数据
            table: 表名

        Returns:
            存储结果
        """
        if not self.validate(data):
            self.logger.warning("No data to store")
            return 0

        if not self.connection or not self.cursor:
            self.logger.error("TimescaleDB connection not established")
            return 0

        if not table:
            self.logger.error("Table name not provided")
            return 0

        try:
            # 确保表存在
            self._ensure_table_exists(table, data)

            # 构建插入语句
            if isinstance(data, dict):
                return self._insert_single_row(table, data)
            elif isinstance(data, list):
                if len(data) > 0:
                    return self._insert_multiple_rows(table, data)
                else:
                    return 0
            else:
                self.logger.error("Data format not supported")
                return 0

        except Exception as e:
            self.logger.error(f"Error storing data to TimescaleDB: {str(e)}")
            self.connection.rollback()
            return 0

    def _ensure_table_exists(self, table, data):
        """
        确保表存在

        Args:
            table: 表名
            data: 数据样例
        """
        if isinstance(data, dict):
            columns = self._get_columns(data)
        elif isinstance(data, list) and len(data) > 0:
            columns = self._get_columns(data[0])
        else:
            return

        # 构建创建表语句
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table} (
"

        # 添加时间戳列
        create_table_sql += "    time TIMESTAMPTZ DEFAULT NOW(),\n"

        # 添加数据列
        for col, col_type in columns.items():
            create_table_sql += f"    {col} {col_type},\n"

        create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

        # 执行创建表语句
        self.cursor.execute(create_table_sql)

        # 将表转换为超表
        try:
            self.cursor.execute(f"SELECT create_hypertable('{table}', 'time');")
        except Exception:
            # 表可能已经是超表
            pass

        self.connection.commit()

    def _get_columns(self, data):
        """
        从数据中提取列和类型

        Args:
            data: 数据

        Returns:
            列和类型的字典
        """
        columns = {}

        for key, value in data.items():
            col_type = self._get_postgres_type(value)
            if col_type:
                columns[key] = col_type

        return columns

    def _get_postgres_type(self, value):
        """
        获取 PostgreSQL 类型

        Args:
            value: 值

        Returns:
            PostgreSQL 类型
        """
        if isinstance(value, int):
            return 'INTEGER'
        elif isinstance(value, float):
            return 'DOUBLE PRECISION'
        elif isinstance(value, bool):
            return 'BOOLEAN'
        elif isinstance(value, str):
            return 'TEXT'
        elif isinstance(value, (dict, list)):
            return 'JSONB'
        elif value is None:
            return 'TEXT'
        else:
            return 'TEXT'

    def _insert_single_row(self, table, data):
        """
        插入单行数据

        Args:
            table: 表名
            data: 数据

        Returns:
            插入的行数
        """
        columns = list(data.keys())
        values = list(data.values())

        # 构建插入语句
        placeholders = ','.join(['%s'] * len(values))
        columns_str = ','.join(columns)

        sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders});"

        # 执行插入
        self.cursor.execute(sql, values)
        self.connection.commit()

        return 1

    def _insert_multiple_rows(self, table, data_list):
        """
        插入多行数据

        Args:
            table: 表名
            data_list: 数据列表

        Returns:
            插入的行数
        """
        if not data_list:
            return 0

        # 获取列名
        columns = list(data_list[0].keys())
        columns_str = ','.join(columns)
        placeholders = ','.join(['%s'] * len(columns))

        # 构建插入语句
        sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders});"

        # 准备数据
        values_list = []
        for data in data_list:
            values = [data.get(col) for col in columns]
            values_list.append(values)

        # 执行批量插入
        execute_batch(self.cursor, sql, values_list)
        self.connection.commit()

        return len(values_list)

class StorageManager:
    """
    存储管理器
    """

    def __init__(self, config=None):
        """
        初始化存储管理器

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.mongodb = MongoDBStorage(config)
        self.timescaledb = TimescaleDBStorage(config)

    def store(self, data, storage_type='mongodb', collection=None, table=None):
        """
        存储数据

        Args:
            data: 要存储的数据
            storage_type: 存储类型
            collection: MongoDB 集合名
            table: TimescaleDB 表名

        Returns:
            存储结果
        """
        if storage_type == 'mongodb':
            return self.mongodb.store(data, collection)
        elif storage_type == 'timescaledb':
            return self.timescaledb.store(data, table)
        else:
            logging.error(f"Storage type not supported: {storage_type}")
            return 0

    def close(self):
        """
        关闭所有存储连接
        """
        self.mongodb.disconnect()
        self.timescaledb.disconnect()
