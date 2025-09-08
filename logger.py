"""
日誌管理模組
提供統一的日誌配置和管理功能
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """彩色日誌格式化器"""

    # ANSI 顏色代碼
    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 綠色
        "WARNING": "\033[33m",  # 黃色
        "ERROR": "\033[31m",  # 紅色
        "CRITICAL": "\033[35m",  # 紫色
        "RESET": "\033[0m",  # 重置
    }

    def format(self, record):
        # 添加顏色
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_colors: bool = True,
) -> None:
    """
    設定全域日誌配置

    Args:
        level: 日誌等級 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日誌檔案路徑，如果為 None 則不寫入檔案
        enable_console: 是否啟用控制台輸出
        enable_colors: 是否啟用彩色輸出（僅限控制台）
    """
    # 清除現有的處理器
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 設定日誌等級
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)

    # 日誌格式
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台處理器
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)

        if enable_colors and sys.stdout.isatty():
            console_handler.setFormatter(
                ColoredFormatter(
                    "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
        else:
            console_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)

    # 檔案處理器
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    取得指定名稱的日誌記錄器

    Args:
        name: 日誌記錄器名稱，通常使用 __name__

    Returns:
        配置好的日誌記錄器
    """
    return logging.getLogger(name)


def get_logger_for_module(module_name: str) -> logging.Logger:
    """
    為特定模組取得日誌記錄器

    Args:
        module_name: 模組名稱

    Returns:
        配置好的日誌記錄器
    """
    return logging.getLogger(f"app.{module_name}")


__all__ = ["get_logger", "get_logger_for_module", "setup_logging", "ColoredFormatter"]
