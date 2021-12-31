'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2021-12-31 08:07:06
LastEditors: DaLao
LastEditTime: 2021-12-31 22:22:07
'''
from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/data')
def get_data():
    return render_template('data.html')


@app.route('/log')
def get_log():
    return render_template('log.html')

@app.route('/add')
def add():
    pass

if __name__ == '__main__':
    app.run()
