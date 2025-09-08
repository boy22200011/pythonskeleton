import logging

def get_logger(name: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        force=True # 確保不會被其他地方的 basicConfig 蓋掉
    )
    return logging.getLogger(name)

__all__ = ["get_logger"]