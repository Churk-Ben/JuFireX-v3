from flask import Blueprint
from app.utils import success

bp = Blueprint("post", __name__, url_prefix="/api/posts")


@bp.get("/")
def list_posts():
    # placeholder implementation
    return success({"items": []})