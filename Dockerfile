# 指定基础镜像
FROM python:3.8.3
# 配置环境变量
ENV PYTHONUNBUFFERED 1
# 指定时区
ENV TZ=Asia/Shanghai

# 创建工作目录，拷贝源码
RUN mkdir -p /flask-starter
WORKDIR /flask-starter
COPY ./requirements.txt /flask-starter
COPY ./src /flask-starter

# 安装依赖
RUN pip install gunicorn==20.1.0 -i https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

# 程序启动命令
ENTRYPOINT [ "gunicorn", "--bind" , "0.0.0.0:8080", "main:app"]