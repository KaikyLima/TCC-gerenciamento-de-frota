from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR, ForeignKey
from model.Base import Base
from model.Funcionario import Funcionario
from sqlalchemy.schema import Sequence

class Motorista(Base):
    __tablename__ = "MOTORISTA"
    IDMOTORISTA:            Mapped[int]   = mapped_column(INTEGER,  Sequence('MOTORISTA_IDMOTORISTA_SEQ')    ,nullable=False, primary_key=True)
    NMMOTORISTA:            Mapped[str]   = mapped_column(VARCHAR(100), nullable=False)
    FUNCIONARIO_NRMATRICULA:Mapped[int]   = mapped_column(INTEGER, ForeignKey(Funcionario.NRMATRICULA), nullable=False)