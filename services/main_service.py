"""
主要服務類別
協調各個子服務的運作
"""

import logging
from typing import Optional, Dict, Any

from config import Config
from utils.helper import do_something
from decorators import timing, log_execution, retry_on_connection_error
from .base import BaseService
from .user_service import DataService
from .notification_service import NotificationService


class MainService(BaseService):
    """
    主要服務類別
    協調各個子服務的運作
    """

    def __init__(self, config: Config):
        """
        初始化主要服務

        Args:
            config: 應用程式配置
        """
        super().__init__(config)
        self.data_service: Optional[DataService] = None
        self.notification_service: Optional[NotificationService] = None
        self._is_running = False

    def initialize(self) -> None:
        """初始化服務"""
        self.logger.info("開始初始化主要服務...")

        # 初始化子服務
        self.data_service = DataService(self.config)
        self.data_service.initialize()

        self.notification_service = NotificationService(self.config)
        self.notification_service.initialize()

        self.logger.info("主要服務初始化完成")

    def cleanup(self) -> None:
        """清理服務資源"""
        self.logger.info("開始清理服務資源...")

        if self.data_service:
            self.data_service.cleanup()

        if self.notification_service:
            self.notification_service.cleanup()

        self._is_running = False
        self.logger.info("服務資源清理完成")

    @timing(log_level=logging.INFO)
    @log_execution(log_args=True, log_result=True)
    def run(self) -> None:
        """
        執行主要服務邏輯

        Raises:
            RuntimeError: 當服務未正確初始化時
        """
        if not self.data_service:
            raise RuntimeError("服務未正確初始化，請先呼叫 initialize()")

        self._is_running = True
        self.logger.info("服務啟動中...")

        try:
            # 執行主要業務邏輯
            result = do_something("Hello Service")
            self.logger.info(f"服務結果: {result}")

            # 這裡可以加入更多的業務邏輯
            self._perform_business_operations()

        except Exception as e:
            self.logger.error(f"服務執行過程中發生錯誤: {e}")
            raise
        finally:
            self._is_running = False
            self.logger.info("服務執行完成")

    @retry_on_connection_error(max_attempts=3, delay=1.0)
    def _perform_business_operations(self) -> None:
        """
        執行業務操作

        這個方法展示了如何使用裝飾器來處理重試邏輯
        """
        self.logger.info("執行業務操作...")

        # 模擬一些業務邏輯
        # 這裡可以加入實際的業務處理代碼

        self.logger.info("業務操作完成")

    @property
    def is_running(self) -> bool:
        """檢查服務是否正在執行"""
        return self._is_running

    def get_service_status(self) -> Dict[str, Any]:
        """
        取得服務狀態資訊

        Returns:
            包含服務狀態的字典
        """
        return {
            "service_name": self.__class__.__name__,
            "is_running": self._is_running,
            "config_env": self.config.env,
            "data_service_initialized": self.data_service is not None,
            "notification_service_initialized": self.notification_service is not None,
        }

    def get_data_service(self) -> Optional[DataService]:
        """
        取得資料服務實例

        Returns:
            資料服務實例或 None
        """
        return self.data_service

    def get_notification_service(self) -> Optional[NotificationService]:
        """
        取得通知服務實例

        Returns:
            通知服務實例或 None
        """
        return self.notification_service


__all__ = ["MainService"]
