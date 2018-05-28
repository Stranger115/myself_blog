#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/12

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基类 Config 中包含通用配置"""
    # 类变量对所有实例化对象公开
    # 防止CSRF攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # 数据库修改自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin shadow.qiuying@qq.com'
    FLASKY_ADMIN = 'shadow.qiuying@qq.com'

    MAIL_SERVER = 'smtp.qq.com'

    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    SSL_DISABLE = False
    SSL_REDIRECT = False
    MAIL_USERNAME = 'shadow.qiuying@qq.com'  # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'bwpyhghjfjoscage'  # os.environ.get('MAIL_PASSWORD')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'shadow.qiuying@qq.com'

    UPLOADS_DEFAULT_DEST = r'D:\projects\myself_blog\app\static\images\profile_picture'
    UPLOADED_PHOTOS_DEST = r'D:\projects\myself_blog\app\static\images\profile_picture'

    # 分页显示文章数量
    FLASKY_POSTS_PER_PAGE = 2

    # 对当前环境配置初始化
    @staticmethod
    def init_app(app):
        pass


"""在不同环境下使用不同数据库"""


class DevelopmentConfig(Config):
    """专用的配置"""
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://root:20180415@localhost/my_blog'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}