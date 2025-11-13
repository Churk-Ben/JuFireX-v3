"""
用户服务层

负责处理用户相关的业务逻辑，包括用户信息获取、用户管理等功能。
暂时使用模拟数据，不连接实际数据库。
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from app.exception.api_exception import ApiException
from app.model import db
from app.model.user import User


class UserService:
    """用户服务类"""
    
    def __init__(self):
        pass
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        根据用户ID获取用户信息
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息字典，如果用户不存在则返回None
            
        Raises:
            ApiException: 当用户ID无效时抛出异常
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ApiException(400, "用户ID必须是正整数")
        
        user = db.session.get(User, user_id)
        if not user:
            return None
        return user.to_dict()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        根据用户名获取用户信息
        
        Args:
            username (str): 用户名
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息字典，如果用户不存在则返回None
        """
        if not username or not isinstance(username, str):
            return None
            
        user = User.query.filter_by(username=username).first()
        return user.to_dict() if user else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        根据邮箱获取用户信息
        
        Args:
            email (str): 邮箱地址
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息字典，如果用户不存在则返回None
        """
        if not email or not isinstance(email, str):
            return None
            
        user = User.query.filter_by(email=email).first()
        return user.to_dict() if user else None
    
    def get_user_public_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        获取用户公开信息（不包含敏感数据）
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Optional[Dict[str, Any]]: 用户公开信息字典
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
            
        # 返回公开信息，排除敏感字段
        return {
            'id': user['id'],
            'username': user['username'],
            'nickname': user['nickname'],
            'avatar': user['avatar'],
            'permission': user['permission'],
            'created_at': user['created_at']
        }
    
    def validate_user_data(self, user_data: Dict[str, Any], is_update: bool = False) -> Dict[str, str]:
        """
        验证用户数据
        
        Args:
            user_data (Dict[str, Any]): 用户数据
            is_update (bool): 是否为更新操作
            
        Returns:
            Dict[str, str]: 验证错误信息，如果验证通过则返回空字典
        """
        errors = {}
        
        # 验证用户名
        if 'username' in user_data:
            username = user_data.get('username', '').strip()
            if not username:
                errors['username'] = '用户名不能为空'
            elif len(username) < 3 or len(username) > 50:
                errors['username'] = '用户名长度必须在3-50个字符之间'
            elif not re.match(r'^[a-zA-Z0-9_]+$', username):
                errors['username'] = '用户名只能包含字母、数字和下划线'
            elif not is_update and self.get_user_by_username(username):
                errors['username'] = '用户名已存在'
        elif not is_update:
            errors['username'] = '用户名不能为空'
        
        # 验证昵称
        if 'nickname' in user_data:
            nickname = user_data.get('nickname', '').strip()
            if not nickname:
                errors['nickname'] = '昵称不能为空'
            elif len(nickname) > 100:
                errors['nickname'] = '昵称长度不能超过100个字符'
        elif not is_update:
            errors['nickname'] = '昵称不能为空'
        
        # 验证邮箱
        if 'email' in user_data:
            email = user_data.get('email', '').strip()
            if not email:
                errors['email'] = '邮箱不能为空'
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors['email'] = '邮箱格式不正确'
            elif not is_update and self.get_user_by_email(email):
                errors['email'] = '邮箱已存在'
        elif not is_update:
            errors['email'] = '邮箱不能为空'
        
        # 验证密码（仅在注册时验证）
        if not is_update and 'password' in user_data:
            password = user_data.get('password', '')
            if not password:
                errors['password'] = '密码不能为空'
            elif len(password) < 6:
                errors['password'] = '密码长度不能少于6个字符'
            elif len(password) > 128:
                errors['password'] = '密码长度不能超过128个字符'
        
        # 验证权限等级
        if 'permission' in user_data:
            permission = user_data.get('permission')
            if permission is not None:
                try:
                    permission = int(permission)
                    if permission < 0 or permission > 3:
                        errors['permission'] = '权限等级必须在0-3之间'
                except (ValueError, TypeError):
                    errors['permission'] = '权限等级必须是整数'
        
        return errors
    
    def update_user_info(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新用户信息
        
        Args:
            user_id (int): 用户ID
            update_data (Dict[str, Any]): 更新数据
            
        Returns:
            Dict[str, Any]: 更新后的用户信息
            
        Raises:
            ApiException: 当用户不存在或数据验证失败时抛出异常
        """
        user_obj = User.query.get(user_id)
        if not user_obj:
            raise ApiException(404, "用户不存在")
        
        # 验证更新数据
        errors = self.validate_user_data(update_data, is_update=True)
        if errors:
            raise ApiException(400, "数据验证失败", errors)
        
        # 模拟更新操作
        allowed_fields = ['nickname', 'avatar', 'permission']
        if 'nickname' in update_data:
            user_obj.nickname = update_data['nickname']
        if 'avatar' in update_data:
            user_obj.avatar = update_data['avatar']
        if 'permission' in update_data:
            try:
                user_obj.permission = int(update_data['permission'])
            except (ValueError, TypeError):
                pass
        db.session.commit()
        return user_obj.to_dict()
    
    def get_users_list(self, page: int = 1, per_page: int = 10, search: str = None) -> Dict[str, Any]:
        """
        获取用户列表
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            search (str): 搜索关键词
            
        Returns:
            Dict[str, Any]: 包含用户列表和分页信息的字典
        """
        query = User.query
        if search:
            like = f"%{search}%"
            query = query.filter((User.username.like(like)) | (User.nickname.like(like)) | (User.email.like(like)))
        total = query.count()
        users = query.order_by(User.id.asc()).offset((page - 1) * per_page).limit(per_page).all()
        public_users = [u.to_public_dict() | {'is_active': u.is_active} for u in users]
        return {
            'users': public_users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }


# 创建服务实例
user_service = UserService()
