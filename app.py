'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2022-01-10 10:38:26
LastEditors: DaLao
LastEditTime: 2022-01-11 00:11:38
'''

import json

from flask import Flask, render_template, send_from_directory, request

from controller import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data_page():
    data = get_people()
    return render_template('data.html', data = data)


@app.route('/log', methods=['GET'])
def log_page():
    data = get_log()
    return render_template('log.html', data = data)

# 抽签
@app.route('/add', methods=['POST'])
def add():
    data = json.loads(request.get_data())
    return add_log(data)

# 上传文件
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    return read_excel(f)


@app.route('/download/<id>', methods=['GET'])
def download(id):
    print(id)
    download_log(id)
    return send_from_directory('static/data', id + ".xls")

if __name__ == '__main__':
    app.run(debug=True)
