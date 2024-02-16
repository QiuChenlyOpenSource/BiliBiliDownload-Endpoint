#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - __init__.py by qiuchenly
#  @时间 : 2024/2/15 下午9:01
import importlib
import pkgutil

from fastapi import APIRouter

router: APIRouter = APIRouter(prefix="/api/v1")

package = importlib.import_module("app.routes")
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f"app.routes.{module_name}")
    # lst = dir(module)
    router.include_router(getattr(module, "router"))
