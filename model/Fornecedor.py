from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR, CHAR
from sqlalchemy.schema import Sequence
from model.Base import Base

class Fornecedor(Base):
    __tablename__ = "FORNECEDOR"
    COD:            Mapped[int] = mapped_column(INTEGER, Sequence('FORNECEDOR_COD_SEQ'), nullable=False, primary_key=True)
    CNPJ:           Mapped[str] = mapped_column(CHAR(14),  nullable=False)
    NMFORNECEDOR:   Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
