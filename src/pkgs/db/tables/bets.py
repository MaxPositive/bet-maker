from decimal import Decimal
from .base import Base

from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column


class Bet(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[str] = mapped_column(index=True)
    bet_amount: Mapped[Decimal] = mapped_column(DECIMAL(scale=2))
    status: Mapped[str] = mapped_column(default="Not played", server_default="Not played")
