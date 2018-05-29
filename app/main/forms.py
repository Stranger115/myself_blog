#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/12
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from app import photos
from ..models import Role, User


class EditProfileUserForm(FlaskForm):
    username = StringField('昵称：', validators=[DataRequired(), Length(1, 64)])
    email = StringField('邮箱：',
                        validators=[DataRequired(), Length(1, 64), Email()])
    profile_picture = FileField('头像：', validators=[
                                                   FileAllowed(photos, '只能上传图片')])
    address = StringField('地址', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField('简介:', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称已被注册')


class EditProfileAdminForm(FlaskForm):
    username = StringField('昵称：', validators=[DataRequired(), Length(1, 64),
                           Regexp('^[A-Za-z][\w_.]*$', 0, '首位大小写字母其余为字母数字或_.')])
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64), Email()])
    role = SelectField('角色：', coerce=int)
    profile_picture = FileField('头像：', validators=[
        FileAllowed(photos, '只能上传图片')])
    # name = StringField('姓名：', validators=[DataRequired()])
    address = StringField('地址', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField('简介:', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称已被注册')



