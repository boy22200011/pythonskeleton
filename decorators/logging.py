"""
日誌裝飾器
提供函數執行的詳細日誌記錄功能
"""

import logging
import traceback
from functools import wraps
from typing import Callable, Any, Optional, Dict

logger = logging.getLogger(__name__)


def log_execution(
    log_level: int = logging.INFO,
    log_args: bool = False,
    log_result: bool = False,
    log_exceptions: bool = True,
) -> Callable:
    """
    執行日誌裝飾器

    Args:
        log_level: 日誌等級
        log_args: 是否記錄函數參數
        log_result: 是否記錄函數結果
        log_exceptions: 是否記錄例外詳情

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 記錄函數開始執行
            message = f"開始執行函數: {func.__name__}"
            if log_args and (args or kwargs):
                message += f" (參數: args={args}, kwargs={kwargs})"

            logger.log(log_level, message)

            try:
                result = func(*args, **kwargs)

                # 記錄函數執行成功
                message = f"函數 {func.__name__} 執行成功"
                if log_result:
                    message += f" (結果: {result})"

                logger.log(log_level, message)
                return result

            except Exception as e:
                # 記錄函數執行失敗
                error_message = f"函數 {func.__name__} 執行失敗: {e}"

                if log_exceptions:
                    error_message += f"\n例外詳情:\n{traceback.format_exc()}"

                logger.error(error_message)
                raise

        return wrapper

    return decorator


def log_function_calls(
    include_args: bool = True,
    include_result: bool = False,
    log_level: int = logging.DEBUG,
) -> Callable:
    """
    函數呼叫日誌裝飾器

    Args:
        include_args: 是否包含參數
        include_result: 是否包含結果
        log_level: 日誌等級

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 記錄函數呼叫
            call_info = f"呼叫函數: {func.__name__}"

            if include_args:
                if args:
                    call_info += f" | args: {args}"
                if kwargs:
                    call_info += f" | kwargs: {kwargs}"

            logger.log(log_level, call_info)

            try:
                result = func(*args, **kwargs)

                if include_result:
                    logger.log(log_level, f"函數 {func.__name__} 返回: {result}")

                return result

            except Exception as e:
                logger.error(f"函數 {func.__name__} 發生例外: {e}")
                raise

        return wrapper

    return decorator


def log_database_operations(operation_type: str = "database") -> Callable:
    """
    資料庫操作日誌裝飾器

    Args:
        operation_type: 操作類型描述

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"開始 {operation_type} 操作: {func.__name__}")

            try:
                result = func(*args, **kwargs)
                logger.info(f"{operation_type} 操作成功: {func.__name__}")
                return result

            except Exception as e:
                logger.error(f"{operation_type} 操作失敗: {func.__name__} - {e}")
                raise

        return wrapper

    return decorator


def log_api_calls(
    api_name: Optional[str] = None, log_request: bool = True, log_response: bool = False
) -> Callable:
    """
    API 呼叫日誌裝飾器

    Args:
        api_name: API 名稱
        log_request: 是否記錄請求
        log_response: 是否記錄回應

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            api_display_name = api_name or func.__name__

            if log_request:
                logger.info(f"API 請求: {api_display_name}")
                if args:
                    logger.debug(f"請求參數: {args}")
                if kwargs:
                    logger.debug(f"請求參數: {kwargs}")

            try:
                result = func(*args, **kwargs)

                if log_response:
                    logger.info(f"API 回應: {api_display_name} - {result}")
                else:
                    logger.info(f"API 呼叫成功: {api_display_name}")

                return result

            except Exception as e:
                logger.error(f"API 呼叫失敗: {api_display_name} - {e}")
                raise

        return wrapper

    return decorator


__all__ = [
    "log_execution",
    "log_function_calls",
    "log_database_operations",
    "log_api_calls",
]
