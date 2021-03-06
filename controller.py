import datetime
import io
import os
import random
import unicodedata
import xlrd
import xlsxwriter
from flask import make_response

from models import *


def uuid()-> str:
    a = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join(random.sample(a, 32))


def record_log(ip, name)->None:
    log = Record(
        id = uuid(),
        ip = ip,
        name = name,
        time = str(datetime.datetime.now())
    )
    session.add(log)
    session.commit()
    session.close()


def get_login_log():
    return session.query(Record).all()


# 读取上传的excel
def read_excel(f):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    f.save(f.filename)
    e = xlrd.open_workbook(f.filename)
    # 读取第一个sheet
    s = e.sheets()[0]
    a = []
    # 检验格式
    # ['序号', '姓名', '性别', '身份证号', '毕业院校及所学专业', '工作单位', '职  称', '职称证件编号', '专  业', '', '', '', '', '联系电话', '电子信箱', '专家类别']
    if len(s.row_values(1)) != 16:
        return {'code': -1}
    for j in range(s.nrows):
        i = s.row_values(j)
        # 跳过非数据行
        if is_number(i[0]) is False:
            continue
        # 将float数据转为str
        for k in i:
            if isinstance(k, float):
                k = str(int(k))
            k.strip('\n').replace(" ", "")

        p = People(
            id = uuid(),
            name = i[1],
            sex = i[2],
            human_id = i[3],
            school = i[4],
            department = i[5],
            rank = i[6],
            rank_id = i[7],
            professional1 = i[8],
            professional2 = i[9],
            professional3 = i[10],
            professional4 = i[11],
            professional5 = i[12],
            phone = i[13],
            email = i[14],
            identify = i[15]
        )
        a.append(p)
    try:
        session.add_all(a)
        session.commit()
        session.close()
    except:
        session.rollback()
    os.remove(f.filename)
    return {'code': 1}


# status == first 首次
# status == second 补充
def select_people(data, status):
    global code, j
    identify = data['identify']
    s = data['sum']
    p = list(session.query(People).filter(People.identify == identify))
    c = []
    if status == 'first':
        for i in p:
            c.append(i.name)
    if status == 'second':
        # 已经抽取的人名单
        b = data['text'].split(';')
        # 剔除已经抽取的人，在剩余人员中进行抽取
        c = []
        for i in p:
            if i.name not in b:
                c.append(i.name)
    # 没有人
    if not len(c):
        # 该分类下无专家
        if status == 'first':
            return {'code': -1, 'result': ''}
        # 第一次就抽取完了
        if status == 'second':
            return {'code': -2, 'result': ''}
    # 人数少于要抽出的人数
    elif len(c) < int(s):
        if status == 'first':
            code = 2
        if status == 'second':
            code = 3
        j = [i for i in range(len(c))]
    else:
        code = 1
        # 产生sum个随机数，记录下标
        j = random.sample(range(0, len(c)), int(s))
    r = ""
    # 拼接结果
    for i in j:
        r += (c[i] + ';')
    return {'code': code, 'result': r}


def add_log(data: dict) -> dict:
    name, time, department, people, word1, word2, start_time, end_time, identify, s, s2, word3, r, r2 = data.values()

    log = Log(
        id = uuid(),
        name = name,
        time = time,
        department = department,
        people = people,
        word1 = word1,
        word2 = word2,
        startTime = start_time,
        endTime = end_time,
        identify = identify,
        sum = s,
        human = r,
        sum2 = s2,
        human2 = r2,
        word3 = word3
    )
    session.add(log)
    session.commit()
    session.close()
    return {'code': 1}


# 下载抽签记录
def download_excel(uuid: str):
    fp = io.BytesIO()
    b = xlsxwriter.Workbook(fp, {'in_memory': True})
    s = b.add_worksheet('Sheet1')
    data = get_log(uuid)
    # 第一行写标题
    s.write_row('A1', list(data.keys()))
    x = 65
    # A2 B2 C2...写实际书记
    for v in data.values():
        s.write(chr(x) + '2', v)
        x += 1
    b.close()
    response = make_response(fp.getvalue())
    fp.close()
    return response


def del_log(uuid: str):
    if uuid == 'all':
        session.query(Log).delete()
        session.commit()
        session.close()
        return {'code': -1}
    log = session.query(Log).filter(Log.id == uuid)[0]
    session.delete(log)
    session.commit()
    session.close()
    return {'code': 1}


def del_info():
    session.query(People).delete()
    session.commit()
    session.close()
    return {'code': 1}


def get_all_log():
    return session.query(Log).all()


def get_people():
    return session.query(People).all()


def get_info(id)-> dict:
    p = session.query(People).filter(People.id == id)[0]
    data = {
        '姓名: ': p.name,
        '性别: ': p.sex,
        '身份证: ': p.human_id,
        '学校: ': p.school,
        '工作单位: ': p.department,
        '职称: ': p.rank,
        '职称编号: ': p.rank_id,
        '专业1: ': p.professional1,
        '专业2: ': p.professional2,
        '专业3: ': p.professional3,
        '专业4: ': p.professional4,
        '专业5: ': p.professional5,
        '电话: ': p.phone,
        '邮件: ': p.email,
        '类别: ': p.identify
    }
    return data


def get_log(id)-> dict:
    p = session.query(Log).filter(Log.id == id)[0]
    data = {
        '事项名称: ': p.name,
        '受理时间: ': p.time,
        '申请单位: ': p.department,
        '联系人: ': p.people,
        '专家评审内容: ': p.word1,
        '评审专家、领域等事项: ': p.word2,
        '组织时间: ': p.startTime + "/" + p.endTime,
        '类别: ': p.identify,
        '抽取人数: ': p.sum,
        '抽取名单: ': p.human,
        '补抽人数: ': p.sum2,
        '补抽名单: ': p.human2,
        '备注: ': p.word3,
    }
    return data
