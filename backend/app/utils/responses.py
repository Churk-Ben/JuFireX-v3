from flask import jsonify


def success(data=None, message: str = "ok"):
    return jsonify({"code": 200, "message": message, "data": data or {}}), 200


def fail(code: int = 400, message: str = "error", data=None):
    return jsonify({"code": code, "message": message, "data": data or {}}), code