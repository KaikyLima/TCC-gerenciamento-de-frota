from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR, FLOAT, DATE, CHAR, ForeignKey
from model.Base import Base
from model.Fornecedor import Fornecedor
from model.Veiculo_model import Veiculo
from sqlalchemy.schema import Sequence
from datetime import datetime
class Despesas(Base):
    __tablename__ = "DESPESAS"
    COD:                Mapped[int]      = mapped_column(INTEGER, Sequence('DESPESAS_COD_SEQ'), nullable=False, primary_key=True)
    TPGASTOS:           Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)
    DTEMISSAO:          Mapped[datetime] = mapped_column(DATE,         nullable=False)
    NRNOTA:             Mapped[str]      = mapped_column(CHAR(10),     nullable=False)
    VALOR:              Mapped[int]      = mapped_column(FLOAT,        nullable=True)
    OBSERVACAO:         Mapped[str]      = mapped_column(VARCHAR(300), nullable=True)
    FORNECEDOR_COD:     Mapped[int]      = mapped_column(INTEGER, ForeignKey(Fornecedor.COD),    nullable=False)
    VEICULO_IDVEICULO:  Mapped[int]      = mapped_column(INTEGER, ForeignKey(Veiculo.IDVEICULO), nullable=False)


