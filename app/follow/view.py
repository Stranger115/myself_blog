#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/5/29
from . import follow
from ..models import User
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user


# 显示粉丝列表
@follow.route('/followers/<username>')
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
    return render_template('follow/followers.html', user=user, pagination=pagination,
                           endpoint='follow.followers', follows=follows)


# 已关注的详细列表
@follow.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page=page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    following = [{'user': item.followed, 'timestamp': item.timestamp}
                for item in pagination.items]
    return render_template('follow/followed.html', user=user, pagination=pagination,
                           endpoint='follow.followed', following=following)


# 取消关注
@follow.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
    current_user.unfollow(user)
    flash('已取消关注')
    return render_template('follow/unfollow.html')


# 关注
@follow.route('/follow/<username>', methods=['GET', 'POST'])
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
    return render_template('follow/follow.html')








