from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR, CHAR, DATE
from sqlalchemy.schema import Sequence
from model.Base import Base
from datetime import datetime
class Veiculo(Base):
    __tablename__ = 'VEICULO'
    IDVEICULO:     Mapped[int]      = mapped_column(INTEGER, Sequence('VEICULO_IDVEICULO_SEQ'), nullable=False, primary_key=True)
    NRPLACA:       Mapped[str]      = mapped_column(CHAR(7),      nullable=False, unique=True)
    DSMODELO:      Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)
    TPTRACAO:      Mapped[str]      = mapped_column(VARCHAR(40),  nullable=False)
    NRRENAVAM:     Mapped[int]      = mapped_column(CHAR(11),     nullable=False, unique=True)
    DTAQUISICAO:   Mapped[datetime] = mapped_column(DATE,         nullable=False)
    NRFROTA:       Mapped[int]      = mapped_column(INTEGER,      nullable=True)
    NRCONJUNTO:    Mapped[int]      = mapped_column(INTEGER,      nullable=True)
    NRCHASSI:      Mapped[str]      = mapped_column(VARCHAR(17),  nullable=False, unique=True)
    QTEIXO:        Mapped[int]      = mapped_column(INTEGER,      nullable=False)
    TPVEICULO:     Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)