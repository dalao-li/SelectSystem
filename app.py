'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2022-01-10 10:38:26
LastEditors: DaLao
LastEditTime: 2022-01-10 11:36:04
'''
"""
Description:
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2021-12-31 08:07:06
LastEditors: DaLao
LastEditTime: 2022-01-02 01:30:07
"""
import json

from flask import Flask, render_template, request

from controller import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data():
    return render_template('data.html')


@app.route('/log', methods=['GET'])
def log():
    data = get_log()
    return render_template('log.html', log = data)

# 抽签
@app.route('/add', methods=['POST'])
def add():
    data = json.loads(request.get_data())
    return add_log(data)

# 上传文件
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    format = f.filename.split('.')[1]
    # 处理excel
    if format in ['xls', 'xlsx']:
        read_excel(f)
        return {'code': 1}
    return {'code': -1}


if __name__ == '__main__':
    app.run(debug=True)
