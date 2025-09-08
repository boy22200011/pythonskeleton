"""
基礎服務類別
提供所有服務的共同功能和介面
"""

from abc import ABC, abstractmethod
from typing import Optional

from config import Config
from logger import get_logger


class BaseService(ABC):
    """
    基礎服務類別
    提供所有服務的共同功能和介面
    """

    def __init__(self, config: Config):
        """
        初始化服務

        Args:
            config: 應用程式配置
        """
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def initialize(self) -> None:
        """初始化服務"""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """清理服務資源"""
        pass


__all__ = ["BaseService"]
