# config.py
"""
配置管理模組
負責載入和管理應用程式的各種配置設定
"""
import os
from dataclasses import dataclass
from typing import Optional, Literal
from urllib.parse import quote_plus
import logging

logger = logging.getLogger(__name__)

try:
    # 若沒裝 python-dotenv 也沒關係，這行會失敗但不影響
    from dotenv import load_dotenv

    load_dotenv()
    logger.info("成功載入 .env 檔案")
except ImportError:
    logger.warning("python-dotenv 未安裝，將使用系統環境變數")
except Exception as e:
    logger.warning(f"載入 .env 檔案失敗: {e}")


def build_db_url(
    user: str,
    password: str,
    host: str,
    db: str,
    port: int = 3306,
    driver: str = "pymysql",
    charset: str = "utf8mb4",
) -> str:
    """
    建構資料庫連線 URL

    Args:
        user: 資料庫使用者名稱
        password: 資料庫密碼
        host: 資料庫主機位址
        db: 資料庫名稱
        port: 資料庫連接埠，預設為 3306
        driver: 資料庫驅動程式，預設為 pymysql
        charset: 字元集，預設為 utf8mb4

    Returns:
        格式化的資料庫連線 URL

    Raises:
        ValueError: 當必要參數為空時
    """
    if not all([user, host, db]):
        raise ValueError("資料庫使用者名稱、主機位址和資料庫名稱不能為空")

    # 密碼有 @ : ! 等符號時要 URL encode
    pw = quote_plus(password or "")
    return f"mysql+{driver}://{user}:{pw}@{host}:{port}/{db}?charset={charset}"


@dataclass(frozen=True)
class Config:
    """
    應用程式配置類別

    Attributes:
        env: 執行環境 (dev/test/prod)
        db_url: 資料庫連線 URL
        debug: 是否啟用除錯模式
        log_level: 日誌等級
        max_workers: 最大工作執行緒數
    """

    env: Literal["dev", "test", "prod"]
    db_url: str
    debug: bool = False
    log_level: str = "INFO"
    max_workers: int = 4

    def __post_init__(self):
        """配置驗證"""
        if not self.db_url:
            raise ValueError("資料庫連線 URL 不能為空")

        if self.env not in ["dev", "test", "prod"]:
            raise ValueError(f"不支援的環境: {self.env}")

        if self.max_workers <= 0:
            raise ValueError("最大工作執行緒數必須大於 0")


def load_config() -> Config:
    """
    載入應用程式配置

    Returns:
        配置物件

    Raises:
        ValueError: 當配置無效時
        EnvironmentError: 當環境變數設定不正確時
    """
    env = os.getenv("APP_ENV", "dev")

    if env not in ["dev", "test", "prod"]:
        raise ValueError(f"不支援的環境: {env}")

    try:
        if env == "dev":
            db_url = build_db_url(
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                host=os.getenv("DB_HOST", "127.0.0.1"),
                db=os.getenv("DB_NAME", "Microsys4S360"),
                port=int(os.getenv("DB_PORT", "3306")),
            )
            debug = True
            log_level = "DEBUG"
        elif env == "test":
            db_url = os.getenv("TEST_DB_URL", "")
            if not db_url:
                raise EnvironmentError("測試環境需要設定 TEST_DB_URL")
            debug = True
            log_level = "DEBUG"
        else:  # prod
            db_url = os.getenv("DB_URL", "")
            if not db_url:
                raise EnvironmentError("生產環境需要設定 DB_URL")
            debug = False
            log_level = os.getenv("LOG_LEVEL", "INFO")

        max_workers = int(os.getenv("MAX_WORKERS", "4"))

        config = Config(
            env=env,
            db_url=db_url,
            debug=debug,
            log_level=log_level,
            max_workers=max_workers,
        )

        logger.info(f"成功載入 {env} 環境配置")
        return config

    except ValueError as e:
        logger.error(f"配置驗證失敗: {e}")
        raise
    except Exception as e:
        logger.error(f"載入配置失敗: {e}")
        raise EnvironmentError(f"載入配置失敗: {e}")


__all__ = ["Config", "load_config", "build_db_url"]
