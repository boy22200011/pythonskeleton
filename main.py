"""
主程式入口
負責應用程式的啟動、配置和服務管理
"""

import sys
import argparse
import signal
import atexit
from typing import Optional
from pathlib import Path

from logger import get_logger, setup_logging
from config import Config, load_config
from services import MyService
from repositories.initMySql import close_database

logger = get_logger(__name__)


class Application:
    """
    應用程式主類別
    負責管理應用程式的生命週期
    """

    def __init__(self):
        """初始化應用程式"""
        self.config: Optional[Config] = None
        self.service: Optional[MyService] = None
        self._shutdown_requested = False

    def setup_signal_handlers(self) -> None:
        """設定信號處理器"""

        def signal_handler(signum, frame):
            logger.info(f"收到信號 {signum}，開始優雅關閉...")
            self._shutdown_requested = True
            self.shutdown()

        # 註冊信號處理器
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # 終止信號

        # 註冊退出處理器
        atexit.register(self.cleanup)

    def load_configuration(self, env: str) -> None:
        """
        載入應用程式配置

        Args:
            env: 執行環境

        Raises:
            SystemExit: 當配置載入失敗時
        """
        try:
            # 設定環境變數
            import os

            os.environ["APP_ENV"] = env

            # 載入配置
            self.config = load_config()

            # 設定日誌
            log_file = None
            if self.config.env == "prod":
                log_file = "logs/app.log"

            setup_logging(
                level=self.config.log_level,
                log_file=log_file,
                enable_console=True,
                enable_colors=self.config.env != "prod",
            )

            logger.info(f"配置載入成功 - 環境: {self.config.env}")

        except Exception as e:
            logger.error(f"配置載入失敗: {e}")
            sys.exit(1)

    def initialize_services(self) -> None:
        """
        初始化服務

        Raises:
            SystemExit: 當服務初始化失敗時
        """
        try:
            logger.info("開始初始化服務...")

            # 建立主要服務
            self.service = MyService(self.config)
            self.service.initialize()

            logger.info("服務初始化完成")

        except Exception as e:
            logger.error(f"服務初始化失敗: {e}")
            sys.exit(1)

    def run(self) -> None:
        """
        執行應用程式

        Raises:
            SystemExit: 當應用程式執行失敗時
        """
        try:
            logger.info("應用程式開始執行...")

            # 顯示服務狀態
            status = self.service.get_service_status()
            logger.info(f"服務狀態: {status}")

            # 執行主要服務
            self.service.run()

            logger.info("應用程式執行完成")

        except KeyboardInterrupt:
            logger.info("收到中斷信號，開始關閉應用程式...")
        except Exception as e:
            logger.exception(f"應用程式執行失敗: {e}")
            sys.exit(1)

    def shutdown(self) -> None:
        """優雅關閉應用程式"""
        if self._shutdown_requested:
            return

        self._shutdown_requested = True
        logger.info("開始關閉應用程式...")

        try:
            if self.service:
                self.service.cleanup()

            logger.info("應用程式關閉完成")

        except Exception as e:
            logger.error(f"應用程式關閉時發生錯誤: {e}")

    def cleanup(self) -> None:
        """清理資源"""
        try:
            # 關閉資料庫連線
            close_database()
            logger.info("資源清理完成")

        except Exception as e:
            logger.error(f"資源清理時發生錯誤: {e}")


def parse_arguments() -> argparse.Namespace:
    """
    解析命令列參數

    Returns:
        解析後的參數物件
    """
    parser = argparse.ArgumentParser(
        description="Python 後端服務骨架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例用法:
  python main.py                    # 使用預設開發環境
  python main.py --env prod         # 使用生產環境
  python main.py --env test         # 使用測試環境
  python main.py --help             # 顯示說明
        """,
    )

    parser.add_argument(
        "--env",
        type=str,
        choices=["dev", "test", "prod"],
        default="dev",
        help="執行環境 (預設: dev)",
    )

    parser.add_argument(
        "--version", action="version", version="Python 後端服務骨架 v1.0.0"
    )

    return parser.parse_args()


def main() -> None:
    """
    主程式入口點

    負責：
    1. 解析命令列參數
    2. 載入配置
    3. 初始化服務
    4. 執行應用程式
    5. 處理優雅關閉
    """
    try:
        # 解析命令列參數
        args = parse_arguments()

        # 建立應用程式實例
        app = Application()

        # 設定信號處理器
        app.setup_signal_handlers()

        # 載入配置
        app.load_configuration(args.env)

        # 初始化服務
        app.initialize_services()

        # 執行應用程式
        app.run()

    except KeyboardInterrupt:
        logger.info("程式被使用者中斷")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"程式執行失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
