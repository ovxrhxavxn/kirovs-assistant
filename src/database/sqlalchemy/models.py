from sqlalchemy.orm import Mapped, mapped_column

from .annotated_types import intpk
from .setup import Base


class AuthenticatedUser(Base):

    __tablename__ = 'authenticated_users'

    id: Mapped[intpk]
    nickname: Mapped[str] = mapped_column(unique=True)
    domain_name: Mapped[str] = mapped_column(unique=True)