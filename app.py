import json

from flask import Flask, redirect, render_template, request, url_for
from controller import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login_page():
    ip = request.remote_addr
    if request.method == 'GET':
        record_log(ip, '访问登陆页面')
        return render_template('login.html', status=1, ip=ip)
    if request.method == 'POST':
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        if name == 'admin' and pwd == 'admin':
            record_log(ip, '登陆成功')
            return redirect(url_for('index_page'))
        else:
            record_log(ip, '登陆失败')
            return render_template('login.html', status=-1)


@app.route('/index', methods=['GET'])
def index_page():
    record_log(request.remote_addr, '访问投票页面')
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data_page():
    record_log(request.remote_addr, '访问人员名单页面')
    data = get_people()
    return render_template('data.html', data=data)


@app.route('/log', methods=['GET'])
def log_page():
    record_log(request.remote_addr, '访问投票记录页面')
    data = get_all_log()
    return render_template('log.html', data=data)


@app.route('/record', methods=['GET'])
def record():
    record_log(request.remote_addr, '访问记录页面')
    data = get_login_log()
    return render_template('record.html', data=data)


@app.route('/select/<status>', methods=['POST'])
def select(status):
    data = json.loads(request.get_data())
    r = select_people(data, status)
    record_log(request.remote_addr, '抽签/' + str(r['code']) + '/' + r['result'])
    return r


@app.route('/add', methods=['POST'])
def add():
    record_log(request.remote_addr, '添加投票记录')
    data = json.loads(request.get_data())
    return add_log(data)


@app.route('/upload', methods=['POST'])
def upload():
    record_log(request.remote_addr, '上传文件')
    f = request.files['file']
    return read_excel(f)


@app.route('/download/<uuid>', methods=['GET'])
def download(uuid):
    def x():
        return str(datetime.datetime.now())

    response = download_excel(uuid)
    response.headers['Content-Type'] = "utf-8"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Content-Disposition"] = "attachment; filename=" + x() + ".xlsx"
    record_log(request.remote_addr, '下载文件' + x() + ".xlsx")
    return response


@app.route('/del/<table>/<uuid>', methods=['GET'])
def delete(table, uuid):
    if table == 'people':
        record_log(request.remote_addr, '删除人员名单')
        return del_info()
    if table == 'log':
        record_log(request.remote_addr, '删除投票记录')
        return del_log(uuid)


@app.route('/get/<table>/<uuid>', methods=['GET'])
def get(table, uuid):
    def x(data):
        c = ''
        for k, v in data.items():
            c += (k + v + "\n")
        return c

    if table == 'people':
        record_log(request.remote_addr, '访问人员名单')
        d = get_info(uuid)
        return x(d)
    if table == 'log':
        record_log(request.remote_addr, '访问投票记录')
        d = get_log(uuid)
        return x(d)


if __name__ == '__main__':
    app.run(debug=True)
