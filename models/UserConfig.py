#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - UserConfig.py by qiuchenly
#  @时间 : 2024/2/16 上午3:19

from pydantic import BaseModel


class UserCfg(BaseModel):
    key: str
    value: str


class BaseResponse(BaseModel):
    code: int
    msg: str


class SaveConfig(BaseResponse):
    id: int


class GetConfig(BaseResponse):
    value: str


class GetQRCode(BaseResponse):
    url: str
    qrcode_key: str


# {
#     "code": 0,
#     "message": "0",
#     "ttl": 1,
#     "data": {
#         "url": "",
#         "refresh_token": "",
#         "timestamp": 0,
#         "code": 86101,
#         "message": "未扫码"
#     }
# }
class QRCodeStatus(BaseResponse):
    url: str
    refresh_token: str
    timestamp: int
    code: int
    message: str


# 登录成功 返回信息
class LoginResponse(BaseResponse):
    code: int
    SESSDATA: str
    bili_jct: str
    DedeUserID: str
    DedeUserID__ckMd5: str
    sid: str
