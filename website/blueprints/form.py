from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from website import db
from website.models import AdminUser, VisitRegistration

bp = Blueprint('views', __name__, url_prefix='/')

DATE_FIELDS = (
    "than_nhan_ngay_sinh",
    "can_pham_nhan_ngay_sinh",
    "can_pham_nhan_ngay_bat",
    "thoi_gian_tham_gap_ngay",
)


def _parse_vn_date(date_str: str):
    """
    Parse ngày tháng theo định dạng dd/mm/yyyy từ form.
    Hỗ trợ thêm yyyy-mm-dd để tương thích dữ liệu cũ.
    """
    cleaned = date_str.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    raise ValueError("invalid date format")


@bp.app_errorhandler(404)
def _404(e):
    return render_template("404.html")




@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.registration_management'))

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    user = AdminUser.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        flash('Sai tài khoản hoặc mật khẩu.', 'danger')
        return render_template('login.html'), 401

    login_user(user)
    flash('Đăng nhập thành công.', 'success')
    return redirect(url_for('views.registration_management'))


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất.', 'success')
    return redirect(url_for('views.home'))

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

    for field in DATE_FIELDS:
        try:
            form_data[field] = _parse_vn_date(form_data[field])
        except ValueError:
            flash('Ngày không hợp lệ. Vui lòng chọn ngày từ lịch hoặc nhập theo định dạng dd/mm/yyyy.', 'danger')
            return render_template('form.html', form_data=form_data), 400

    registration = VisitRegistration(
        **form_data,
        trang_thai=VisitRegistration.STATUS_PROCESSING,
    )
    db.session.add(registration)
    db.session.commit()

    flash('Đăng ký thăm gặp thành công.', 'success')
    return redirect(url_for('views.registration_detail', registration_id=registration.id))


@bp.route('/register/<int:registration_id>', methods=['GET'])
def registration_detail(registration_id: int):
    registration = VisitRegistration.query.get_or_404(registration_id)
    return render_template('registration_detail.html', registration=registration)


@bp.route('/manage/registrations', methods=['GET'])
@login_required
def registration_management():
    registrations = VisitRegistration.query.order_by(VisitRegistration.id.desc()).all()
    return render_template(
        'registration_management.html',
        registrations=registrations,
        status_choices=VisitRegistration.STATUS_CHOICES,
    )


@bp.route('/manage/registrations/<int:registration_id>/status', methods=['POST'])
@login_required
def update_registration_status(registration_id: int):
    registration = VisitRegistration.query.get_or_404(registration_id)
    new_status = request.form.get('trang_thai', '').strip()
    valid_statuses = {status for status, _ in VisitRegistration.STATUS_CHOICES}

    if new_status not in valid_statuses:
        flash('Trạng thái không hợp lệ.', 'danger')
        return redirect(url_for('views.registration_management'))

    registration.trang_thai = new_status
    db.session.commit()

    flash(f'Đã cập nhật trạng thái hồ sơ #{registration.id}.', 'success')
    return redirect(url_for('views.registration_management'))
