from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, text
from datetime import datetime
from typing import Annotated

# SQLAlchemyの型アノテーション
# タイムスタンプ型: created_at
created_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.now()),
]

# タイムスタンプ型: updated_at
updated_at = Annotated[
    datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), # MariaDB/MySQL用
        # server_onupdate=func.now() # PostgreSQL用 (こちらが標準的だが、環境差異をコメントで残す)
    ),
]

class Base(DeclarativeBase):
    pass 