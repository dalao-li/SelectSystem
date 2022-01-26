'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2022-01-10 10:38:26
LastEditors: DaLao
LastEditTime: 2022-01-26 21:08:42
'''

import json

import datetime

from flask import Flask, render_template, request, redirect,url_for

from controller import *

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html',status=1)
    if request.method == 'POST':
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        if name == 'admin' and pwd == 'admin':
            return redirect(url_for('main_page'))
        else :
            return render_template('login.html',status=-1)


@app.route('/main', methods=['GET'])
def main_page():
    if request.method == 'GET':
        return render_template('main.html')


@app.route('/data', methods=['GET','POST'])
def data_page():
    if request.method == 'GET':
        data = get_people()
        return render_template('data.html', data = data, status = -1)
    if request.method == 'POST':
        f = request.files['file']
        data = get_people()
        status = read_excel(f)
        return render_template('data.html', data = data, status = status)

@app.route('/log', methods=['GET'])
def log_page():
    data = get_all_log()
    return render_template('log.html', data = data)

# 抽签
@app.route('/select/<status>', methods=['POST'])
def select(status):
    data = json.loads(request.get_data())
    return select_people(data,status)


@app.route('/add', methods=['POST'])
def add():
    data = json.loads(request.get_data())
    return add_log(data)


@app.route('/download/<id>', methods=['GET'])
def download(id):
    response = download_excel(id)
    response.headers['Content-Type'] = "utf-8"
    response.headers["Cache-Control"] = "no-cache"
    name = datetime.datetime.now()
    response.headers["Content-Disposition"] = "attachment; filename=" + str(name) + ".xlsx"
    return response


@app.route('/del/<id>', methods=['GET'])
def delete(id):
    return del_log(id)

@app.route('/get/<table>/<id>', methods=['GET'])
def get(table,id):
    return get_info(table, id)


if __name__ == '__main__':
    app.run(debug=True)
