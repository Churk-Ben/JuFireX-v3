"""
用户API路由层

负责处理用户相关的HTTP请求，包括用户信息获取、用户管理等功能。
严格遵循路由层和服务层分离的设计原则。
"""

from flask import Blueprint, request, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.user_service import user_service
from app.service.auth_service import auth_service
from app.utils.responses import success, fail
from app.exception.api_exception import ApiException

# 创建用户路由蓝图
bp = Blueprint("user", __name__, url_prefix="/api/user")


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


@bp.route("/<int:user_id>", methods=["GET"])
def get_user_info(user_id):
    """
    获取用户信息接口
    
    GET /api/user/{user_id}
    
    Args:
        user_id (int): 用户ID
        
    Returns:
        JSON: 用户信息响应
        
    Example:
        GET /api/user/1
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "id": 1,
                "username": "admin",
                "nickname": "Administrator",
                "avatar": "/static/avatars/admin.jpg",
                "permission": 3,
                "created_at": "2024-01-01T00:00:00"
            }
        }
    """
    try:
        # 获取用户公开信息
        user_info = user_service.get_user_public_info(user_id)
        
        if not user_info:
            return fail(404, "用户不存在")
        
        return success(user_info, "获取用户信息成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/session", methods=["GET"])
@jwt_required()
def get_user_session():
    """
    获取用户session信息接口
    
    GET /api/user/session
    
    Headers:
        Authorization: Bearer {session_token}
        
    Returns:
        JSON: 用户会话信息响应
        
    Example:
        GET /api/user/session
        Headers: Authorization: Bearer abc123...
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
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
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return fail(401, "未认证")
        current_user = user_service.get_user_by_id(user_id)
        if not current_user:
            return fail(401, "用户不存在或会话无效")
        return success({
            'user': {
                'id': current_user['id'],
                'username': current_user['username'],
                'nickname': current_user['nickname'],
                'avatar': current_user.get('avatar'),
                'permission': current_user.get('permission', 1)
            },
            'session': None
        }, "获取会话信息成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/info", methods=["GET"])
@jwt_required()
def get_user_detailed_info():
    """
    获取用户详细信息接口
    
    GET /api/user/info
    
    Headers:
        Authorization: Bearer {session_token}
        
    Returns:
        JSON: 用户详细信息响应
        
    Example:
        GET /api/user/info
        Headers: Authorization: Bearer abc123...
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "id": 1,
                "username": "admin",
                "nickname": "Administrator",
                "email": "admin@jufirex.com",
                "avatar": "/static/avatars/admin.jpg",
                "permission": 3,
                "is_active": true,
                "is_verified": true,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
                "last_login_at": "2024-01-15T10:30:00"
            }
        }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return fail(401, "未认证")
        user_info = user_service.get_user_by_id(user_id)
        if not user_info:
            return fail(401, "用户不存在或会话无效")
        return success(user_info, "获取用户详细信息成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    """
    更新用户资料接口
    
    PUT /api/user/profile
    
    Headers:
        Authorization: Bearer {session_token}
        Content-Type: application/json
        
    Body:
        {
            "nickname": "新昵称",
            "avatar": "/static/avatars/new_avatar.jpg"
        }
        
    Returns:
        JSON: 更新结果响应
        
    Example:
        PUT /api/user/profile
        Headers: 
            Authorization: Bearer abc123...
            Content-Type: application/json
        Body:
        {
            "nickname": "新昵称",
            "avatar": "/static/avatars/new_avatar.jpg"
        }
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "id": 1,
                "username": "admin",
                "nickname": "新昵称",
                "email": "admin@jufirex.com",
                "avatar": "/static/avatars/new_avatar.jpg",
                "permission": 3,
                "updated_at": "2024-01-15T11:00:00"
            }
        }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return fail(401, "未认证")
        current_user = user_service.get_user_by_id(user_id)
        if not current_user:
            return fail(401, "用户不存在或会话无效")
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return fail(400, "请求数据不能为空")
        
        # 更新用户信息
        updated_user = user_service.update_user_info(current_user['id'], data)
        
        return success(updated_user, "用户资料更新成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")


@bp.route("/list", methods=["GET"])
@jwt_required()
def get_users_list():
    """
    获取用户列表接口（管理员功能）
    
    GET /api/user/list?page=1&per_page=10&search=keyword
    
    Headers:
        Authorization: Bearer {session_token}
        
    Query Parameters:
        page (int, optional): 页码，默认为1
        per_page (int, optional): 每页数量，默认为10
        search (str, optional): 搜索关键词
        
    Returns:
        JSON: 用户列表响应
        
    Example:
        GET /api/user/list?page=1&per_page=10&search=admin
        Headers: Authorization: Bearer abc123...
        
        Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "users": [...],
                "pagination": {
                    "page": 1,
                    "per_page": 10,
                    "total": 2,
                    "pages": 1
                }
            }
        }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return fail(401, "未认证")
        current_user = user_service.get_user_by_id(user_id)
        if not current_user:
            return fail(401, "用户不存在或会话无效")
        
        # 检查权限（只有管理员可以查看用户列表）
        if current_user.get('permission', 0) < 2:
            return fail(403, "权限不足，无法访问用户列表")
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', None)
        
        # 参数验证
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        # 获取用户列表
        users_data = user_service.get_users_list(page, per_page, search)
        
        return success(users_data, "获取用户列表成功")
        
    except ApiException as e:
        return fail(e.code, e.message, e.data if hasattr(e, 'data') else None)
    except Exception as e:
        return fail(500, f"服务器内部错误: {str(e)}")
