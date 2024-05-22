from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, DATE, ForeignKey
from model.Base import Base
from datetime import datetime
from model.Veiculo_model import Veiculo
from sqlalchemy.schema import Sequence
class CtVinculo(Base):
    __tablename__ = "CTVINCULO"
    ID:                     Mapped[int]      = mapped_column(INTEGER, Sequence('CTVINCULO_ID_SEQ'), nullable=False, primary_key=True)
    DTVINCULO:              Mapped[datetime] = mapped_column(DATE,    nullable=False)
    DTDESVINCULO:           Mapped[datetime] = mapped_column(DATE,    nullable=True)
    VEICULO_IDVEICULO:       Mapped[int]      = mapped_column(INTEGER, ForeignKey(Veiculo.IDVEICULO), nullable=False)
    MOTORISTA_IDMOTORISTA:  Mapped[int]      = mapped_column(INTEGER, ForeignKey(Veiculo.IDVEICULO), nullable=False)