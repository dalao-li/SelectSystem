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
def get_data():
    return render_template('data.html')


@app.route('/log', methods=['GET'])
def get_log():
    return render_template('log.html')


@app.route('/add', methods=['POST'])
def add():
    data = json.loads(request.get_data())
    a = add_log(data)
    print(a)
    return a


if __name__ == '__main__':
    app.run()
