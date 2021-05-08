FROM python:3.8-slim-buster as build_bin
WORKDIR /code
# 复制源文件
COPY {{ app_name }}_watcher /code/{{ app_name }}_watcher/
RUN python -m zipapp -p "/usr/bin/env python3" {{ app_name }}_watcher
COPY {{ app_name }}_sender /code/{{ app_name }}_sender/
RUN python -m zipapp -p "/usr/bin/env python3" {{ app_name }}_sender

FROM python:3.8-slim-buster as build_img
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update -y && apt install -y --no-install-recommends build-essential libsnappy-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /code
COPY pip.conf /etc/pip.conf
RUN pip --no-cache-dir install --upgrade pip
COPY requirements.txt /code/requirements.txt
RUN python -m pip --no-cache-dir install -r requirements.txt
COPY --from=build_bin /code/{{ app_name }}_watcher.pyz /code/
COPY --from=build_bin /code/{{ app_name }}_sender.pyz /code/
ENTRYPOINT ["python"]