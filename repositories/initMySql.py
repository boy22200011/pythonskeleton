"""
資料庫初始化模組
負責建立和管理資料庫連線、會話和基礎模型
"""

from contextlib import contextmanager
from typing import Generator, Optional
import logging

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import QueuePool

from config import Config

logger = logging.getLogger(__name__)

# 全域變數
engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None
Base = declarative_base()


def init_database(config: Config) -> None:
    """
    初始化資料庫連線

    Args:
        config: 應用程式配置物件

    Raises:
        SQLAlchemyError: 當資料庫連線失敗時
    """
    global engine, SessionLocal

    try:
        # 建立資料庫引擎
        engine = create_engine(
            config.db_url,
            echo=config.debug,
            poolclass=QueuePool,
            pool_size=10,  # 連線池大小
            max_overflow=20,  # 最大溢出連線數
            pool_pre_ping=True,  # 連線前檢查
            pool_recycle=1800,  # 避免 MySQL 連線閒置被踢
            pool_timeout=30,  # 取得連線的超時時間
            future=True,
            connect_args={
                "charset": "utf8mb4",
                "autocommit": False,
            },
        )

        # 設定連線事件監聽器
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """設定資料庫連線參數"""
            if "mysql" in config.db_url:
                with dbapi_connection.cursor() as cursor:
                    cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES'")
                    cursor.execute("SET SESSION time_zone='+00:00'")

        @event.listens_for(engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            """連線取出時的處理"""
            logger.debug("從連線池取出連線")

        @event.listens_for(engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            """連線歸還時的處理"""
            logger.debug("連線歸還到連線池")

        # 建立會話工廠
        SessionLocal = sessionmaker(
            bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

        # 測試連線
        test_connection()

        logger.info("資料庫初始化成功")

    except SQLAlchemyError as e:
        logger.error(f"資料庫初始化失敗: {e}")
        raise
    except Exception as e:
        logger.error(f"資料庫初始化發生未預期錯誤: {e}")
        raise SQLAlchemyError(f"資料庫初始化失敗: {e}")


def test_connection() -> bool:
    """
    測試資料庫連線

    Returns:
        連線是否成功

    Raises:
        SQLAlchemyError: 當連線測試失敗時
    """
    if not engine:
        raise SQLAlchemyError("資料庫引擎未初始化")

    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("資料庫連線測試成功")
        return True
    except SQLAlchemyError as e:
        logger.error(f"資料庫連線測試失敗: {e}")
        raise


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    取得資料庫會話的上下文管理器

    Yields:
        資料庫會話物件

    Raises:
        SQLAlchemyError: 當無法建立會話時
    """
    if not SessionLocal:
        raise SQLAlchemyError("資料庫會話工廠未初始化")

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"資料庫操作失敗，已回滾: {e}")
        raise
    finally:
        session.close()


def get_db_session_dependency() -> Generator[Session, None, None]:
    """
    用於依賴注入的資料庫會話產生器
    適用於 FastAPI 等框架

    Yields:
        資料庫會話物件
    """
    with get_db_session() as session:
        yield session


def close_database() -> None:
    """
    關閉資料庫連線
    """
    global engine, SessionLocal

    if engine:
        engine.dispose()
        logger.info("資料庫連線已關閉")

    engine = None
    SessionLocal = None


# 自動初始化（如果配置可用）
try:
    from config import load_config

    config = load_config()
    init_database(config)
except Exception as e:
    logger.warning(f"自動初始化資料庫失敗: {e}")


__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "init_database",
    "get_db_session",
    "get_db_session_dependency",
    "test_connection",
    "close_database",
]
