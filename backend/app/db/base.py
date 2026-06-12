from datetime import datetime
from typing import Optional, list
from sqlalchemy import String, Text, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)


    threads: Mapped[list["ThreadModel"]] = relationship("ThreadModel", back_populates="category", cascade="all, delete-orphan")


class ThreadModel(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

 
    category: Mapped["CategoryModel"] = relationship("CategoryModel", back_populates="threads")
    author: Mapped[Optional["UserModel"]] = relationship("UserModel", back_populates="threads")
    replies: Mapped[list["ReplyModel"]] = relationship("ReplyModel", back_populates="thread", cascade="all, delete-orphan")


class ReplyModel(Base):
    __tablename__ = "replies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    thread_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("replies.id", ondelete="CASCADE"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now(), nullable=True)


    thread: Mapped["ThreadModel"] = relationship("ThreadModel", back_populates="replies")
    author: Mapped[Optional["UserModel"]] = relationship("UserModel", back_populates="replies")
    

    parent: Mapped[Optional["ReplyModel"]] = relationship("ReplyModel", remote_side=[id], back_populates="children")
    children: Mapped[list["ReplyModel"]] = relationship("ReplyModel", back_populates="parent", cascade="all, delete-orphan")