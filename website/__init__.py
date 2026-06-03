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

    @app.cli.command("list-admins")
    def list_admins_command():
        """Hiển thị danh sách tài khoản admin."""
        import click
        from .models import AdminUser

        admins = AdminUser.query.order_by(AdminUser.id.asc()).all()
        if not admins:
            click.echo("Chưa có tài khoản admin nào.")
            return

        click.echo("Danh sách admin:")
        for admin in admins:
            click.echo(f"- id={admin.id}, username={admin.username}")

    @app.cli.command("delete-admin")
    def delete_admin_command():
        """Xóa tài khoản admin theo username hoặc id."""
        import click
        from .models import AdminUser

        identifier = click.prompt("Nhập username hoặc id admin cần xóa", type=str).strip()
        if not identifier:
            raise click.ClickException("Bạn phải nhập username hoặc id")

        admin = None
        if identifier.isdigit():
            admin = db.session.get(AdminUser, int(identifier))
        if admin is None:
            admin = AdminUser.query.filter_by(username=identifier).first()
        if admin is None:
            raise click.ClickException("Không tìm thấy admin cần xóa")

        db.session.delete(admin)
        db.session.commit()
        click.echo(f"Đã xóa admin: {admin.username} (id={admin.id})")
    
    @app.cli.command("change-admin-password")
    def change_admin_password_command():
        """Đổi mật khẩu tài khoản admin."""
        import click
        from werkzeug.security import generate_password_hash
        from .models import AdminUser

        identifier = click.prompt("Nhập username hoặc id admin cần đổi mật khẩu", type=str).strip()
        if not identifier:
            raise click.ClickException("Bạn phải nhập username hoặc id")

        admin = None
        if identifier.isdigit():
            admin = db.session.get(AdminUser, int(identifier))
        
        if admin is None:
            admin = AdminUser.query.filter_by(username=identifier).first()
            
        if admin is None:
            raise click.ClickException("Không tìm thấy tài khoản admin cần đổi mật khẩu")

        new_password = click.prompt("Nhập mật khẩu mới", hide_input=True, confirmation_prompt=True).strip()
        
        if not new_password:
            raise click.ClickException("Mật khẩu không được để trống")

        admin.password_hash = generate_password_hash(new_password)
        db.session.commit()
        click.echo(f"Đã đổi mật khẩu thành công cho admin: {admin.username} (id={admin.id})")

    return app
