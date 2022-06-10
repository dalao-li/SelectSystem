#!/bin/bash

name='select'
tag='v1'

docker rm -f ${name}

docker build -t ${name}:${tag} .

docker run -itd -p 80:5000 --name=${name} ${name}:${tag}