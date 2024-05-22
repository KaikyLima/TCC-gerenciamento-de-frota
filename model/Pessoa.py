from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, DATE, VARCHAR, CHAR
from model.Base import Base
from datetime import datetime
class Pessoa(Base):
    __tablename__ = "PESSOA"
    IDPESSOA:      Mapped[int]      = mapped_column(INTEGER,      nullable=False, primary_key=True)
    NMPESSOA:      Mapped[str]      = mapped_column(VARCHAR(100), nullable=False)
    NRCPF:         Mapped[str]      = mapped_column(CHAR(11),     nullable=False)
    DTNASCIMENTO:  Mapped[datetime] = mapped_column(DATE,         nullable=False)