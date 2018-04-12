from flask import Flask, render_template
from flask import abort
from flask.ext.bootstrap import Bootstrap
from datetime import datetime
from flask.ext.moment import Moment
from nameform import NameForm

app = Flask(__name__)

# 初始化
bootstrap = Bootstrap(app)
moment = Moment(app)

# app.config字典可存储框架、扩展、和程序本身的配置变量
# 设置密钥 ，该为通用密钥。可在flask和多个第三方扩展中使用
app.config['SECRET_KEY'] = 'hard to guss string'


# 处理url和函数之间关系的程序叫做路由（装饰器）,可处理get、post 默认仅get
@app.route('/', methods=['GET', 'POST'])
def index():
    """视图函数，默认返回200"""
    # Flask使用上下文让特定变量在一个线程中可全局访问，而不干扰其他线程
    # user_agent = request.headers.get('User_Agent')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name,
                           current_time=datetime.utcnow())


# 动态响应 flask 支持路由中使用int、float、path
# 例如：/user/<int :id>:则动态片段只匹配id为整形的url
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html'),500

# @app.route('/user/<id>')
# def get_user(id):
#     load_user = {2: 'adada'}
#     user = load_user(id)
#     print(user)
#     if not user:
#         abort(404)  # 抛出异常把控制权交给web服务器
#     return render_template('user.html', name=user)


if __name__ == '__main__':
    app.run(debug=True)  # app.run(debug = True)
