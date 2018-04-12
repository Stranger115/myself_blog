from flask import Flask

app = Flask(__name__)


# 处理url和函数之间关系的程序叫做路由（装饰器）
@app.route('/')
def hello_world():
    """视图函数"""
    return 'Hello World!'


# 动态响应 flask 支持路由中使用int、float、path
# 例如：/user/<int :id>:则动态片段只匹配id为整形的url
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)  # app.run(debug = True)
