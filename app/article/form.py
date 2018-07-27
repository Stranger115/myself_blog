#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/5/29
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('标题:', validators=[DataRequired(), Length(1, 64)])
    body = PageDownField('正文：', validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('评论：', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('发表评论')