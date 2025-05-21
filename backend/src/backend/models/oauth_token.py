from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

from .base import Base, created_at, updated_at

if TYPE_CHECKING:
    from .user import User # noqa: F401

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="トークンID (主キー)")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="ユーザーID (USERS.idへの外部キー)")
    provider: Mapped[str] = mapped_column(String(50), nullable=False, comment="プロバイダー名 (例: google, facebook)")
    access_token: Mapped[str] = mapped_column(String(1024), nullable=False, comment="アクセストークン") # トークン長は余裕を持つ
    refresh_token: Mapped[str | None] = mapped_column(String(1024), comment="リフレッシュトークン (オプション)")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, comment="有効期限 (オプション)")
    scopes: Mapped[str | None] = mapped_column(String(1024), comment="スコープ (スペース区切り、オプション)")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["User"] = relationship(back_populates="oauth_tokens")

    def __repr__(self) -> str:
        return f"OAuthToken(id={self.id!r}, user_id={self.user_id!r}, provider={self.provider!r})" 