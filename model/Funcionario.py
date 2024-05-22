from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, DATE, VARCHAR, CHAR, ForeignKey
from model.Base import Base
from datetime import datetime
from model.Pessoa import Pessoa
from sqlalchemy.schema import Sequence
class Funcionario(Base):
    __tablename__ = "FUNCIONARIO"
    NRMATRICULA:    Mapped[int]      = mapped_column(INTEGER, Sequence ('PESSOA_IDPESSOA_SEQ'),     nullable=False, primary_key=True)
    NMFUNCIONARIO:  Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)
    DSFUNCAO:       Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)
    DTADMISSAO:     Mapped[datetime] = mapped_column(DATE,         nullable=False)
    TPSITUACAO:     Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)
    PESSOA_IDPESSOA:Mapped[int]      = mapped_column(INTEGER, ForeignKey(Pessoa.IDPESSOA), nullable=False)