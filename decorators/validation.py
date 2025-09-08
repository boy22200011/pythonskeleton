"""
驗證裝飾器
提供函數參數和返回值的驗證功能
"""

import inspect
from functools import wraps
from typing import Callable, Any, Type, Union, get_type_hints, get_origin, get_args


def validate_input(strict: bool = False, skip_none: bool = True) -> Callable:
    """
    輸入驗證裝飾器
    根據函數的型別提示驗證參數

    Args:
        strict: 是否嚴格模式（不允許額外參數）
        skip_none: 是否跳過 None 值驗證

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 取得函數簽名和型別提示
            sig = inspect.signature(func)
            type_hints = get_type_hints(func)

            # 綁定參數
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # 驗證每個參數
            for param_name, param_value in bound_args.arguments.items():
                if param_name in type_hints:
                    expected_type = type_hints[param_name]

                    # 跳過 None 值（如果允許）
                    if skip_none and param_value is None:
                        continue

                    # 驗證型別
                    if not _is_valid_type(param_value, expected_type):
                        raise TypeError(
                            f"參數 '{param_name}' 的型別錯誤: "
                            f"期望 {expected_type}, 實際 {type(param_value)}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_output(expected_return_type: Type[Any]) -> Callable:
    """
    輸出驗證裝飾器
    驗證函數返回值是否符合預期型別

    Args:
        expected_return_type: 期望的返回型別

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            if not _is_valid_type(result, expected_return_type):
                raise TypeError(
                    f"返回值型別錯誤: 期望 {expected_return_type}, 實際 {type(result)}"
                )

            return result

        return wrapper

    return decorator


def validate_range(
    min_value: Union[int, float] = None,
    max_value: Union[int, float] = None,
    param_name: str = None,
) -> Callable:
    """
    數值範圍驗證裝飾器

    Args:
        min_value: 最小值
        max_value: 最大值
        param_name: 要驗證的參數名稱

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 取得函數簽名
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # 如果指定了參數名稱，只驗證該參數
            if param_name:
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    _validate_numeric_range(value, min_value, max_value, param_name)
            else:
                # 驗證所有數值參數
                for name, value in bound_args.arguments.items():
                    if isinstance(value, (int, float)):
                        _validate_numeric_range(value, min_value, max_value, name)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_not_empty(param_names: list[str] = None) -> Callable:
    """
    非空驗證裝飾器

    Args:
        param_names: 要驗證的參數名稱列表，如果為 None 則驗證所有參數

    Returns:
        裝飾後的函數
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 取得函數簽名
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # 決定要驗證的參數
            params_to_check = param_names or list(bound_args.arguments.keys())

            for param_name in params_to_check:
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]

                    # 檢查是否為空
                    if value is None or (hasattr(value, "__len__") and len(value) == 0):
                        raise ValueError(f"參數 '{param_name}' 不能為空")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def _is_valid_type(value: Any, expected_type: Type[Any]) -> bool:
    """
    檢查值是否符合預期型別

    Args:
        value: 要檢查的值
        expected_type: 預期型別

    Returns:
        是否符合型別
    """
    # 處理 Union 型別
    if get_origin(expected_type) is Union:
        return any(_is_valid_type(value, arg) for arg in get_args(expected_type))

    # 處理 Optional 型別
    if expected_type is type(None):
        return value is None

    # 處理基本型別
    if expected_type in (int, float, str, bool, list, dict, tuple):
        return isinstance(value, expected_type)

    # 處理其他型別
    try:
        return isinstance(value, expected_type)
    except TypeError:
        # 如果 isinstance 失敗，嘗試其他檢查
        return type(value) == expected_type


def _validate_numeric_range(
    value: Union[int, float],
    min_value: Union[int, float],
    max_value: Union[int, float],
    param_name: str,
) -> None:
    """
    驗證數值範圍

    Args:
        value: 要驗證的值
        min_value: 最小值
        max_value: 最大值
        param_name: 參數名稱

    Raises:
        ValueError: 當值超出範圍時
    """
    if min_value is not None and value < min_value:
        raise ValueError(f"參數 '{param_name}' 的值 {value} 小於最小值 {min_value}")

    if max_value is not None and value > max_value:
        raise ValueError(f"參數 '{param_name}' 的值 {value} 大於最大值 {max_value}")


__all__ = ["validate_input", "validate_output", "validate_range", "validate_not_empty"]
