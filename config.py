REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
ASR_AUDIO_URL_LIST = "asr-audio-url-list"

# MONGODB_URI = "mongodb://quality_inspection:gV0EvTuPB1Pdm65@dds-2ze620d946a887641454-pub.mongodb.rds.aliyuncs.com:3717/rtc_service_offline_data"
MONGODB_URI = "mongodb://quality_inspection:gV0EvTuPB1Pdm65@dds-2ze620d946a887641.mongodb.rds.aliyuncs.com:3717/rtc_service_offline_data"
MONGODB_DB = "rtc_service_offline_data"
COLLECTION_TASK = "asr_task_test"
COLLECTION_RESULT = "asr_result_test"
COLLECTION_MONITOR = "asr_monitor_test"

WHISPER_TINY_SIZE = 39 * 1024 * 1024
WHISPER_BASE_SIZE = 74 * 1024 * 1024
WHISPER_SMALL_SIZE = 244 * 1024 * 1024
WHISPER_MEDIUM_SIZE = 769 * 1024 * 1024
WHISPER_LARGE_SIZE = 1550 * 1024 * 1024

DOWNLOAD_DIR = "./download"

STATUS_WAITING = 0
STATUS_START_DOWNLOAD = 1
STATUS_END_DOWNLOAD = 2
STATUS_START_RECOGNIZE = 3
STATUS_END_RECOGNIZE = 4
STATUS_SUCCESS = 8
STATUS_FAIL = 9

CODE_SUCCESS = 1
CODE_FAIL = 0
