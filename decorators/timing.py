"""
計時裝飾器
提供函數執行時間的測量和記錄功能
"""

import time
import logging
from functools import wraps
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


def timing(
    log_level: int = logging.INFO,
    log_message: Optional[str] = None,
    include_args: bool = False,
) -> Callable:
    """
    計時裝飾器

    Args:
        log_level: 日誌等級
        log_message: 自訂日誌訊息
        include_args: 是否在日誌中包含函數參數

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                message = log_message or f"函數 {func.__name__} 執行完成"
                if include_args and (args or kwargs):
                    message += f" (參數: args={args}, kwargs={kwargs})"
                message += f" - 耗時: {execution_time:.4f} 秒"

                logger.log(log_level, message)
                return result

            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"函數 {func.__name__} 執行失敗 - 耗時: {execution_time:.4f} 秒, 錯誤: {e}"
                )
                raise

        return wrapper

    return decorator


def slow_function_warning(threshold: float = 1.0) -> Callable:
    """
    慢函數警告裝飾器

    Args:
        threshold: 執行時間閾值（秒）

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                if execution_time > threshold:
                    logger.warning(
                        f"函數 {func.__name__} 執行時間過長: {execution_time:.4f} 秒 "
                        f"(閾值: {threshold} 秒)"
                    )

                return result

            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"函數 {func.__name__} 執行失敗 - 耗時: {execution_time:.4f} 秒, 錯誤: {e}"
                )
                raise

        return wrapper

    return decorator


def performance_monitor(
    log_slow_queries: bool = True, slow_query_threshold: float = 0.5
) -> Callable:
    """
    效能監控裝飾器
    特別適用於資料庫查詢和 API 呼叫

    Args:
        log_slow_queries: 是否記錄慢查詢
        slow_query_threshold: 慢查詢閾值（秒）

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                if log_slow_queries and execution_time > slow_query_threshold:
                    logger.warning(
                        f"慢查詢檢測 - 函數: {func.__name__}, "
                        f"執行時間: {execution_time:.4f} 秒, "
                        f"閾值: {slow_query_threshold} 秒"
                    )
                else:
                    logger.debug(
                        f"函數 {func.__name__} 執行時間: {execution_time:.4f} 秒"
                    )

                return result

            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"函數 {func.__name__} 執行失敗 - "
                    f"執行時間: {execution_time:.4f} 秒, 錯誤: {e}"
                )
                raise

        return wrapper

    return decorator


__all__ = ["timing", "slow_function_warning", "performance_monitor"]
