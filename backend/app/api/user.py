from flask import Blueprint, request
from app.service import user_service
from app.utils import success

bp = Blueprint("user", __name__, url_prefix="/api/users")


@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    token = user_service.login(email, password)
    return success({"token": token})