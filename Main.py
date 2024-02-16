#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - Main.py by qiuchenly
#  @时间 : 2024/2/15 下午8:53

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routes import router
from database import *

app = FastAPI()

app.include_router(router)

load()
register_tortoise(
    app,
    db_url="sqlite://userdb.sqlite3",
    modules={"models": ["Main"]},
    generate_schemas=True,
    add_exception_handlers=False,
)
