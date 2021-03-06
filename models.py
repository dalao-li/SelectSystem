from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Log(Base):
    __tablename__ = 'Log'
    id = Column(String(32), primary_key=True)
    name = Column(String(32))
    time = Column(String(32))
    department = Column(String(32))
    people = Column(String(32))
    word1 = Column(String(32))
    word2 = Column(String(32))
    startTime = Column(String(32))
    endTime = Column(String(32))
    identify = Column(String(32))
    # 抽取的人数
    sum = Column(String(32))
    # 抽到的人名
    human = Column(String(32))

    # 补充抽取的人数
    sum2 = Column(String(32))
    # 补充抽到的人名
    human2 = Column(String(32))
    # 备注
    word3 = Column(String(32))

class People(Base):
    __tablename__ = 'People'
    id = Column(String(32), primary_key=True)
    name = Column(String(32))
    sex = Column(String(32))
    human_id = Column(String(32))
    school = Column(String(32))
    department = Column(String(32))
    rank = Column(String(32))
    rank_id = Column(String(32))
    professional1 = Column(String(32))
    professional2 = Column(String(32))
    professional3 = Column(String(32))
    professional4 = Column(String(32))
    professional5 = Column(String(32))
    phone = Column(String(32))
    email = Column(String(32))
    identify = Column(String(32))


class Record(Base):
    __tablename__ = 'Record'
    id = Column(String(32), primary_key=True)
    ip = Column(String(32))
    name = Column(String(32))
    time = Column(String(32))

sqlite_url = 'sqlite:///Info.db?check_same_thread=False'

# 创建引擎
engine = create_engine(sqlite_url)

# 创建表
Base.metadata.create_all(engine)

# 创建DBSession类型:
Session = sessionmaker(bind=engine)

# 创建Session类实例
session = Session()