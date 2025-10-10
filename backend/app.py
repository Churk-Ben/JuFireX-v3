from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.api.user import bp as user_bp
from app.api.post import bp as post_bp
from app.exception.api_exception import ApiException
from app.model import db
from config import DevelopmentConfig, TestingConfig, ProductionConfig


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    # Load config by name
    cfg = (config_name or app.config.get("ENV") or "development").lower()
    if cfg == "production":
        app.config.from_object(ProductionConfig())
    elif cfg == "testing":
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    # Init extensions
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    # Global error handler for ApiException
    @app.errorhandler(ApiException)
    def handle_api_exception(err: ApiException):
        return jsonify({"code": err.code, "message": err.message}), err.code

    # Health check
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)