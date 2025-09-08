"""
重試裝飾器
提供函數執行失敗時的自動重試功能
"""

import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple, Any, Optional

logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None,
) -> Callable:
    """
    重試裝飾器

    Args:
        max_attempts: 最大重試次數
        delay: 初始延遲時間（秒）
        backoff_factor: 延遲時間倍增因子
        exceptions: 需要重試的例外類型
        on_retry: 重試時的回調函數

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts - 1:
                        logger.error(
                            f"函數 {func.__name__} 在 {max_attempts} 次嘗試後仍然失敗"
                        )
                        raise e

                    logger.warning(
                        f"函數 {func.__name__} 第 {attempt + 1} 次嘗試失敗: {e}"
                    )

                    if on_retry:
                        on_retry(attempt + 1, e)

                    time.sleep(current_delay)
                    current_delay *= backoff_factor

            # 這行程式碼理論上不會執行到
            raise last_exception

        return wrapper

    return decorator


def retry_on_connection_error(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    針對連線錯誤的重試裝飾器

    Args:
        max_attempts: 最大重試次數
        delay: 延遲時間（秒）

    Returns:
        裝飾後的函數
    """
    from sqlalchemy.exc import SQLAlchemyError, DisconnectionError
    import requests.exceptions

    return retry(
        max_attempts=max_attempts,
        delay=delay,
        exceptions=(
            SQLAlchemyError,
            DisconnectionError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ),
    )


def retry_on_http_error(
    max_attempts: int = 3,
    delay: float = 1.0,
    status_codes: Tuple[int, ...] = (500, 502, 503, 504),
) -> Callable:
    """
    針對 HTTP 錯誤的重試裝飾器

    Args:
        max_attempts: 最大重試次數
        delay: 延遲時間（秒）
        status_codes: 需要重試的 HTTP 狀態碼

    Returns:
        裝飾後的函數
    """
    import requests

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code in status_codes:
                        last_exception = e

                        if attempt == max_attempts - 1:
                            logger.error(f"HTTP 請求在 {max_attempts} 次嘗試後仍然失敗")
                            raise e

                        logger.warning(
                            f"HTTP 請求第 {attempt + 1} 次嘗試失敗，狀態碼: {e.response.status_code}"
                        )
                        time.sleep(delay)
                    else:
                        raise e
                except Exception as e:
                    raise e

            raise last_exception

        return wrapper

    return decorator


__all__ = ["retry", "retry_on_connection_error", "retry_on_http_error"]
