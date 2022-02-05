'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2022-01-10 10:38:26
LastEditors: DaLao
LastEditTime: 2022-02-06 00:07:23
'''

import json, datetime

from flask import Flask, render_template, request, redirect, url_for,make_response

from controller import *


app = Flask(__name__)


@app.route('/<page>' , methods = ['GET' , 'POST'])
def pages(page):
    if page == '':
        if request.method == 'GET':
            return render_template('login.html', status = 1)
        if request.method == 'POST':
            name = request.form.get("name")
            pwd = request.form.get("pwd")
            if name == 'admin' and pwd == 'admin':
                return redirect(url_for('main_page'))
            else:
                return render_template('login.html', status = -1)
    if page == 'main' :
        if request.method == 'GET':
            return render_template('main.html')
    if page == 'data' :
        if request.method == 'GET':
            data = get_people()
            return render_template('data.html', data = data, status = -1)
        if request.method == 'POST':
            f = request.files['file']
            status = read_excel(f)
            data = get_people()
            return render_template('data.html', data = data, status = status)
    if page == 'log' : 
        data = get_all_log()
        return render_template('log.html', data = data)
    if page == 'favicon.ico':
        return '1'


@app.route('/api/<status>/<name>/<id>', methods = ['GET', 'POST'])
def api(status, name, id):
    if status == 'get':
        if name == 'select_people':
            data = json.loads(request.get_data())
            return select_people(data,id)
        if name == 'download_log':
            fp = download_excel(id)
            response = make_response(fp)
            response.headers['Content-Type'] = "utf-8"
            response.headers["Cache-Control"] = "no-cache"
            response.headers["Content-Disposition"] = "attachment; filename=" + str(datetime.datetime.now()) + ".xlsx"
            return response
        if name == 'log_info':
            return get_info('log', id)
        if name == 'people_info':
            return get_info('people', id)
    if status == 'add':
        if name == 'log':
            data = json.loads(request.get_data())
            return add_log(data)
    if status == 'del':
        if name == 'log':
            return del_log(id)


if __name__ == '__main__':
    app.run(debug = True)
