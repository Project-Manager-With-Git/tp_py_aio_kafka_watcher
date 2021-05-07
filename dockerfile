FROM python:3.8-slim-buster as build_bin
WORKDIR /code
# 复制源文件
COPY tp_py_aio_kafka_watcher_watcher /code/tp_py_aio_kafka_watcher_watcher/
RUN python -m zipapp -p "/usr/bin/env python3" tp_py_aio_kafka_watcher_watcher
COPY tp_py_aio_kafka_watcher_sender /code/tp_py_aio_kafka_watcher_sender/
RUN python -m zipapp -p "/usr/bin/env python3" tp_py_aio_kafka_watcher_sender

FROM python:3.8-slim-buster as build_img
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update -y && apt install -y --no-install-recommends build-essential libsnappy-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /code
COPY pip.conf /etc/pip.conf
RUN pip --no-cache-dir install --upgrade pip
COPY requirements.txt /code/requirements.txt
RUN python -m pip --no-cache-dir install -r requirements.txt
COPY --from=build_bin /code/tp_py_aio_kafka_watcher_watcher.pyz /code/
COPY --from=build_bin /code/tp_py_aio_kafka_watcher_sender.pyz /code/
ENTRYPOINT ["python"]