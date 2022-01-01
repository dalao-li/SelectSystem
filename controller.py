'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2021-12-31 22:25:47
LastEditors: DaLao
LastEditTime: 2022-01-01 17:02:58
'''
import random
from models import *

def get_random_id():
    a = 'abcdefghijklmnopqrstuvwxyz123456'
    return ''.join(random.sample(a, 10))

    
def add_log(data):
    ids = get_random_id()
    name,time,department,people,word1,word2,startTime,endTime,sum,identify = data.values()
    # 添加记录
    log = Log(id=ids,name=name,time=time,department=department,people=people,word1=word1,word2=word2,startTime=startTime,endTime=endTime,identify=identify)
    session.add(log)
    session.commit()
    session.close()
    
    p = session.query(People).filter(identify=identify)
    # 没有这类专家
    if len(p) is False:
        return {'code':-1,'result':''}
    # 人数少于要抽出的人数
    elif len(p) <= sum:
        code = 0
        index = [i for i in range(len(p))]
    else:
        code = 1
        # 产生sum个随机数，记录下标
        index = random.sample(range(0,len(p)),sum)
    r = ""
    # 拼接结果
    for i in index:
        r += p[i].name
    return {'code':code,'result':r}

    