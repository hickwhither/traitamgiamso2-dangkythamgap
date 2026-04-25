from datetime import date

from website import db

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column


class VisitRegistration(db.Model):
    __tablename__ = "visit_registrations"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Thân nhân can phạm nhân
    than_nhan_ho_ten: Mapped[str] = mapped_column(nullable=False)
    than_nhan_ngay_sinh: Mapped[date] = mapped_column(Date, nullable=False)
    than_nhan_noi_dang_ky_thuong_tru: Mapped[str] = mapped_column(nullable=False)
    than_nhan_so_cccd_cmnd: Mapped[str] = mapped_column(nullable=False)
    than_nhan_quan_he_voi_can_pham_nhan: Mapped[str] = mapped_column(nullable=False)

    # Can phạm nhân
    can_pham_nhan_ho_ten: Mapped[str] = mapped_column(nullable=False)
    can_pham_nhan_ngay_sinh: Mapped[date] = mapped_column(Date, nullable=False)
    can_pham_nhan_noi_dang_ky_thuong_tru: Mapped[str] = mapped_column(nullable=False)
    can_pham_nhan_toi_danh: Mapped[str] = mapped_column(nullable=False)
    can_pham_nhan_ngay_bat: Mapped[date] = mapped_column(Date, nullable=False)

    # Thời gian đăng ký thăm gặp
    thoi_gian_tham_gap_ngay: Mapped[date] = mapped_column(Date, nullable=False)
    thoi_gian_tham_gap_buoi: Mapped[str] = mapped_column(nullable=False)  # sáng / chiều
