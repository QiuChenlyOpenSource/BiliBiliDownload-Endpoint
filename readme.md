# B站视频下载解析后台系统

## 项目介绍

下载b站视频，开发中。

## 软件架构

poetry + fastapi + pydantic + httpx + asyncio + concurrent.futures

## 安装教程

```shell
poetry install
```

## 使用说明

运行后会启动一个http接口服务，端口8000.

```shell
poetry run uvicorn Main:app --reload
```
