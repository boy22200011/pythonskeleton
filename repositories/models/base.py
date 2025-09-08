"""
基礎資料模型
提供所有實體模型的共同欄位和方法
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session

from repositories.initMySql import Base


class BaseModel(Base):
    """
    基礎模型類別
    提供所有實體模型的共同欄位和基本方法
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, comment="建立時間"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新時間",
    )
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否已刪除")

    @declared_attr
    def __tablename__(cls) -> str:
        """自動生成資料表名稱"""
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        """
        將模型轉換為字典

        Returns:
            包含模型資料的字典
        """
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        從字典更新模型屬性

        Args:
            data: 包含要更新資料的字典
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def soft_delete(self) -> None:
        """軟刪除（標記為已刪除）"""
        self.is_deleted = True
        self.updated_at = datetime.utcnow()

    def restore(self) -> None:
        """還原軟刪除"""
        self.is_deleted = False
        self.updated_at = datetime.utcnow()

    @classmethod
    def get_by_id(cls, session: Session, id: int) -> Optional["BaseModel"]:
        """
        根據 ID 取得單一記錄

        Args:
            session: 資料庫會話
            id: 記錄 ID

        Returns:
            找到的記錄或 None
        """
        return session.query(cls).filter(cls.id == id, cls.is_deleted == False).first()

    @classmethod
    def get_all(
        cls, session: Session, skip: int = 0, limit: int = 100
    ) -> list["BaseModel"]:
        """
        取得所有記錄（分頁）

        Args:
            session: 資料庫會話
            skip: 跳過的記錄數
            limit: 限制的記錄數

        Returns:
            記錄列表
        """
        return (
            session.query(cls)
            .filter(cls.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @classmethod
    def count(cls, session: Session) -> int:
        """
        計算記錄總數

        Args:
            session: 資料庫會話

        Returns:
            記錄總數
        """
        return session.query(cls).filter(cls.is_deleted == False).count()

    def __repr__(self) -> str:
        """字串表示"""
        return f"<{self.__class__.__name__}(id={self.id})>"
