#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - Concurrency.py by qiuchenly
#  @时间 : 2024/2/15 下午8:49
import os
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor


class ThreadEx:
    def __init__(self):
        self.maxWorks = 4
        self.mConcurrentPool: ThreadPoolExecutor = None
        self.mPoolThread = []

    def initPool(self, max_works: int):
        """
        初始化线程池
        Args:
            max_works: 线程数量

        Returns:

        """
        self.maxWorks = max_works
        if self.mConcurrentPool is not None:
            self.mConcurrentPool.shutdown(False)
        # for th in concurrent.futures.as_completed(pollCache):
        #     song = th.result()
        self.mConcurrentPool = ThreadPoolExecutor(max_workers=max_works)

    def addTask(
        self,
        callback,
        fn,
        *args,
        **kwargs,
    ):
        t = self.mConcurrentPool.submit(fn, *args, **kwargs)
        t.add_done_callback(callback)
        self.mPoolThread.append(t)
        return True

    def getCurrentResize(self):
        return self.maxWorks
