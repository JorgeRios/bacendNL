from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class TblRequisicion(Base):
    __tablename__ = "tblRequisicion"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")


# {'fecha': '12/03/2024', 'estatus': 'elaborada', 'departamento': 'dep1', 'ramo': 1, 'motivo': 'moivo1', 'grupoProd': 'grupo1', 'consecutivo': '1', 'direccion': 'Direc1', 'proyecto': 'proyecto1',
 #        'fechaEntrega': '', 'oficinaEntrega': 'oficina1 ', 'tipoProd': 'tipo1', 'productos': [{'label': 'The Shawshank Redemption', 'year': 1994}], 'comentario': 'comentario1', 'solicitante': 'usuario', 'archivo': {}}
