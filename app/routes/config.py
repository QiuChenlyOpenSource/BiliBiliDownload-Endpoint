#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - config.py by qiuchenly
#  @时间 : 2024/2/16 上午1:46
#

from fastapi import APIRouter
from models.UserConfig import UserCfg, BaseResponse, SaveConfig, GetConfig
from database.DBEntitys import UserConfig

router = APIRouter(prefix="/cfg")


@router.get("/hello")
async def test_api():
    """
    测试接口是否正常
    :return:
    """
    return {"code": 200}


@router.post("/config/")
async def create_config(config: UserCfg):
    # 检查是否存在相同的key
    if await UserConfig.filter(key=config.key).exists():
        return BaseResponse(code=400, msg="key已存在")
    config = await UserConfig.create(key=config.key, value=config.value)
    return SaveConfig(id=config.id, code=200, msg="创建成功")


@router.get("/config/{keyName}")
async def get_config(keyName: str):
    try:
        config = await UserConfig.get(key=keyName)
    except:
        return BaseResponse(code=400, msg="key不存在")
    return GetConfig(
        code=0,
        msg="查询成功",
        value=config.value,
    )


@router.get("/config/")
async def list_configs():
    configs = await UserConfig.all()
    return {
        "config": [
            {"id": config.id, "key": config.key, "value": config.value}
            for config in configs
        ]
    }


# 清空所有配置项目
@router.get("/config/clear")
async def delete_configs():
    await UserConfig.all().delete()
    return {"code": 0, "msg": "清空所有配置项目"}
