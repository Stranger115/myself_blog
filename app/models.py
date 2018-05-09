#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/14

from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask.ext.moment import datetime
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


class Role(db.Model):
    """用户角色"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """普通用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    user_phone_num = db.Column(db.String(11))
    user_address = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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


class FoodType(db.Model):
    """商品类别"""
    __tablename__ = 'food_types'
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String(36), index=True)

    merchants = db.relationship('Merchant', backref='foodtype')

    def __repr__(self):
        return '<Store_type %r>' % self.merchant_name


class Merchant(UserMixin, db.Model, UserBase):
    """商户"""
    __tablename__ = 'merchants'
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(64), unique=True, index=True)

    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    merchant_phone_num = db.Column(db.String(11))
    merchant_address = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)

    store_type = db.Column(db.String(36), db.ForeignKey('food_types.id'))

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

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<Merchant %r>' % self.merchant_name
