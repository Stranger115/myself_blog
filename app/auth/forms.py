#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/25

from flask.ext.wtf import Form
from wtforms import SubmitField, PasswordField, RadioField, BooleanField, \
    StringField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email
from wtforms import ValidationError
from ..models import User
# import json

# province_id = '86'


class LoginForm(Form):
    username = StringField('用户登录:', validators=[DataRequired()])
    password = PasswordField('我的密码:', validators=[DataRequired()])
    remember_me = BooleanField('记住我', default='checked', validators=[DataRequired()])
    submit = SubmitField('登录')


class RegistrationForm(Form):
    username = StringField('用户昵称：', validators=[DataRequired(), Length(1, 64)],)
    email = StringField('用户邮箱：', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码：', validators=[DataRequired(),
                            EqualTo('password2', message='密码不一致'),
                            Length(8, 16, message='密码长度为8到16'),
                            Regexp('^w*', message='密码应由数字和字母组成')])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    phone_num = StringField('用户电话：', validators=[DataRequired(), Length(1, 11),
                            Regexp('^1[34578]\d{9}$', message='请输入正确的手机号码')])

    # # 读地址
    # with open("app/static/data/data.json", 'r', encoding="utf-8") as load_f:
    #     load_dict = json.load(load_f)
    #     province = load_dict[province_id]
    #     address_province = SelectField('地址', choices=[x for x in zip(
    #         province.keys(), province.values())])
    #     # cities =
    #     address_city = SelectField('', choices=[x for x in zip()])
    address = StringField('地址：', validators=[DataRequired()])

    submit = SubmitField('注册')

    # 检查用户名是否已存在
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')
            