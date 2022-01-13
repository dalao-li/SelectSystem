'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2021-12-31 22:25:47
LastEditors: DaLao
LastEditTime: 2022-01-13 22:35:08
'''

import random,os
import pandas as pd
import xlwt
from models import *


def get_random_id() -> str:
    a = 'abcdefghijklmnopqrstuvwxyz123456'
    return ''.join(random.sample(a, 32))


def read_excel(f):
    format = f.filename.split('.')[1]
    # 处理excel
    if format not in ['xls', 'xlsx']:
        return {'code': -1}
    f.save("static/download/" + f.filename)
    df = pd.read_excel("static/download/" + f.filename , sheet_name='水资源、水环评项目评审专家库')
    a = []
    for i in df.values:
        p = People(
            id=get_random_id(),
            name=i[1],
            sex=i[2],
            human_id=i[3],
            school=i[4],
            department=i[5],
            rank=i[6],
            rank_id=i[7],
            professional1=i[8],
            professional2=i[9],
            professional3=i[10],
            professional4=i[11],
            professional5=i[12],
            phone=i[13],
            email=i[14],
            identify=i[15]
        )
        a.append(p)
    del(a[0])
    del(a[0])
    try:
        session.query(People).delete()
        session.commit()
        session.close()
    except:
        session.rollback()
    
    session.add_all(a)
    session.commit()
    session.close()
    os.remove("static/download/" + f.filename)
    return {'code': 1}

# 添加抽签记录
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
    log = Log(
        id=get_random_id(),
        name=name, 
        time=time, 
        department=department, 
        people=people, 
        word1=word1, 
        word2=word2,
        startTime=start_time, 
        endTime=end_time, 
        identify=identify, 
        sum=s, 
        human=r
    )
    session.add(log)
    session.commit()
    session.close()
    return {'code': code, 'result': r}

# 下载抽签记录
def download_log(id : str):
    log = session.query(Log).filter(Log.id == id)[0]
    e = xlwt.Workbook()
    s = e.add_sheet("Sheet1")
    e.save("static/download/" + id + ".xls")
    # 写入表格
    s.write(0,0,'名称')
    s.write(0,1,'时间')
    s.write(0,2,'类别')
    s.write(0,3,'人数')
    s.write(0,4,'名单')

    s.write(1,0,log.name)
    s.write(1,1,log.time)
    s.write(1,2,log.identify)
    s.write(1,3,log.sum)
    s.write(1,4,log.human)
   

def get_log():
    return session.query(Log).all()
    
def get_people():
    return session.query(People).all()