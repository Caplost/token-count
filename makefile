# 定义变量
IMAGE_NAME = tiktoken-api
CONTAINER_NAME = tiktoken-api-container

# 构建 Docker 镜像
.PHONY: build
build:
    docker build -t $(IMAGE_NAME) .

# 运行 Docker 容器
.PHONY: run
run:
    docker run -d --name $(CONTAINER_NAME) -p 5000:5000 $(IMAGE_NAME)

# 停止并移除 Docker 容器
.PHONY: stop
stop:
    docker stop $(CONTAINER_NAME)
    docker rm $(CONTAINER_NAME)

# 重新构建并运行
.PHONY: restart
restart: stop build run

# 列出正在运行的容器
.PHONY: ps
ps:
    docker ps

# 进入正在运行的容器
.PHONY: shell
shell:
    docker exec -it $(CONTAINER_NAME) /bin/bash