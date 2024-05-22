from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR
from sqlalchemy.schema import Sequence
from model.Base import Base

class Uf(Base):
    __tablename__ = "UF"
    CDUF:    Mapped[int] = mapped_column(INTEGER,Sequence('UF_CDUF_SEQ'), nullable=False, primary_key=True)
    NMUF:    Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    DSSIGLA: Mapped[str] = mapped_column(VARCHAR(2),   nullable=False)