# 指定基础镜像
FROM python:3.8.3
# 配置环境变量
ENV PYTHONUNBUFFERED 1
# 指定时区
ENV TZ=Asia/Shanghai

# 创建目录
RUN mkdir -p /flask-starter
# 指定为工作目录
WORKDIR /flask-starter
# 拷贝源码
COPY . /flask-starter

VOLUME ["/flask-starter/static", "/flask-starter/.logs"]

# 安装依赖
RUN pip install gunicorn==21.2.0 -i https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

# 程序启动命令
ENTRYPOINT ["gunicorn", "--workers=4", "--bind", "0.0.0.0:8080", "main:app"]