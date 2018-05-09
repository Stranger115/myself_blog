#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/14

from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask.ext.login import login_required
from os import abort
from . import main
from .forms import NameForm
from ..models import User


# 路由修饰器由蓝本提供
@main.route('/')
def index():
    name = None
    return render_template('index.html', name=name, current_time=datetime.utcnow())


# @main.route('/<name>', methods=['GET', 'POST'])
# def user(name):
#     form = NameForm()
#     if form.validate_on_submit():
#         # Flask会为蓝本中的全部端点加上一个命名空间，可以在不同的蓝本中使用相同的
#         # 端点名定义视图函数，而不会产生冲突。命名空间就是蓝本实例化的名字（ Blueprint构造函数的第一个参数），
#         # 所以视图函数index()，注册的端点名是main.index，其URL使用 url_for('main.index')获取
#         # 跨蓝本的重定向必须使用带有命名空间的端点名
#         return redirect(url_for('.index'))
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False),
#                            current_time=datetime.utcnow())


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)