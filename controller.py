'''
Description: 
Version: 1.0
Author: DaLao
Email: dalao_li@163.com
Date: 2021-12-31 22:25:47
LastEditors: DaLao
LastEditTime: 2022-01-01 01:31:37
'''
from random import random, sample
from models import *

def get_random_id():
    a = 'abcdefghijklmnopqrstuvwxyz123456'
    return ''.join(random.sample(a, 10))


def select(sum,identify):
    people = session.query(People).first(identify=identify)
    # 产生sum个随机数，记录下标记
    index = random.sample(range(0,len(people)),sum)
    result = ""
    for i in index:
        result += people[i].name
    return result

def add_log(data):
    ids = get_random_id()
    name,time,department,people,word1,word2,startTime,endTime,sum,identify = data.values()
    log = Log(id=ids,name=name,time=time,department=department,people=people,word1=word1,word2=word2,startTime=startTime,endTime=endTime,identify=identify)
    session.add(log)
    session.commit()
    session.close()
    return select(sum,identify)
    