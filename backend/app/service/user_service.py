from app.model.user import User
from app.exception import ApiException
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token


def login(email: str | None, password: str | None) -> str:
    if not email or not password:
        raise ApiException(400, "邮箱或密码不能为空")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        raise ApiException(401, "邮箱或密码错误")
    return create_access_token(identity=user.id)