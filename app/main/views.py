#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/14

from datetime import datetime
from flask import render_template, request, redirect, url_for, abort,\
    current_app, make_response
from flask_login import login_required, current_user
from . import main
from ..models import User, Permissions, Post
from ..decorators import admin_required, permission_required
from ..auth.views import login


# 路由修饰器由蓝本提供
@main.route('/', methods=['GET', 'POST'])
def index():
    show_followed = False

    # 首页显示所关注者的文章
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_INDEX_PRE_PAGE'],
        error_out=False)
    posts = pagination.items

    # 显示登录
    login_form = login()

    return render_template('index.html', pagination=pagination, posts=posts,
                           current_time=datetime.utcnow(), login_form=login_form)


# @main.route('/', methods=['GET', 'POST'])
# def search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         contain = form.contain


# 关注文章列表
@main.route('/choose_articles')
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)  # max_age:cookie过期时间
    return resp


# 推荐文章列表
@main.route('/followed_articles')
@login_required
def show_followed_articles():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.errorhandler(404)
def page_not_find(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
#         # Flask会为蓝本中的全部端点加上一个命名空间，可以在不同的蓝本中使用相同的
#         # 端点名定义视图函数，而不会产生冲突。命名空间就是蓝本实例化的名字（ Blueprint构造函数的第一个参数），
#         # 所以视图函数index()，注册的端点名是main.index，其URL使用 url_for('main.index')获取
#         # 跨蓝本的重定向必须使用带有命名空间的端点名


# 个人中心
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


# 后台管理员
@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return "For administrators!"


# 评论管理员
@main.route('/moderator')
@login_required
@permission_required(Permissions.MODERATE_COMMITS)
def for_moderators_only():
    return "For comment moderators"





