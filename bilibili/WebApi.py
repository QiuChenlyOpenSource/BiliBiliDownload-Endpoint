#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - WebApi.py by qiuchenly
#  @时间 : 2024/2/16 上午11:36
import asyncio
from datetime import datetime, timezone
import json

from database import LoginSession, UserInformationCache
from models.UserConfig import QRCodeStatus, LoginResponse
from utils.Http import HttpRequest
from tortoise.models import Model, DoesNotExist


class Bilibili:

    http: HttpRequest

    def __init__(self):
        self.http = HttpRequest()

    def login(self, username, password):
        pass

    def getQRCode(self):
        u = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header"
        res = self.http.getHttp(
            u,
            header={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            },
        ).json()
        # {"code":0,"message":"0","ttl":1,"data":
        #   {"url":"https://passport.bilibili.com/h5-app/passport/login/scan?navhide=1\\u0026qrcode_key=66cdba76d99fb8f9bd0b5f16d15f626a\\u0026from=main-fe-header",
        #    "qrcode_key":"66cdba76d99fb8f9bd0b5f16d15f626a"}}
        return {
            "url": res["data"]["url"],
            "qrcode_key": res["data"]["qrcode_key"],
        }

    async def getQRCodeStatus(self, qrCodeKey: str):
        u = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrCodeKey}&source=main-fe-header"
        res = self.http.getHttp(
            u,
            header={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            },
        ).json()
        # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'url': 'https://passport.biligame.com/x/passport-login/web/crossDomain?DedeUserID=&DedeUserID__ckMd5=&Expires=&SESSDATA=,,*-&bili_jct=&gourl=https%3A%2F%2Fwww.bilibili.com', 'refresh_token': '', 'timestamp': , 'code': 0, 'message': ''}}

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
        # code 86090
        # message "二维码已扫码未确认"
        if res["data"]["code"] == 0:
            cookie = self.http.getSession().cookies
            # <Cookies[<Cookie SESSDATA= />, <Cookie bili_jct= />, <Cookie DedeUserID= />, <Cookie DedeUserID__ckMd5= />, <Cookie sid= />]>
            # LoginSession 保存到数据库里
            # 先检查DedeUserID 如果存在的话 则更新
            # 如果不存在则创建
            if await LoginSession.filter(DedeUserID=cookie["DedeUserID"]).exists():
                await LoginSession.filter(DedeUserID=cookie["DedeUserID"]).update(
                    SESSDATA=cookie["SESSDATA"],
                    bili_jct=cookie["bili_jct"],
                    DedeUserID=cookie["DedeUserID"],
                    DedeUserID__ckMd5=cookie["DedeUserID__ckMd5"],
                    sid=cookie["sid"],
                )
                session = await LoginSession.get(DedeUserID=cookie["DedeUserID"])
            else:
                session = await LoginSession.create(
                    SESSDATA=cookie["SESSDATA"],
                    bili_jct=cookie["bili_jct"],
                    DedeUserID=cookie["DedeUserID"],
                    DedeUserID__ckMd5=cookie["DedeUserID__ckMd5"],
                    sid=cookie["sid"],
                )

            return LoginResponse(
                code=0,
                message="成功",
                SESSDATA=session.SESSDATA,
                bili_jct=session.bili_jct,
                DedeUserID=session.DedeUserID,
                DedeUserID__ckMd5=session.DedeUserID__ckMd5,
                sid=session.sid,
            )
        return QRCodeStatus(
            msg="成功",
            # code=res["code"],
            message=res["data"]["message"],
            url=res["data"]["url"],
            refresh_token=res["data"]["refresh_token"],
            timestamp=res["data"]["timestamp"],
            code=res["data"]["code"],
        )

    async def setUserByUserID(self, userID: str):
        # 从数据库查找出用户数据
        user = await LoginSession.get(DedeUserID=userID)
        # 设置到http的cookie中
        self.http.getSession().cookies.set("SESSDATA", user.SESSDATA)
        self.http.getSession().cookies.set("bili_jct", user.bili_jct)
        self.http.getSession().cookies.set("DedeUserID", user.DedeUserID)
        self.http.getSession().cookies.set("DedeUserID__ckMd5", user.DedeUserID__ckMd5)
        # self.http.getSession().cookies.set("sid", user.sid) //这个不是cookie中的
        return user

    def getHttp(self, u: str):
        return self.http.getHttp(
            u,
            header={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            },
        )

    async def getUserInfo(self, userId: str | None = None):
        u = "https://api.bilibili.com/x/web-interface/nav"

        need_update = True

        # 如果没有传入mid 则直接请求
        if userId:
            # 先从数据库里拿用户信息
            try:
                user = await UserInformationCache.get(mid=userId)
            except DoesNotExist as e:
                user = None
            if user:
                # 计算当前的时间和更新时间的差值 超过12小时就更新
                need_update = (
                    datetime.now(timezone.utc) - user.updated_at
                ).seconds * 1000 > 1000 * 60 * 60 * 1
                res = json.loads(user.info)

        if need_update:
            res = self.getHttp(u).json()
            res = res["data"]
            if user:
                info = await UserInformationCache.filter(mid=userId).update(
                    info=json.dumps(res), updated_at=datetime.now(timezone.utc)
                )
            else:
                info = await UserInformationCache.create(
                    mid=res["mid"], info=json.dumps(res)
                )

        return res

    async def GetUserFavoriteDirectoryByUserId(self, uid: int):
        u = f"https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={uid}"
        res = self.getHttp(u).json()
        return res

    # https://api.bilibili.com/x/v3/fav/folder/collected/list?pn=1&ps=20&up_mid=&platform=web 根据mid获取收藏和订阅的合集
    async def GetUserFavoriteDirectoryCollectedByUserId(
        self, uid: int, pn: int = 1, ps: int = 20
    ):
        u = f"https://api.bilibili.com/x/v3/fav/folder/collected/list?pn={pn}&ps={ps}&up_mid={uid}&platform=web"
        res = self.getHttp(u).json()
        return res

    # https://api.bilibili.com/x/v3/fav/resource/list?media_id=&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web 根据收藏夹media_id获取收藏夹内的视频
    async def GetUserFavoriteVideoByMediaId(
        self, media_id: int, pn: int = 1, ps: int = 20
    ):
        u = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id={media_id}&pn={pn}&ps={ps}&keyword=&order=mtime&type=0&tid=0&platform=web"
        res = self.getHttp(u).json()
        return res

    # https://api.bilibili.com/x/web-interface/nav/stat 获取动态粉丝信息
    async def GetUserStat(self):
        u = f"https://api.bilibili.com/x/web-interface/nav/stat"
        res = self.getHttp(u).json()
        return res

    async def checkUserCookieNeedUpdate(self, csrf: str):
        # 检查cookie是否过期
        # https://passport.bilibili.com/x/passport-login/web/cookie/info?csrf= 发现这个接口需要让用户更新cookie 暂时没发现有什么用
        u = (
            "https://passport.bilibili.com/x/passport-login/web/cookie/info?csrf="
            + csrf
        )
        """{
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": {
                "refresh": true,
                "timestamp": 1708064491504
            }
        }
        """
        res = self.getHttp(u).json()
        return res

    # https://api.bilibili.com/x/space/wbi/acc/info?mid=&token=&platform=web&web_location=1550101&w_rid=&wts= 根据mid w_rid wts 获取用户主页上的详细信息
    async def GetUserSpaceInfoByMid(self, mid: int):
        # wrid+wts 是根据用户信息算出来的
        wts = ""
        w_rid = ""
        # 先从用户接口取两个Key出来
        #   var t = getLocal("wbi_img_url")
        #   , r = getLocal("wbi_sub_url");

        u = f"https://api.bilibili.com/x/space/wbi/acc/info?mid={mid}&token=&platform=web&web_location=1550101&w_rid={w_rid}&wts={wts}"
        res = self.getHttp(u).json()
        return res
