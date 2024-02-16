#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - Http.py by qiuchenly
#  @时间 : 2024/2/15 下午8:50
import json
import httpx


class HttpRequest:
    __session = None

    def __init__(self, proxy=None, verifySSL=False):
        # 全局唯一Session
        self.__session = httpx.Client(
            http2=True,
            proxies=proxy,
            follow_redirects=False,
            timeout=5,
            verify=verifySSL,
        )
        # self.__session.verify = False

    def getProxy(self):
        u = "https://service.ipzan.com/core-extract?num=1&no=&minute=3&format=json&repeat=1&protocol=1&pool=quality&mode=whitelist&secret="
        r = self.__session.get(u).json()
        base = r["data"]["list"][0]
        ip = base["ip"]
        port = base["port"]
        proxyMeta = "http://%(host)s:%(port)s" % {
            "host": ip,
            "port": port,
        }
        proxies = {"http://": proxyMeta, "https://": proxyMeta}
        return proxies

    def getHttp(
        self,
        url: str,
        method: int = 0,
        data: [str, bytes] = r"",
        header: dict = {},
        proxy=None,
        noLog=False,
    ):
        """
        Http请求-提交二进制流
        Args:
            url: url网址
            method: 0 表示Get请求 1 表示用POST请求. 默认值为 0.
            data: 提交的二进制流data数据. 默认值为 r''.
            header: 协议头. 默认值为 {}.

        Returns:
            requests.Response: 返回的http数据
        """
        print("请求数据", url, data, header, proxy)
        try:
            if method == 0:
                d = self.__session.get(url, headers=header)
            else:
                d = self.__session.post(url=url, data=data, headers=header)
        except Exception as e:
            print("请求出现问题", e)
            d = None
            return d
        ContentType = d.headers.get("Content-Type")
        if ContentType is not None and ContentType.find("image/") != -1:
            print("Http请求结果", d.status_code, "内容是图片")
        else:
            print("Http请求结果", d.status_code, d.text) if not noLog else None
        return d

    def getHttp2Json(
        self, url: str, method: int = 0, data: dict = {}, header: dict = {}, proxy=""
    ):
        """Http请求-提交json数据

        Args:
            url (str): url网址
            method (int): 0 表示Get请求 1 表示用POST请求. 默认值为 0.
            data (bytes): 提交的json对象数据. 默认值为 {}.
            header (dict): 协议头. 默认值为 {}.

        Returns:
            requests.Response: 返回的http数据
        """
        d = json.dumps(data, ensure_ascii=False)
        d = d.encode("utf-8")
        return self.getHttp(url, method, d, header, proxy)

    def getSession(self):
        return self.__session

    def setCookie(self, ck: httpx.Cookies):
        for a in ck:
            self.__session.cookies.set(a, ck[a])
        # print("cookie set.")
