from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, created_at, updated_at

if TYPE_CHECKING:
    from .oauth_token import OAuthToken  # noqa: F401

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="ユーザーID (主キー)")
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False, comment="メールアドレス (ユニーク)")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="ハッシュ化されたパスワード")
    full_name: Mapped[str | None] = mapped_column(String(255), comment="氏名")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False, comment="アクティブフラグ")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False, comment="スーパーユーザーフラグ")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    oauth_tokens: Mapped[list["OAuthToken"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, full_name={self.full_name!r})" 