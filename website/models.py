from datetime import date

from website import db

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column


class VisitRegistration(db.Model):
    __tablename__ = "visit_registrations"

    STATUS_INCOMPLETE = "chua_day_du"
    STATUS_PROCESSING = "dang_xu_ly"
    STATUS_CONFIRMED = "da_xac_nhan"
    STATUS_REJECTED = "da_tu_choi"

    STATUS_CHOICES = (
        (STATUS_INCOMPLETE, "Thiếu thông tin"),
        (STATUS_PROCESSING, "Đang xử lý"),
        (STATUS_CONFIRMED, "Đã xác nhận"),
        (STATUS_REJECTED, "Đã từ chối"),
    )

    STATUS_LABELS = dict(STATUS_CHOICES)
    STATUS_TAG_CLASSES = {
        STATUS_INCOMPLETE: "is-warning",
        STATUS_PROCESSING: "is-info",
        STATUS_CONFIRMED: "is-success",
        STATUS_REJECTED: "is-danger",
    }

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

    trang_thai: Mapped[str] = mapped_column(
        nullable=False,
        default=STATUS_PROCESSING,
        server_default=STATUS_PROCESSING,
    )

    @property
    def trang_thai_hien_thi(self) -> str:
        return self.STATUS_LABELS.get(self.trang_thai, self.trang_thai)

    @property
    def trang_thai_tag_class(self) -> str:
        return self.STATUS_TAG_CLASSES.get(self.trang_thai, "is-light")
