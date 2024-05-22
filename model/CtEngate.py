from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, DATE, ForeignKey
from model.Base import Base
from datetime import datetime
from model.Veiculo_model import Veiculo
from sqlalchemy.schema import Sequence

class CtEngate(Base):
    __tablename__ = "CTENGATE"
    ID:          Mapped[int]      = mapped_column(INTEGER,Sequence('CTENGATE_ID_SEQ'), nullable=False, primary_key=True)
    DTENGATE:    Mapped[datetime] = mapped_column(DATE,    nullable=False)
    DTDESENGATE: Mapped[datetime] = mapped_column(DATE,    nullable=True)
    NRFROTA:     Mapped[int]      = mapped_column(INTEGER, nullable=False)
    NRCONJUNTO:  Mapped[int]      = mapped_column(INTEGER, nullable=False)
    VEICULO_IDVEICULO:   Mapped[int]      = mapped_column(INTEGER, ForeignKey(Veiculo.IDVEICULO), nullable=False)