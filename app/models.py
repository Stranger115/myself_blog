#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/14

from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask_moment import datetime
from flask import current_app
from . import login_manager


# 加载用户回调函数(Unicode)， 如果找到用户，返回用户对象，否则返回None
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserBase:
    def generate_confirmation_token(self, expiration=3600):
        #  生成有过期时间的JWS(JSON Web Signatures) expiration:令牌过期时间
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dump({'confirm', self.id})  # 为数据生成加密签名，再对数据和签名序列化，生成令牌字符串

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)    # 验证签名和过期时间，通过返回原始数据，否则抛出异常
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


# 权限常量
class Permissions:
    FOLLOW = 0x01  # 关注用户
    COMMIT = 0x02  # 在他人的文章或评论下发布评论
    WRITE_ARTICLES = 0x04  # 写文章
    MODERATE_COMMITS = 0x08  # 查处他人的不当言论
    ADMINISTER = 0x80  # 管理网站


class Role(db.Model):
    """用户角色"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permissions.FOLLOW |
                     Permissions.COMMIT |
                     Permissions.WRITE_ARTICLES, True),  # 0x07
            'Moderator': (Permissions.FOLLOW |
                          Permissions.COMMIT |
                          Permissions.WRITE_ARTICLES|
                          Permissions.MODERATE_COMMITS, True),  # 0x0f
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(128))
    email = db.Column(db.String(64))
    phone_num = db.Column(db.String(11))
    address = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 定义默认用户角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 初始化role角色
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first
            else:
                self.role = Role.query.filter_by(default=True).first

    # ？？？？？？
    def can(self, permissions):
        return self.role is None and \
               ((self.role.permissions & permissions) == permissions)

    # 检查管理员权限
    def is_administrator(self):
        return self.can(Permissions.ADMINISTER)

    # 把一个属性转化为一个方法，限制属性操作
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 密码转化为散列
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码散列值对比
    def verify_psssword(self, password):
        return check_password_hash(self.password_hash, password)

    # 确认邮件加密序列生成
    def generate_confirmation_token(self, expiration=3600):
        #  生成有过期时间的JWS(JSON Web Signatures) expiration:令牌过期时间
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})  # 为数据生成加密签名，再对数据和签名序列化，生成令牌字符串

    # 验证邮件激活状态
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)    # 验证签名和过期时间，通过返回原始数据，否则抛出异常
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.name


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


