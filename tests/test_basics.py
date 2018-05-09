#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/25
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    # 创建一个测试环境（类似运行中的程序）
    def setUp(self):
        self.app = create_app('testing')  # 激活上下文
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 确保程序实例存在
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    # 确保程序在测试配置中运行
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])