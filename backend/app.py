from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from app.model import db
from app.model.user import User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
JWTManager(app)
CORS(app)
db.init_app(app)
Migrate(app, db)
with app.app_context():
  db.create_all()
  if not User.query.filter_by(username="admin").first():
    admin = User(
      username="admin",
      nickname="Administrator",
      email="admin@jufirex.com",
      password=generate_password_hash("admin123"),
      avatar="/static/avatars/admin.jpg",
      permission=3,
      is_active=True,
      is_verified=True
    )
    db.session.add(admin)
    db.session.commit()

# 注册蓝图
from app.api.user import bp as user_bp
from app.api.auth import bp as auth_bp
from app.api.post import bp as post_bp

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)

@app.get("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
