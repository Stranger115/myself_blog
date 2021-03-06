#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/12
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from config import config


"""工厂函数在 apps 包的构造文件中定义"""
# 创建外部模型
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
photos = UploadSet('photos', IMAGES)


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
    pagedown.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)


    # 附加路由和自定义的错误页面

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .article import article as article_blueprint
    from .follow import follow as follow_blueprint
    from .profile import profile as profile_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(article_blueprint, url_prefix='/article')
    app.register_blueprint(follow_blueprint, url_prefix='/follow')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    return app
