'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2022-01-10 10:38:26
LastEditors: DaLao
LastEditTime: 2022-01-18 14:24:01
'''
import datetime
import json

from flask import Flask, render_template, request, redirect, url_for

from controller import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html', status=1)
    if request.method == 'POST':
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        if name == 'admin' and pwd == 'admin':
            return redirect(url_for('index_page'))
        else:
            return render_template('login.html', status=-1)


@app.route('/index', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data_page():
    data = get_people()
    return render_template('data.html', data=data)


@app.route('/log', methods=['GET'])
def log_page():
    data = get_all_log()
    return render_template('log.html', data=data)


# 抽签
@app.route('/select/<status>', methods=['POST'])
def select(status):
    data = json.loads(request.get_data())
    return select_people(data, status)


@app.route('/add', methods=['POST'])
def add():
    data = json.loads(request.get_data())
    return add_log(data)


# 上传文件
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    return read_excel(f)


@app.route('/download/<uuid>', methods=['GET'])
def download(uuid):
    response = download_excel(uuid)
    # print("response", type(response))
    response.headers['Content-Type'] = "utf-8"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Content-Disposition"] = "attachment; filename=" + str(datetime.datetime.now()) + ".xlsx"
    return response


@app.route('/del/<table>/<uuid>', methods=['GET'])
def delete(table, uuid):
    if table == 'people':
        return del_info()
    if table == 'log':
        return del_log(uuid)


@app.route('/get/<table>/<uuid>', methods=['GET'])
def get(table, uuid):
    def x(d):
        c = ''
        for k, v in d.items():
            c += (k + v + "\n")
        return c

    if table == 'people':
        d = get_info(uuid)
        return x(d)
    if table == 'log':
        d = get_log(uuid)
        return x(d)


if __name__ == '__main__':
    app.run(debug=True)
