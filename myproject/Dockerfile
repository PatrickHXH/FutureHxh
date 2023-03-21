# 建立 python 3.9环境
FROM python:3.9

RUN ln -fs /usr/bin/python3.9 /usr/bin/python3

# 安装netcat
RUN apt-get update && apt install -y netcat


# 设置 python 环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 可选：设置镜像源为国内
#COPY pip.conf /root/.pip/pip.conf

# 容器内创建 myproject 文件夹
ENV APP_HOME=/var/www/html/myproject
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# 将当前目录加入到工作目录中（. 表示当前目录）
ADD . $APP_HOME

# 更新pip版本
# RUN /usr/local/bin/python -m pip install --upgrade pip  #使用drone安装

# 添加当前依赖至镜像
ADD ./requirements.txt $APP_HOME/requirements.txt

# 安装项目依赖
# RUN python3 -m pip install -r requirements.txt   #使用drone安装
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# 移除\r in windows
RUN sed -i 's/\r//' ./start.sh

# 给start.sh可执行权限
RUN chmod +x ./start.sh

# 数据迁移，并使用uwsgi启动服务
ENTRYPOINT /bin/bash ./start.sh