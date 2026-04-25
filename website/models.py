import sqlalchemy
db: sqlalchemy

from website import db
from flask_login import UserMixin

from datetime import date

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.mutable import *

class Form(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    hovaten_thannhan: Mapped[str] = mapped_column(nullable=False)
    ngaysinh_thannhan: Mapped[date] = mapped_column(Date)
    noidangkythuongtru_thannhan: Mapped[str] = mapped_column(nullable=False)
    cccdcmnd_thannhan: Mapped[str] = mapped_column(nullable=False)
    quanhephamnhan: Mapped[str] = mapped_column(nullable=False)

    hovaten_canphamnhan: Mapped[str] = mapped_column(nullable=False)
    ngaysinh_canphamnhan: Mapped[date] = mapped_column(Date)
    noidangkythuongtru_canphamnhan: Mapped[str] = mapped_column(nullable=False)
    toidanh: Mapped[str] = mapped_column(nullable=False)
    ngaybat: Mapped[date] = mapped_column(Date)

    ngaythamgap: Mapped[date] = mapped_column(Date)
    buoi: Mapped[str] = mapped_column(nullable=False) # sang / chieu


