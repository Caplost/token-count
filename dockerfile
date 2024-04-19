# 使用 Python 3.9 slim 版本作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装 Python 依赖库
RUN pip install --no-cache-dir -r requirements.txt

# 复制 Flask 应用程序代码
COPY app.py .

# 暴露容器端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 启动 Flask 应用程序
CMD ["flask", "run", "--host=0.0.0.0"]