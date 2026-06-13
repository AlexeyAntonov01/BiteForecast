from sqlalchemy import String, ForeignKey,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import datetime

class Base(DeclarativeBase):
    pass

class FishTable(Base):
    __tablename__ = "FishTable"

    fishId : Mapped[int] = mapped_column(primary_key=True)
    fish_name : Mapped[str] = mapped_column(String(50),nullable=False)

class FishRulesTable(Base):
    __tablename__ = "FishRulesTable"

    ruleId : Mapped[int] = mapped_column(primary_key=True)
    fishId : Mapped[int] = mapped_column(ForeignKey("FishTable.fishId", ondelete="CASCADE"))
    ReservoirId : Mapped[int] =  mapped_column(ForeignKey("ReservoirTypeTable.ReservoirId", ondelete="RESTRICT"))
    season : Mapped[str] =  mapped_column(String(10))
    rules_config: Mapped[dict] = mapped_column(JSONB,nullable=False)
    modified_datetime : Mapped[datetime.datetime] = mapped_column(nullable=False,default=datetime.datetime.now)

    __table_args__ = (
        UniqueConstraint(
            "fishId", "ReservoirId", "season", 
            name="uq_fish_waterbody_season"
        ),
    )

class ReservoirTypeTable(Base):
    __tablename__ = "ReservoirTypeTable"

    ReservoirId : Mapped[int] = mapped_column(primary_key=True)
    Reservoir_name: Mapped[str] = mapped_column(String(50),nullable=False)