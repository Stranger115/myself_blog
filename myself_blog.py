from flask import Flask, render_template
from flask import abort

app = Flask(__name__)


# 处理url和函数之间关系的程序叫做路由（装饰器）
@app.route('/')
def hello_world():
    """视图函数，默认返回200"""
    # Flask使用上下文让特定变量在一个线程中可全局访问，而不干扰其他线程
    # user_agent = request.headers.get('User_Agent')
    return render_template('index.html')


# 动态响应 flask 支持路由中使用int、float、path
# 例如：/user/<int :id>:则动态片段只匹配id为整形的url
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


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
