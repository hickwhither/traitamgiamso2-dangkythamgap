from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import os, importlib
from sqlalchemy import text
db = SQLAlchemy()


def create_database(app):
    with app.app_context():
        db.create_all()
    print("Database created")


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    # Loading bp
    for brp in os.listdir(os.path.dirname('./website/blueprints/')):
        if brp[0] == '_' or brp[-3:] != '.py':
            continue
        brp = brp[:-3]
        imported = importlib.import_module(f".{brp}", package='website.blueprints')
        if hasattr(imported, 'bp'):
            app.register_blueprint(getattr(imported, 'bp'))

    # from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)

    from .models import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    @app.cli.command("create-admin")
    def create_admin_command():
        """Tạo tài khoản admin từ command line."""
        import click
        from werkzeug.security import generate_password_hash
        from .models import AdminUser

        username = click.prompt("Admin username", type=str).strip()
        password = click.prompt("Admin password", hide_input=True, confirmation_prompt=True).strip()

        if not username or not password:
            raise click.ClickException("Username/password không được để trống")

        existing = AdminUser.query.filter_by(username=username).first()
        if existing:
            raise click.ClickException("Username đã tồn tại")

        admin = AdminUser(username=username, password_hash=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Đã tạo admin: {username}")

    return app
