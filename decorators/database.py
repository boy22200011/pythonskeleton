"""
資料庫裝飾器
提供資料庫操作相關的裝飾器功能
"""

import logging
from functools import wraps
from typing import Callable, Any, Optional
from contextlib import contextmanager

from repositories.initMySql import get_db_session

logger = logging.getLogger(__name__)


def with_db_session(auto_commit: bool = True, auto_rollback: bool = True) -> Callable:
    """
    資料庫會話裝飾器
    自動管理資料庫會話的建立、提交和回滾

    Args:
        auto_commit: 是否自動提交事務
        auto_rollback: 發生錯誤時是否自動回滾

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with get_db_session() as session:
                # 將 session 作為第一個參數傳入函數
                return func(session, *args, **kwargs)

        return wrapper

    return decorator


def transactional(isolation_level: Optional[str] = None) -> Callable:
    """
    事務裝飾器
    確保函數在事務中執行

    Args:
        isolation_level: 事務隔離等級

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with get_db_session() as session:
                try:
                    # 設定隔離等級（如果指定）
                    if isolation_level:
                        session.execute(
                            f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"
                        )

                    result = func(session, *args, **kwargs)
                    session.commit()
                    logger.debug(f"事務提交成功: {func.__name__}")
                    return result

                except Exception as e:
                    session.rollback()
                    logger.error(f"事務回滾: {func.__name__} - {e}")
                    raise

        return wrapper

    return decorator


def read_only(use_read_replica: bool = False) -> Callable:
    """
    唯讀裝飾器
    標記函數為唯讀操作，可以優化查詢效能

    Args:
        use_read_replica: 是否使用讀取副本

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with get_db_session() as session:
                # 設定唯讀模式
                if use_read_replica:
                    # 這裡可以設定使用讀取副本的邏輯
                    logger.debug(f"使用讀取副本執行: {func.__name__}")

                # 設定會話為唯讀模式
                session.execute("SET SESSION TRANSACTION READ ONLY")

                try:
                    result = func(session, *args, **kwargs)
                    logger.debug(f"唯讀操作完成: {func.__name__}")
                    return result
                finally:
                    # 恢復讀寫模式
                    session.execute("SET SESSION TRANSACTION READ WRITE")

        return wrapper

    return decorator


def cache_query_result(
    cache_key_func: Optional[Callable] = None, ttl: int = 300
) -> Callable:
    """
    查詢結果快取裝飾器
    快取資料庫查詢結果以提高效能

    Args:
        cache_key_func: 快取鍵生成函數
        ttl: 快取存活時間（秒）

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 生成快取鍵
            if cache_key_func:
                cache_key = cache_key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # 這裡可以整合 Redis 或其他快取系統
            # 目前只是範例，實際使用時需要實作快取邏輯
            logger.debug(f"查詢快取鍵: {cache_key}")

            # 執行原始函數
            return func(*args, **kwargs)

        return wrapper

    return decorator


def batch_operation(batch_size: int = 1000) -> Callable:
    """
    批次操作裝飾器
    將大量資料操作分批處理

    Args:
        batch_size: 批次大小

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 假設第一個參數是要處理的資料列表
            if args and hasattr(args[0], "__iter__"):
                data_list = args[0]
                other_args = args[1:]

                results = []
                total_items = len(data_list)

                logger.info(
                    f"開始批次處理 {total_items} 個項目，批次大小: {batch_size}"
                )

                for i in range(0, total_items, batch_size):
                    batch = data_list[i : i + batch_size]
                    batch_num = i // batch_size + 1
                    total_batches = (total_items + batch_size - 1) // batch_size

                    logger.debug(
                        f"處理批次 {batch_num}/{total_batches} ({len(batch)} 個項目)"
                    )

                    try:
                        batch_result = func(batch, *other_args, **kwargs)
                        results.append(batch_result)
                    except Exception as e:
                        logger.error(f"批次 {batch_num} 處理失敗: {e}")
                        raise

                logger.info(f"批次處理完成，共處理 {total_items} 個項目")
                return results
            else:
                # 如果不是批次操作，直接執行
                return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = [
    "with_db_session",
    "transactional",
    "read_only",
    "cache_query_result",
    "batch_operation",
]
