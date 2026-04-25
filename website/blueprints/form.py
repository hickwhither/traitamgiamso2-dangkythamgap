from flask import Blueprint, flash, redirect, render_template, request, url_for

from website import db
from website.models import VisitRegistration

bp = Blueprint('views', __name__, url_prefix='/')


@bp.app_errorhandler(404)
def _404(e):
    return render_template("404.html")


@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register_form():
    if request.method == 'GET':
        return render_template('form.html')

    form_data = {
        "than_nhan_ho_ten": request.form.get("than_nhan_ho_ten", "").strip(),
        "than_nhan_ngay_sinh": request.form.get("than_nhan_ngay_sinh", "").strip(),
        "than_nhan_noi_dang_ky_thuong_tru": request.form.get("than_nhan_noi_dang_ky_thuong_tru", "").strip(),
        "than_nhan_so_cccd_cmnd": request.form.get("than_nhan_so_cccd_cmnd", "").strip(),
        "than_nhan_quan_he_voi_can_pham_nhan": request.form.get("than_nhan_quan_he_voi_can_pham_nhan", "").strip(),
        "can_pham_nhan_ho_ten": request.form.get("can_pham_nhan_ho_ten", "").strip(),
        "can_pham_nhan_ngay_sinh": request.form.get("can_pham_nhan_ngay_sinh", "").strip(),
        "can_pham_nhan_noi_dang_ky_thuong_tru": request.form.get("can_pham_nhan_noi_dang_ky_thuong_tru", "").strip(),
        "can_pham_nhan_toi_danh": request.form.get("can_pham_nhan_toi_danh", "").strip(),
        "can_pham_nhan_ngay_bat": request.form.get("can_pham_nhan_ngay_bat", "").strip(),
        "thoi_gian_tham_gap_ngay": request.form.get("thoi_gian_tham_gap_ngay", "").strip(),
        "thoi_gian_tham_gap_buoi": request.form.get("thoi_gian_tham_gap_buoi", "").strip(),
    }

    if any(not value for value in form_data.values()):
        flash('Vui lòng nhập đầy đủ thông tin bắt buộc.', 'danger')
        return render_template('form.html', form_data=form_data), 400

    registration = VisitRegistration(**form_data)
    db.session.add(registration)
    db.session.commit()

    flash('Đăng ký thăm gặp thành công.', 'success')
    return redirect(url_for('views.registration_detail', registration_id=registration.id))


@bp.route('/register/<int:registration_id>', methods=['GET'])
def registration_detail(registration_id: int):
    registration = VisitRegistration.query.get_or_404(registration_id)
    return render_template('registration_detail.html', registration=registration)
