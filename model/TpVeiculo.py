from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR
from model.Base import Base

class TpVeiculo(Base):
    __tablename__ = "TPVEICULO"
    IDTPVEICULO:  Mapped[int] = mapped_column(INTEGER,      nullable=False, primary_key=True)
    DSTPVEICULO:  Mapped[str] = mapped_column(VARCHAR(100), nullable=False)