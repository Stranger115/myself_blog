#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/25

from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from ..email import send_email
from app import db
from . import auth


# 登录表单函数
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_psssword(form.password.data):
            login_user(user, form.remember_me.data)  # 在用户会话中记录用户已登录
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return form


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    login_form = login()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data,
                    phone_num=form.phone_num.data, address=form.address.data,
                    profile_picture='images/profile_picture/default.jpg',
                    email=form.email.data)
        # 注册信息加入数据库
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()  # 邮件激活序列
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user,
                   token=token)
        flash('确认邮件已发送，请在邮箱中确认您的账户！')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form, login_form=login_form)


# 确认用户账号，用户点击这个链接要先登录才执行这个视图函数
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('请现在邮箱中激活您的账户')
    else:
        flash('激化链接已失效，请点击重发')
    return redirect(url_for('main.index'))


# 处理过滤未确认账户的用户
@auth.before_app_request
def before_request():
    # endpoint请求端点
    if current_user.is_authenticated:
        current_user.ping()  # 更新已登录用户的访问时间
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# 重新发送账户确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()

    send_email(current_user.email, '确认你的账户', 'auth/email/confirm',
               user=current_user, token=token)
    flash('新的激活邮件已发送至您的邮箱，请及时激活')
    return redirect(url_for('main.index'))

