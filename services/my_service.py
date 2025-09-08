from logger import get_logger
from utils.helper import do_something

logger = get_logger(__name__)

class MyService:
    def __init__(self, config):
        self.config = config

    def run(self):
        logger.info("服務啟動中...")
        result = do_something("Hello Service")
        logger.info(f"服務結果: {result}")
