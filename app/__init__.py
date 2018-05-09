#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/12
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from config import config


"""工厂函数在 apps 包的构造文件中定义"""
# 创建外部模型
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
# 防止用户会话被篡改
login_manager.session_protection = 'strong'
# 设置登录页面的地址
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """现在程序在运行时创建，只有调用 create_app() 之后才能使用 apps.route 修饰器"""
    app = Flask(__name__)

    # 初始化config.py的配置文件
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 创建的扩展对象上调用 init_app() 可以完成初始化过程
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    # 附加路由和自定义的错误页面

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
