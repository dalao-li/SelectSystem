'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2021-12-31 22:25:47
LastEditors: DaLao
LastEditTime: 2022-01-10 11:29:12
'''

import random
from models import *


def get_random_id() -> str:
    a = 'abcdefghijklmnopqrstuvwxyz123456'
    return ''.join(random.sample(a, 10))


def read_excel(f):
    pass

def add_log(data: dict) -> dict:
    name, time, department, people, word1, word2, start_time, end_time, identify, s = data.values()

    p = list(session.query(People).filter(People.identify == identify))
    # 没有这类专家
    if not len(p):
        return {'code': -1, 'result': ''}
    # 人数少于要抽出的人数
    elif len(p) <= int(s):
        code = 0
        index = [i for i in range(len(p))]
    else:
        code = 1
        # 产生sum个随机数，记录下标
        index = random.sample(range(0, len(p)), int(s))
    r = ""
    # 拼接结果
    for i in index:
        r += (p[i].name + '; ')

    # 添加记录
    log = Log(id=get_random_id(), name=name, time=time, department=department, people=people, word1=word1, word2=word2,
              startTime=start_time, endTime=end_time, identify=identify, sum=s, human=r)
    session.add(log)
    session.commit()
    session.close()
    return {'code': code, 'result': r}


def get_log():
    return session.query(Log).all()
    
def get_people():
    return session.query(People).all()