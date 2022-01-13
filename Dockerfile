FROM python:3.10.1-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install  --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/  --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

COPY . .

CMD python3 -m flask run