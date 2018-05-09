#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/14

"""
    蓝本和程序类似，也可以定义路由。不同的是，在蓝本中定义的路由处于休眠状态，
    直到蓝本注册到程序上后，路由才真正成为程序的一部分。使用位于全局作用域中的
    蓝本时，定义路由的方法几乎和单脚本程序一样。
"""

from flask import Blueprint


"""
    蓝本可以在单个文件中定义，也可使用更结构化的方式在包中的多个模块中创建。
    为了获得最大的灵活性，程序包中创建了一个子包，用于保存蓝本
"""

# 通过实例化一个 Blueprint 类对象可以创建蓝本。两个必须指定的参数：(blueprint_name，blueprint_pack）
# 大多数情况下第二个参数使用 Python 的__name__ 变量即可
main = Blueprint('main', __name__)

"""
    这些模块在 app/main/__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，
    因为在views.py 和 errors.py 中还要导入蓝本 main
"""
# 导入这两个模块能把路由和错误处理程序与蓝本关联起来
from . import views, errors

