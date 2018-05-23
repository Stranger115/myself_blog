#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/5/16
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permissions


# 判定用户是否拥有指定权限装饰器
def permission_required(permisson):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permisson):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permissions.ADMINISTER)(f)