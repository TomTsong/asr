import logging.config
import multiprocessing
import redis

import config
from log_config import logging_dict_config

from recognizer import SpeechRecognizer
from task import ASRTask

logging.config.dictConfig(logging_dict_config)
logger = logging.getLogger()


urls = [
    "http://1258455058.vod2.myqcloud.com/1def07cdvodcq1258455058/e546c45c243791579844613923/f0.aac",
    "http://1258455058.vod2.myqcloud.com/1def07cdvodcq1258455058/9ad6ba91243791579843741011/f0.aac",
    "http://1258455058.vod2.myqcloud.com/1def07cdvodcq1258455058/dbac6b65243791579861837907/f0.aac",
    "http://1258455058.vod2.myqcloud.com/1def07cdvodcq1258455058/7da29bdb243791579853326813/f0.aac",
    # "http://1258455058.vod2.myqcloud.com/1def07cdvodcq1258455058/cb79a958243791579861152364/f0.aac",
]
infos = [
    {
        "size": 0,
        "duration": 0,
        "url": url,
        "start_time": "",
        "end_time": ""
    } for url in urls
]

def get_audio_info():
    """
    info = {
        "size": 0,
        "duration": 0,
        "url": "",
        "start_time": "",
        "end_time": ""
    }
    """
    if len(infos) > 0:
        info = infos.pop()

    else:
        info = None

    return info


# cli = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
#
#
# def get_audio_info():
#     url = cli.rpop(config.ASR_AUDIO_URL_LIST)
#     if url:
#         return {"url": url}
#
#     return None

rec = SpeechRecognizer(model_name="large")


def run(recognizer):
    while True:
        # 第一步，获取url
        info = get_audio_info()
        if not info:
            logger.info("info is none")
            break

        # 第二步，创建任务，并执行
        task = ASRTask(info, recognizer=recognizer)
        task.run()


def multi_run(num=2, model_name="large"):
    class CustomManager(multiprocessing.managers.BaseManager):
        pass

    CustomManager.register('SpeechRecognizer', SpeechRecognizer)
    with CustomManager() as manager:
        share_recognizer = manager.SpeechRecognizer(model_name=model_name)
        processes = [multiprocessing.Process(target=run, args=(share_recognizer,)) for _ in range(num)]
        for p in processes:
            p.start()

        for p in processes:
            p.join()


if __name__ == "__main__":
    # run()
    num = 2
    multi_run(num)
