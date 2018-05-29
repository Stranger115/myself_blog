#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/14

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort,\
    current_app
from flask.ext.login import login_required, current_user
from app import db, photos
from . import main
from .forms import EditProfileUserForm, EditProfileAdminForm, PostForm
from ..models import User, Permissions, Post
from ..decorators import admin_required, permission_required


# 路由修饰器由蓝本提供
@main.route('/')
def index():
    name = None
    return render_template('index.html', name=name, current_time=datetime.utcnow())


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


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        filename = photos.save(form.profile_picture.data)
        current_user.profile_picture = photos.url(filename)
        current_user.address = form.address.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        # if form.profile_picture.data is None:
        #     flash(photos)
        return redirect(url_for('main.user', username=current_user.username))
    form.username.data = current_user.username
    form.address.data = current_user.address
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
# @admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role_id = form.role.data
        filename = photos.save(form.profile_picture.data)
        user.profile_picture = photos.url(filename)
        user.address = form.address.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('资料已更新')
        return redirect(url_for('main.user', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    form.role.data = user.role_id
    form.address.data = user.address
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return "For administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permissions.MODERATE_COMMITS)
def for_moderators_only():
    return "For comment moderators"


@main.route('/article_label', methods=['GET', 'POST'])
def article_label():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('article_label.html', posts=posts, pagination=pagination)


@main.route('/article/<int:id>')
def article(id):
    post = Post.query.get_or_404(id)
    return render_template('article.html', post=post)


@main.route('/post_article', methods=['GET', 'POST'])
@login_required
def post_article():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('post_article.html', form=form)


@main.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.can(Permissions.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('文章已修改！')
        return redirect(url_for('.article', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_article.html', form=form)


@main.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
# @Permissions
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('已关注')
    current_user.follow(user)
    flash('已关注')
    return render_template('follow.html')


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
    current_user.unfollow(user)
    flash('已取消关注')
    return render_template('unfollow.html')


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, pagination=pagination,
                           endpoint='.followers', follows=follows)


@main.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page=page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    following = [{'user': item.follower, 'timestamp': item.timestamp}
                for item in pagination.items]
    return render_template('followed.html', user=user, pagination=pagination,
                           endpoint='.followed', following=following)
