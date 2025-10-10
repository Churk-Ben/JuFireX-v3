from pathlib import Path
import importlib.util
import sys
from werkzeug.security import generate_password_hash


def load_create_app():
    backend_dir = Path(__file__).parent
    app_py = backend_dir / "app.py"
    spec = importlib.util.spec_from_file_location("app_module", app_py)
    app_module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules["app_module"] = app_module
    assert spec and spec.loader
    spec.loader.exec_module(app_module)  # type: ignore
    return app_module.create_app


def main():
    create_app = load_create_app()
    app = create_app("development")
    # Lazy imports to avoid package name collision with app package
    from app.model import db  # type: ignore
    from app.model.user import User  # type: ignore

    with app.app_context():
        db.create_all()
        email = "test@example.com"
        password = "password"
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            print(f"Seeded user: {email} / {password}")
        else:
            print("User already exists, skipping.")


if __name__ == "__main__":
    main()