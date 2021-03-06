#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/5/29
from flask import url_for, redirect, render_template, request, current_app,\
    abort, flash
from flask_login import login_required, current_user

from . import article
from .. import db
from ..models import Post, Permissions, Comment
from .form import PostForm, CommentForm
from ..decorators import permission_required
from ..auth.views import login_page


# 修改文章
@article.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.WRITE_ARTICLES)
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
    return render_template('article/edit_article.html', form=form)


# 写文章
@article.route('/post_article', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.WRITE_ARTICLES)
def post_article():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))
    return render_template('article/post_article.html', form=form)


# 文章分页
@article.route('/article_label', methods=['GET', 'POST'])
def article_label():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('article/article_label.html', posts=posts, pagination=pagination)


# 文章详情页
@article.route('/article/<int:id>', methods=['GET', 'POST'])
@login_page
def article(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    reply_form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, article=post,
                          comment_user=current_user._get_current_object())
        db.session.add(comment)
        flash('发送成功')
        return redirect(url_for('article.article', id=post.id, page=-1))
    if reply_form.validate_on_submit():
        reply_comments = Comment(form.body.data, article=post,
                                 reply_user=current_user._get_current_object())
        db.session.add(reply_comments)
        return redirect()
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count()-1) / \
               current_app.config['FLASKY_COMMINTS_PER_PAGE']+1
    pagination = post.comments.filter_by(reply_id=None).all().order_by(Comment.id.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMINTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    length = range(len(comments))
    return render_template('article/article.html',length=length, post=post, login_form=g.login_form,
                           form=form, reply_form=reply_form, comments=comments, pagination=pagination)
