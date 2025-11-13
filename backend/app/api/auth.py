"""
认证API路由层

负责处理用户认证相关的HTTP请求，包括用户注册、登录、登出、状态检查等功能。
严格遵循路由层和服务层分离的设计原则。
"""

from flask import Blueprint, request, make_response
from datetime import datetime, UTC
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app.service.auth_service import auth_service
from app.utils.responses import success, fail
from app.exception.api_exception import ApiException

# 创建认证路由蓝图
bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def get_session_token():
    """
    从请求头中获取会话令牌
    
    Returns:
        str: 会话令牌，如果不存在则返回None
    """
    # 从Authorization头获取Bearer token
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]  # 移除 'Bearer ' 前缀
    
    # 从Cookie中获取token
    return request.cookies.get('session_token')


@bp.route("/register", methods=["POST"])
def register():
    """
    用户注册接口
    
    POST /api/auth/register
    
    Headers:
        Content-Type: application/json
        
    Body:
        {
            "username": "testuser",
            "nickname": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "avatar": "/static/avatars/default.jpg",
            "permission": 1
        }
        
    Returns:
        JSON: 注册结果响应
        
    Example:
        POST /api/auth/register
        Content-Type: application/json
        
        Body:
        {
            "username": "testuser",
            "nickname": "Test User", 
            "email": "test@example.com",
            "password": "password123"
        }
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "user_id": 3,
                "username": "testuser",
                "nickname": "Test User",
                "email": "test@example.com",
                "created_at": "2024-01-15T12:00:00"
            }
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return fail(400, "请求数据不能为空")
        
        # 必填字段验证
        required_fields = ['username', 'nickname', 'email', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return fail(400, f"缺少必填字段: {', '.join(missing_fields)}")
        
        result = auth_service.register_user(data)
        
        return success(result, "用户注册成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/login", methods=["POST"])
def login():
    """
    用户登录接口
    
    POST /api/auth/login
    
    Headers:
        Content-Type: application/json
        
    Body:
        {
            "username": "admin",
            "password": "admin123"
        }
        
    Returns:
        JSON: 登录结果响应，包含会话令牌
        
    Example:
        POST /api/auth/login
        Content-Type: application/json
        
        Body:
        {
            "username": "admin",
            "password": "admin123"
        }
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "token": "abc123...",
                "user": {
                    "id": 1,
                    "username": "admin",
                    "nickname": "Administrator",
                    "avatar": "/static/avatars/admin.jpg",
                    "permission": 3
                },
                "expires_at": "2024-01-22T10:30:00"
            }
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return fail(400, "请求数据不能为空")
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return fail(400, "用户名和密码不能为空")
        
        login_result = auth_service.login_user(username, password)
        access_token = create_access_token(identity=str(login_result['user']['id']))
        login_result['token'] = access_token
        response = make_response(success(login_result, "登录成功"))
        response.set_cookie('session_token', access_token, max_age=7*24*60*60, httponly=True, secure=False, samesite='Lax')
        return response
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/logout", methods=["POST"])
def logout():
    """
    用户登出接口
    
    POST /api/auth/logout
    
    Headers:
        Authorization: Bearer {session_token}
        
    Returns:
        JSON: 登出结果响应
        
    Example:
        POST /api/auth/logout
        Headers: Authorization: Bearer abc123...
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "logged_out": true
            }
        }
    """
    try:
        # 获取会话令牌
        session_token = get_session_token()
        if not session_token:
            return fail(401, "未提供会话令牌")
        
        # 调用服务层进行用户登出
        logout_success = auth_service.logout_user(session_token)
        
        if not logout_success:
            return fail(400, "登出失败，会话可能已失效")
        
        # 创建响应并清除Cookie
        response = make_response(success({"logged_out": True}, "登出成功"))
        response.set_cookie('session_token', '', expires=0)
        
        return response
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/status", methods=["GET"])
@jwt_required()
def check_status():
    """
    检查登录状态接口
    
    GET /api/auth/status
    
    Headers:
        Authorization: Bearer {session_token}
        
    Returns:
        JSON: 认证状态响应
        
    Example:
        GET /api/auth/status
        Headers: Authorization: Bearer abc123...
        
        Response (已登录):
        {
            "code": 200,
            "message": "success",
            "data": {
                "is_authenticated": true,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "nickname": "Administrator",
                    "avatar": "/static/avatars/admin.jpg",
                    "permission": 3
                },
                "session": {
                    "token": "abc123...",
                    "created_at": "2024-01-15T10:30:00",
                    "expires_at": "2024-01-22T10:30:00"
                }
            }
        }
        
        Response (未登录):
        {
            "code": 200,
            "message": "success",
            "data": {
                "is_authenticated": false,
                "user": null,
                "session": null
            }
        }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return fail(401, "未认证")
        from app.service.user_service import user_service
        try:
            user = user_service.get_user_by_id(int(user_id))
        except Exception:
            user = None
        if not user:
            return fail(401, "用户不存在或未认证")
        jwt_payload = get_jwt()
        exp = jwt_payload.get('exp')
        expires_at = datetime.fromtimestamp(exp, tz=UTC).isoformat() if exp else None
        return success({
            'is_authenticated': True,
            'isLoggedIn': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'nickname': user['nickname'],
                'avatar': user.get('avatar'),
                'permission': user.get('permission', 1)
            },
            'session': {
                'token': None,
                'created_at': None,
                'expires_at': expires_at
            }
        }, "获取认证状态成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/refresh", methods=["POST"])
@jwt_required()
def refresh_session():
    """
    刷新会话接口
    
    POST /api/auth/refresh
    
    Headers:
        Authorization: Bearer {session_token}
        
    Returns:
        JSON: 刷新结果响应
        
    Example:
        POST /api/auth/refresh
        Headers: Authorization: Bearer abc123...
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "token": "abc123...",
                "expires_at": "2024-01-22T10:30:00",
                "refreshed_at": "2024-01-15T12:00:00"
            }
        }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return fail(401, "未认证")
        new_token = create_access_token(identity=str(user_id))
        jwt_payload = get_jwt()
        exp = jwt_payload.get('exp')
        response = make_response(success({
            'token': new_token,
            'expires_at': datetime.fromtimestamp(exp, tz=UTC).isoformat() if exp else None,
            'refreshed_at': datetime.now(UTC).isoformat()
        }, "会话刷新成功"))
        response.set_cookie('session_token', new_token, max_age=7*24*60*60, httponly=True, secure=False, samesite='Lax')
        return response
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/validate", methods=["POST"])
@jwt_required()
def validate_token():
    """
    验证令牌接口
    
    POST /api/auth/validate
    
    Headers:
        Content-Type: application/json
        
    Body:
        {
            "token": "abc123..."
        }
        
    Returns:
        JSON: 验证结果响应
        
    Example:
        POST /api/auth/validate
        Content-Type: application/json
        
        Body:
        {
            "token": "abc123..."
        }
        
        Response (有效):
        {
            "code": 200,
            "message": "success",
            "data": {
                "valid": true,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "nickname": "Administrator",
                    "avatar": "/static/avatars/admin.jpg",
                    "permission": 3
                }
            }
        }
        
        Response (无效):
        {
            "code": 200,
            "message": "success",
            "data": {
                "valid": false,
                "user": null
            }
        }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return success({"valid": False, "user": None}, "未认证")
        from app.service.user_service import user_service
        try:
            user = user_service.get_user_by_id(int(user_id))
        except Exception:
            user = None
        if not user:
            return success({"valid": False, "user": None}, "用户不存在")
        return success({
            "valid": True,
            "user": {
                'id': user['id'],
                'username': user['username'],
                'nickname': user['nickname'],
                'avatar': user.get('avatar'),
                'permission': user.get('permission', 1)
            }
        }, "令牌验证成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")
