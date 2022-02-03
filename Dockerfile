FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install  --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/  --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

CMD flask run --host=0.0.0.0 --port=5000

