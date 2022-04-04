FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY flask.conf /etc/supervisord.conf

COPY . .

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/  --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

CMD supervisord -c /etc/supervisord.conf

