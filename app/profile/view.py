#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/5/29
from . import profile
from ..models import User
from ..main.forms import EditProfileAdminForm, EditProfileUserForm
from app import photos, db
from flask import url_for, redirect, render_template, flash
from flask_login import login_required, current_user


@profile.route('/edit_profile', methods=['GET', 'POST'])
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
    return render_template('profile/edit_profile.html', form=form)


@profile.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
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
    return render_template('profile/edit_profile.html', form=form, user=user)