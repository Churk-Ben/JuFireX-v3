from datetime import datetime
from app.model import db


class User(db.Model):
    """
    用户模型类
    
    包含用户的基本信息字段，支持用户注册、登录、权限管理等功能
    """
    __tablename__ = "users"
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True, comment="用户ID")
    username = db.Column(db.String(50), unique=True, nullable=False, comment="用户名")
    nickname = db.Column(db.String(100), nullable=False, comment="用户昵称")
    email = db.Column(db.String(255), unique=True, nullable=False, comment="邮箱地址")
    password = db.Column(db.String(255), nullable=False, comment="密码哈希")
    
    # 用户信息字段
    avatar = db.Column(db.String(500), nullable=True, comment="头像路径")
    permission = db.Column(db.Integer, default=1, nullable=False, comment="权限等级")
    
    # 状态字段
    is_active = db.Column(db.Boolean, default=True, nullable=False, comment="是否激活")
    is_verified = db.Column(db.Boolean, default=False, nullable=False, comment="是否已验证邮箱")
    
    # 时间戳字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    last_login_at = db.Column(db.DateTime, nullable=True, comment="最后登录时间")

    def __repr__(self) -> str:
        return f"<User {self.username}({self.email})>"
    
    def to_dict(self, include_sensitive=False):
        """
        将用户对象转换为字典格式
        
        Args:
            include_sensitive (bool): 是否包含敏感信息（如密码）
            
        Returns:
            dict: 用户信息字典
        """
        user_dict = {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'avatar': self.avatar,
            'permission': self.permission,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        
        if include_sensitive:
            user_dict['password'] = self.password
            
        return user_dict
    
    def to_public_dict(self):
        """
        获取用户公开信息（不包含敏感数据）
        
        Returns:
            dict: 用户公开信息字典
        """
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'permission': self.permission,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }