#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/12
"""
    启动脚本
"""
import os
from app import create_app, db
from app.models import User, Role, Post
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.migrate import Migrate

# 如果已经定义了环境变量 FLASK_CONFIG，则从中读取配置名；否则使用默认配置
app = create_app(os.getenv('FLASK_CONFIG')or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


@manager.command
def test():
    """Run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)\

# 开启Debug模式, --threaded开启多线程模式
manager.add_command("runserver", Server(use_debugger=True))
if __name__ == '__main__':
    app.run()
    # manager.run()
