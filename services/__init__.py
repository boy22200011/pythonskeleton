"""
服務層模組
提供業務邏輯處理和服務協調功能
"""

from .base import BaseService
from .user_service import DataService, UserService
from .main_service import MainService
from .notification_service import NotificationService, NotificationType

# 為了向後相容，保留 MyService 別名
MyService = MainService

__all__ = [
    "BaseService",
    "DataService",
    "UserService",
    "MainService",
    "NotificationService",
    "NotificationType",
    "MyService",
]
