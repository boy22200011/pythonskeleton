import sys
import argparse
from logger import get_logger
from config import Config
from services.my_service import MyService

logger = get_logger(__name__)

def main():
    # 命令列參數
    parser = argparse.ArgumentParser(description="後端服務骨架")
    parser.add_argument("--env", type=str, default="dev", help="執行環境: dev/test/prod")
    args = parser.parse_args()

    # 載入設定
    config = Config(env=args.env)
    logger.info(f"使用環境: {args.env}")
    logger.info(f"DB連線字串: {config.db_conn}")
    try:
        # 建立服務
        service = MyService(config)
        service.run()
    except Exception as e:
        logger.exception(f"程式執行失敗: {e}")
        sys.exit(1)
    finally:
        logger.info("程式結束")

if __name__ == "__main__":
    main()
