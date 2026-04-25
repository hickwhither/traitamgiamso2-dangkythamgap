from flask import *
# from flask_login import current_user

from website import db
from website.models import *

bp = Blueprint('views', __name__, url_prefix='/')

@bp.app_errorhandler(404)
def _404(e):
    return render_template("404.html")

@bp.route('/')
def home():
    return render_template('index.html')



@bp.route('/register', methods=['GET'])
def register_form():
    return render_template('form.html')
