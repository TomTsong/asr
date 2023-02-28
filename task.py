import arrow
import logging
import os
import uuid

from cutter import Cutter
from downloader import MultiDownloader
from recognizer import SpeechRecognizer
from collection import TaskCollection, ResultCollection

import config

logger = logging.getLogger()


class ASRTask:
    def __init__(self, audio_info, recognizer=None):
        self.audio_info = audio_info
        self._task = None
        self.recognizer = recognizer

    @staticmethod
    def gen_task_id():
        return str(uuid.uuid1())

    # 私有方法，只能内部调用
    def create(self, info, task_id=None):
        """
        @task_id: 任务ID
        @info：音频信息
        """
        task = {
            "url": info["url"],
            "start_time": info.get("start_time"),
            "end_time": info.get("end_time"),
            "size": info.get("size", 0),
            "duration": info.get("duration", 0),
            "task_id": task_id or self.gen_task_id(),
            "start_download_time": None,
            "end_download_time": None,
            "start_recognize_time": None,
            "end_recognize_time": None,
            "status": config.STATUS_WAITING,  # 0,1,2,3
            "detail": "",
            "create_time": arrow.now().datetime,
            "update_time": arrow.now().datetime
        }
        res = TaskCollection.insert_one(task, remove_id=False)
        self._task = task
        return res

    @staticmethod
    def struct_filename(url):
        return "{}-{}".format(url.split("/")[-2], url.split("/")[-1])

    def struct_filepath(self, url):
        filename = self.struct_filename(url)
        return os.path.join(config.DOWNLOAD_DIR, filename)

    def get_task(self):
        return self._task

    def download(self):
        task = self.get_task()
        url = task["url"]
        params = {
            "url": url,
            "save_path": config.DOWNLOAD_DIR,  # 保存文件的路径
            "file_name": self.struct_filename(url),
            "headers": {},
            "thread_count": 10  # 线程数，即同时下载的任务数
        }
        # 更新文件开始下载的时间
        now = arrow.now().datetime
        TaskCollection.update_one(
            {"_id": task["_id"]},
            {
                "$set": {
                    "status": config.STATUS_START_DOWNLOAD,
                    "start_download_time": now,
                    "update_time": now
                }
            }
        )
        downloader = MultiDownloader(**params)
        try:
            downloader.run()
            # 更新文件下载完成的时间
            now = arrow.now().datetime
            TaskCollection.update_one(
                {"_id": task["_id"]},
                {
                    "$set": {
                        "status": config.STATUS_END_DOWNLOAD,
                        "end_download_time": now,
                        "update_time": now
                    }
                }
            )
            return {"code": config.CODE_SUCCESS}

        except Exception as e:
            logger.info(f"[{task['task_id']}] 下载报错：{e}")
            now = arrow.now().datetime
            TaskCollection.update_one(
                {"_id": task["_id"]},
                {
                    "$set": {
                        "status": config.STATUS_FAIL,
                        "update_time": now,
                        "detail": str(e)
                    }
                }
            )
            return {"code": config.CODE_FAIL, "error": str(e)}

    def recognize(self, language=None):
        task = self.get_task()
        filepath = self.struct_filepath(task["url"])
        size = os.path.getsize(filepath)
        if not self.recognizer:
            self.recognizer = SpeechRecognizer()

        sr = self.recognizer
        logger.info(f"[{task['task_id']}] 音频切条...")
        cutter = Cutter(filepath)
        now = arrow.now().datetime
        TaskCollection.update_one(
            {"_id": task["_id"]},
            {
                "$set": {
                    "size": size,
                    "duration": cutter.total_duration,
                    "status": config.STATUS_START_RECOGNIZE,
                    "start_recognize_time": now,
                    "update_time": now
                }
            }
        )
        logger.info(f"[{task['task_id']}] 音频切条成功.")
        try:
            index = 0
            for file in cutter.pieces():
                logger.info(f"[{task['task_id']}] {file}")
                result = sr.auto_recognize(file, language=language)
                logger.info(f"[{task['task_id']}] 识别文本入库...")
                res = self.save_result(result, index=index)
                if res['code'] == config.CODE_SUCCESS:
                    logger.info(f"[{task['task_id']}] 文本入库成功.")

                else:
                    logger.info(f"[{task['task_id']}] 文本入库失败.")

                index += 1
                os.remove(file)

        # try:
        #     result = sr.auto_recognize(filepath)

        except Exception as e:
            now = arrow.now().datetime
            TaskCollection.update_one(
                {"_id": task["_id"]},
                {
                    "$set": {
                        "status": config.STATUS_FAIL,
                        "end_recognize_time": now,
                        "update_time": now,
                        "detail": str(e)
                    }
                }
            )
            return {
                "code": config.CODE_FAIL,
                "error": str(e)
            }

        now = arrow.now().datetime
        TaskCollection.update_one(
            {"_id": task["_id"]},
            {
                "$set": {
                    "status": config.STATUS_END_RECOGNIZE,
                    "end_recognize_time": now,
                    "update_time": now
                }
            }
        )
        return {"code": config.CODE_SUCCESS}

    def save_result(self, result, index=0):
        task = self.get_task()
        # now = arrow.now()
        # if task.get("start_time"):
        #     now = arrow.get(task["start_time"])

        data = []
        for segment in result["segments"]:
            # start = now.shift(seconds=segment["start"]).format("YYYY-MM-DD HH:mm:ss")
            # end = now.shift(seconds=segment["end"]).format("YYYY-MM-DD HH:mm:ss")
            start = segment["start"]
            end = segment["end"]
            duration = segment["end"] - segment["start"]
            data.append({
                # "url": task["url"],
                "task_id": task["task_id"],
                "index": index,
                "segment_id": segment["id"],
                "start_time": start,
                "end_time": end,
                "duration": duration,
                "text": segment["text"],
            })

        if not data:
            return {"code": 1}

        res = ResultCollection.insert_many(data)
        return res

    def remove_file(self):
        task = self.get_task()
        filepath = self.struct_filepath(task["url"])
        os.remove(filepath)

    def run(self):
        # 第零步，创建任务id
        task_id = self.gen_task_id()

        # 第一步，创建任务
        task = self.get_task()
        if task is not None:
            raise Exception("task exists, please reinit the task")

        logger.info(f"[{task_id}] 任务开始创建...")
        res = self.create(self.audio_info, task_id=task_id)
        if res["code"] != config.CODE_SUCCESS:
            logger.info(f"[{task_id}] 任务创建失败，原因：{res.get('error')}")
            return res

        task = self.get_task()
        logger.info(f"[{task['task_id']}] 任务创建成功：{task}")

        # 第二步，下载音频
        logger.info(f"[{task['task_id']}] 开始下载音频...")
        res = self.download()
        if res["code"] != config.CODE_SUCCESS:
            logger.info(f"音频下载失败，原因：{res.get('error')}")
            return res

        logger.info(f"[{task['task_id']}] 音频下载成功.")

        # 第三步，语音识别
        logger.info(f"[{task['task_id']}] 开始语音识别...")
        res = self.recognize(language="Chinese")
        if res["code"] != config.CODE_SUCCESS:
            logger.info(f"语音识别失败，原因：{res.get('error')}")
            return res

        logger.info(f"[{task['task_id']}] 语音识别成功.")

        self.remove_file()

        # # 第四步，识别结果保存入库
        # logger.info(f"[{task['task_id']}] 开始保存文本...")
        # res = self.save_result(res["data"])
        # if res["code"] != config.CODE_SUCCESS:
        #     logger.info(f"文本保存失败，原因：{res.get('error')}")
        #     return res
        #
        # logger.info(f"[{task['task_id']}] 文本保存成功.")
        return res
