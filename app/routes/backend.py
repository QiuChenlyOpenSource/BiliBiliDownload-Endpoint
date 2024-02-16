#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - backend.py by qiuchenly
#  @时间 : 2024/2/16 上午3:01
from fastapi import APIRouter

from bilibili.WebApi import Bilibili
from database import LoginSession
from models.UserConfig import GetQRCode

router = APIRouter(prefix="/bili")

bili = Bilibili()


@router.get("/hello")
async def test_api():
    """
    测试接口是否正常
    :return:
    """
    return {"code": 0}


# 获取登录二维码
@router.get("/login/qrcode")
async def get_login_qrcode() -> GetQRCode:
    code = bili.getQRCode()
    return GetQRCode(
        code=0,
        msg="获取成功",
        url=code["url"],
        qrcode_key=code["qrcode_key"],
    )


# 获取登录二维码状态
@router.get("/login/qrcode/status")
async def get_login_qrcode_status(qrcode_key: str):
    try:
        status = await bili.getQRCodeStatus(qrcode_key)
    except:
        return {
            "code": 400,
            "msg": "触发风控,被ban了。",
        }
    return {
        "code": 0,
        "msg": "获取成功",
        "data": status,
    }


# 获取登录用户列表
@router.get("/login/user")
async def get_login_user():
    # LoginSession
    users = await LoginSession.all()
    return {
        "code": 0,
        "msg": "获取成功",
        "data": [
            {
                "id": user.id,
                "SESSDATA": user.SESSDATA,
                "bili_jct": user.bili_jct,
                "DedeUserID": user.DedeUserID,
                "DedeUserID__ckMd5": user.DedeUserID__ckMd5,
                "sid": user.sid,
            }
            for user in users
        ],
    }


# 通过userid设置当前操作用户
@router.get("/login/user/{userID}")
async def set_login_user(userID: str):
    user = await bili.setUserByUserID(userID)
    return {
        "code": 0,
        "msg": "设置成功",
        "data": {
            "id": user.id,
            "SESSDATA": user.SESSDATA,
            "bili_jct": user.bili_jct,
            "DedeUserID": user.DedeUserID,
            "DedeUserID__ckMd5": user.DedeUserID__ckMd5,
            "sid": user.sid,
        },
    }


# 获取用户信息
@router.get("/login/user/info/")
async def get_user_info():
    info = await bili.getUserInfo()
    return {
        "code": 0,
        "msg": "获取成功",
        "data": info["data"],
    }


# GetUserFavoriteDirectoryByUserId 获取用户uid的收藏夹
@router.get("/login/user/favorite/{uid}")
async def get_user_favorite(uid: int):
    favorite = await bili.GetUserFavoriteDirectoryByUserId(uid)
    return {
        "code": 0,
        "msg": "获取成功",
        "data": favorite["data"],
    }


# GetUserFavoriteDirectoryCollectedByUserId 获取用户收藏的合集
@router.get("/login/user/favorite/collected/{uid}")
async def get_user_favorite_collected(uid: int):
    favorite = await bili.GetUserFavoriteDirectoryCollectedByUserId(uid)
    return {
        "code": 0,
        "msg": "获取成功",
        "data": favorite["data"],
    }


# GetUserFavoriteVideoByMediaId 获取用户收藏夹内的视频
@router.get("/login/user/favorite/video/{media_id}/{pn}/{ps}")
async def get_user_favorite_video(media_id: int, pn=1, ps=20):
    favorite = await bili.GetUserFavoriteVideoByMediaId(media_id, pn, ps)
    return {
        "code": 0,
        "msg": "获取成功",
        "data": favorite["data"],
    }
