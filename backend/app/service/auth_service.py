"""
认证服务层

负责处理用户认证相关的业务逻辑，包括用户注册、登录验证、会话管理等功能。
暂时使用模拟数据，不连接实际数据库。
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from app.exception.api_exception import ApiException
from app.service.user_service import user_service


class AuthService:
    """认证服务类"""
    
    def __init__(self):
        # 模拟会话存储
        self._mock_sessions = {}
        # 模拟密码存储（实际应用中应该使用加密存储）
        self._mock_passwords = {
            'admin': self._hash_password('admin123'),
            'user001': self._hash_password('password123')
        }
        # 模拟用户ID计数器
        self._next_user_id = 3
    
    def _hash_password(self, password: str) -> str:
        """
        密码哈希处理
        
        Args:
            password (str): 原始密码
            
        Returns:
            str: 哈希后的密码
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_session_token(self) -> str:
        """
        生成会话令牌
        
        Returns:
            str: 会话令牌
        """
        return secrets.token_urlsafe(32)
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户注册
        
        Args:
            user_data (Dict[str, Any]): 用户注册数据
            
        Returns:
            Dict[str, Any]: 注册结果
            
        Raises:
            ApiException: 当数据验证失败时抛出异常
        """
        # 验证用户数据
        errors = user_service.validate_user_data(user_data, is_update=False)
        if errors:
            raise ApiException(400, "注册数据验证失败", errors)
        
        # 检查用户名和邮箱是否已存在
        if user_service.get_user_by_username(user_data['username']):
            raise ApiException(400, "用户名已存在")
        
        if user_service.get_user_by_email(user_data['email']):
            raise ApiException(400, "邮箱已存在")
        
        # 创建新用户（模拟）
        new_user_id = self._next_user_id
        self._next_user_id += 1
        
        new_user = {
            'id': new_user_id,
            'username': user_data['username'].strip(),
            'nickname': user_data['nickname'].strip(),
            'email': user_data['email'].strip(),
            'avatar': user_data.get('avatar', '/static/avatars/default.jpg'),
            'permission': user_data.get('permission', 1),
            'is_active': True,
            'is_verified': False,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'last_login_at': None
        }
        
        # 存储密码哈希
        self._mock_passwords[user_data['username']] = self._hash_password(user_data['password'])
        
        # 添加到用户服务的模拟数据中
        user_service._mock_users[new_user_id] = new_user
        
        return {
            'user_id': new_user_id,
            'username': new_user['username'],
            'nickname': new_user['nickname'],
            'email': new_user['email'],
            'created_at': new_user['created_at']
        }
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        用户身份验证
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            Optional[Dict[str, Any]]: 认证成功返回用户信息，失败返回None
        """
        if not username or not password:
            return None
        
        # 获取用户信息
        user = user_service.get_user_by_username(username)
        if not user:
            return None
        
        # 验证密码
        stored_password_hash = self._mock_passwords.get(username)
        if not stored_password_hash:
            return None
        
        if stored_password_hash != self._hash_password(password):
            return None
        
        # 检查用户状态
        if not user.get('is_active', False):
            return None
        
        return user
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            Dict[str, Any]: 登录结果，包含会话信息
            
        Raises:
            ApiException: 当登录失败时抛出异常
        """
        if not username or not password:
            raise ApiException(400, "用户名和密码不能为空")
        
        # 身份验证
        user = self.authenticate_user(username, password)
        if not user:
            raise ApiException(401, "用户名或密码错误")
        
        # 生成会话令牌
        session_token = self._generate_session_token()
        
        # 创建会话信息
        session_info = {
            'token': session_token,
            'user_id': user['id'],
            'username': user['username'],
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat(),
            'is_active': True
        }
        
        # 存储会话
        self._mock_sessions[session_token] = session_info
        
        # 更新用户最后登录时间
        user['last_login_at'] = datetime.utcnow().isoformat()
        user_service._mock_users[user['id']] = user
        
        return {
            'token': session_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'nickname': user['nickname'],
                'avatar': user['avatar'],
                'permission': user['permission']
            },
            'expires_at': session_info['expires_at']
        }
    
    def logout_user(self, session_token: str) -> bool:
        """
        用户登出
        
        Args:
            session_token (str): 会话令牌
            
        Returns:
            bool: 登出是否成功
        """
        if not session_token:
            return False
        
        session = self._mock_sessions.get(session_token)
        if not session:
            return False
        
        # 标记会话为非活跃状态
        session['is_active'] = False
        session['logout_at'] = datetime.utcnow().isoformat()
        
        return True
    
    def get_session_info(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        获取会话信息
        
        Args:
            session_token (str): 会话令牌
            
        Returns:
            Optional[Dict[str, Any]]: 会话信息，如果会话无效则返回None
        """
        if not session_token:
            return None
        
        session = self._mock_sessions.get(session_token)
        if not session:
            return None
        
        # 检查会话是否活跃
        if not session.get('is_active', False):
            return None
        
        # 检查会话是否过期
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.utcnow() > expires_at:
            session['is_active'] = False
            return None
        
        return session.copy()
    
    def get_current_user(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        根据会话令牌获取当前用户信息
        
        Args:
            session_token (str): 会话令牌
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息，如果会话无效则返回None
        """
        session = self.get_session_info(session_token)
        if not session:
            return None
        
        user = user_service.get_user_by_id(session['user_id'])
        return user
    
    def check_auth_status(self, session_token: str) -> Dict[str, Any]:
        """
        检查认证状态
        
        Args:
            session_token (str): 会话令牌
            
        Returns:
            Dict[str, Any]: 认证状态信息
        """
        session = self.get_session_info(session_token)
        
        if not session:
            return {
                'isLoggedIn': False,
                'is_authenticated': False,
                'user': None,
                'session': None
            }
        
        user = user_service.get_user_by_id(session['user_id'])
        if not user:
            return {
                'isLoggedIn': False,
                'is_authenticated': False,
                'user': None,
                'session': None
            }
        
        return {
            'isLoggedIn': True,
            'is_authenticated': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'nickname': user['nickname'],
                'avatar': user['avatar'],
                'permission': user['permission']
            },
            'session': {
                'token': session['token'],
                'created_at': session['created_at'],
                'expires_at': session['expires_at']
            }
        }
    
    def refresh_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        刷新会话
        
        Args:
            session_token (str): 会话令牌
            
        Returns:
            Optional[Dict[str, Any]]: 刷新后的会话信息，如果会话无效则返回None
        """
        session = self.get_session_info(session_token)
        if not session:
            return None
        
        # 延长会话过期时间
        new_expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
        session['expires_at'] = new_expires_at
        session['refreshed_at'] = datetime.utcnow().isoformat()
        
        # 更新存储的会话信息
        self._mock_sessions[session_token] = session
        
        return {
            'token': session['token'],
            'expires_at': session['expires_at'],
            'refreshed_at': session['refreshed_at']
        }


# 创建服务实例
auth_service = AuthService()