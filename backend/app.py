from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 注册蓝图
from app.api.user import bp as user_bp
from app.api.auth import bp as auth_bp

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

@app.get("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
