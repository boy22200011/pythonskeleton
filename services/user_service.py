"""
資料服務
處理資料相關的業務邏輯
"""

from typing import Optional, List, Dict, Any

from config import Config
from decorators import with_db_session
from .base import BaseService


class DataService(BaseService):
    """
    資料服務
    處理資料相關的業務邏輯

    注意：這個服務提供通用的資料操作方法，請根據您的實際資料庫結構進行調整
    """

    def initialize(self) -> None:
        """初始化資料服務"""
        self.logger.info("資料服務初始化完成")

    def cleanup(self) -> None:
        """清理資料服務資源"""
        self.logger.info("資料服務資源清理完成")

    @with_db_session
    def execute_query(
        self, session, query: str, params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        執行查詢語句

        Args:
            session: 資料庫會話
            query: SQL 查詢語句
            params: 查詢參數

        Returns:
            查詢結果列表
        """
        try:
            result = session.execute(query, params or {})
            columns = result.keys()
            rows = result.fetchall()

            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            self.logger.error(f"執行查詢失敗: {e}")
            raise

    @with_db_session
    def execute_update(self, session, query: str, params: Dict[str, Any] = None) -> int:
        """
        執行更新語句

        Args:
            session: 資料庫會話
            query: SQL 更新語句
            params: 更新參數

        Returns:
            影響的行數
        """
        try:
            result = session.execute(query, params or {})
            return result.rowcount
        except Exception as e:
            self.logger.error(f"執行更新失敗: {e}")
            raise

    @with_db_session
    def get_table_info(self, session, table_name: str) -> List[Dict[str, Any]]:
        """
        取得資料表結構資訊

        Args:
            session: 資料庫會話
            table_name: 資料表名稱

        Returns:
            資料表結構資訊
        """
        query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_COMMENT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
        """
        return self.execute_query(session, query, {"table_name": table_name})

    @with_db_session
    def get_table_list(self, session) -> List[Dict[str, Any]]:
        """
        取得所有資料表列表

        Args:
            session: 資料庫會話

        Returns:
            資料表列表
        """
        query = """
        SELECT 
            TABLE_NAME,
            TABLE_COMMENT,
            CREATE_TIME,
            UPDATE_TIME
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME
        """
        return self.execute_query(session, query)

    @with_db_session
    def get_table_data(
        self, session, table_name: str, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        取得資料表資料

        Args:
            session: 資料庫會話
            table_name: 資料表名稱
            limit: 限制筆數
            offset: 偏移量

        Returns:
            資料列表
        """
        query = f"SELECT * FROM `{table_name}` LIMIT :limit OFFSET :offset"
        return self.execute_query(session, query, {"limit": limit, "offset": offset})

    @with_db_session
    def count_table_records(self, session, table_name: str) -> int:
        """
        計算資料表記錄數

        Args:
            session: 資料庫會話
            table_name: 資料表名稱

        Returns:
            記錄數
        """
        query = f"SELECT COUNT(*) as count FROM `{table_name}`"
        result = self.execute_query(session, query)
        return result[0]["count"] if result else 0


# 為了向後相容，保留 UserService 別名
UserService = DataService

__all__ = ["DataService", "UserService"]
